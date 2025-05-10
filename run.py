import os
import sys
import copy
import datasets
import importlib
import time
import random
import logging
import numpy as np
import json
import pprint
from tqdm import tqdm
import multiprocessing
from typing import Dict, Any, List
from datetime import datetime
from arguments import WrappedTrainingArguments
import torch
torch.autograd.set_detect_anomaly(True)
import transformers
from transformers.trainer_utils import get_last_checkpoint
#torch.cuda.set_sync_debug_mode(1)
#torch.backends.cudnn.benchmark = True
from transformers import (
    HfArgumentParser,
    EarlyStoppingCallback,
    WEIGHTS_NAME,
)
from transformers.data.data_collator import DataCollatorWithPadding
# local import
from models.transformers_based import Model
from models.gpt import run_gpt_inference, compute_cost
#from models.gpt_based import do_inference
from dataset import PROMPT_MAP, TokenizedDataset
from trainer import EvaluateFriendlyTrainer
from utils.configure import Configure
import utils.tool
from PIL import Image
# try:
#     from torch.utils.tensorboard import SummaryWriter
# except:
#     from tensorboardX import SummaryWriter

TASK_LIST = list(PROMPT_MAP.keys())
MAP_BATCH_SIZE = {
    'llama3.1': {'mini':32, 'small':16}, # 32, 16
    'qwen2.5': {'mini':32, 'small':32}, # small: 16
    'llama3.2': {'mini':32, 'small':8},
    'qwen2-vl': {'mini':1},
    'qwen2.5-vl': {'mini':1},
    'llava1.6': {'mini':1, 'small':1}, # mini: 1
    'llava1.5': {'mini':1, 'small':1},
}
# Transformers-based Llava series suck in batched inference.....better keep the batch size at 1...

logger = logging.getLogger(__name__)
cpu_cont = multiprocessing.cpu_count()

def set_seed(seed=42):
    random.seed(seed)
    os.environ['PYHTONHASHSEED'] = str(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.backends.cudnn.deterministic = True

class FolderName(object):
    def __init__(self, args):
        self.args = args
        self.use_mask = False # whether to use images with caption masked
        if ('lmm' in args.scheme_dict) and (args.use_mask_img):
            self.use_mask = True

    def get_folder_name_no_date(
        self, 
        run_multiturn, 
        dependencies, 
        rid, 
        p_meta, 
        fix_folder_name=None
    ):
        multiturn_flag = run_multiturn and (rid > 0)
        base_name = f"{p_meta['template']['name']}-{p_meta['version']}-{p_meta['out_format']}"
        should_evaluate = p_meta['template']['should_evaluate'] if 'should_evaluate' in p_meta['template'] else p_meta['template']["versions"][p_meta["version"]]['should_evaluate']
        if should_evaluate:
            f_name = [base_name]
            if dependencies and (not multiturn_flag): # and (not run_multiturn)
                # pre_turn_name = "_".join(pre_turn_name.split("_")[1:])
                #f_name = '_'.join([base_name, dependencies])
                #f_name = [base_name, dependencies]
                f_name.append(dependencies)
        else:
            tmp = [base_name]
            if dependencies and (not multiturn_flag):
                tmp.append(dependencies)
            #f_name = '_'.join(tmp + fix_folder_name)
            if fix_folder_name:
                f_name = tmp + fix_folder_name
        
        if self.use_mask:
            #f_name = '_'.join(['Mask', f_name])
            f_name = ['Mask'] + f_name
        f_name = '_'.join(f_name)

        f_name = f"round-{rid}_" + f_name if multiturn_flag else f_name
        return f_name

def is_turn_res_found(fd_name_no_date, check_dir):
    found = False
    final_check_dir = ""
    for dir in os.listdir(check_dir):
        if dir.startswith(fd_name_no_date):
        #if "_".join(dir.split("_")[:-1]) == fd_name_no_date:
            final_check_dir = os.path.join(check_dir, dir)
            # if os.path.exists(os.path.join(final_check_dir, 'predictions.json')):
            if 'predictions.json' in os.listdir(final_check_dir):
                if not check_dir.split("/")[-1].startswith('gpt'):
                    found = True
                    print(f"Existing experiment predictions file detected in {final_check_dir}, will skip this turn.")
                    break
            else: # turn unfinished
                os.system(f"rm -r {final_check_dir}")
    if found:
        return final_check_dir
    else:
        return ""
        
def check_start_from(args, exist_run_dir):
    # base_idr : ./results/fhm/seed-42/llava1.6-7bf.
    # run_dir: ./results/fhm/seed-42/llava1.6-7bf/S1_len-256_GPU-2_2024xxxxxx
    
    # base_dir: ./results/fhm/seed-42/llama3.1-8bf/
    # exist_run_dir: ./results/fhm/seed-42/llama3.1-8bf/M2T_llava1.6-7bf_len-1024_GPU-2_
    # check which round to start from
    where_to_start_get = False
    for modal_id, item in enumerate(args.scheme_dict.items()):
        m_type, schedule = item[0], item[1] # schedule: {'prompt': {0: {}, 1:{}, ...}, 'multi-turn':T/F}
        model_type = m_type.split("_")[0]
        run_multiturn = schedule['multi-turn']
        this_step_model = args.step_model_map[m_type]
        base_dir = os.path.join(
            args.root_output_dir, args.task, 
            args.dataset_split,
            f"seed-{args.seed}",
            this_step_model,
            # args.step_model_map[m_type] # this_step_model
            # args.llm if model_type == 'llm' else args.lmm
        )
        if model_type == 'llm':
            base_dir = os.path.join(base_dir, args.lmm, f"BS-{args.ori_per_device_eval_batch_size}")
        if not this_step_model.startswith('gpt'):
            this_step_model_size = int(this_step_model.split("-")[-1].strip('bf'))
            if (this_step_model_size <= 13) and (args.use_greedy_decoding_for_mini_models):
                base_dir = os.path.join(args.root_output_dir, args.task, args.dataset_split, this_step_model)
        if this_step_model.startswith('gpt'):
            base_dir = os.path.join(args.root_output_dir, args.task, args.dataset_split, this_step_model)
        if not os.path.exists(base_dir):
            os.makedirs(base_dir, exist_ok=True)
        check_dir, last_output_dir = "", ""
        for rid, p_meta in schedule['prompt'].items():
            if model_type == args.decision_model_type:
                #check_dir = exist_run_dir if p_meta['template']['should_evaluate'] else base_dir
                should_evaluate = p_meta['template']['should_evaluate'] if 'should_evaluate' in p_meta['template'] else p_meta['template']["versions"][p_meta["version"]]['should_evaluate']
                if should_evaluate:
                    if exist_run_dir: # previous run exists
                        check_dir = exist_run_dir
                else:
                    check_dir = base_dir
                    if run_multiturn and (rid > 0):
                        if exist_run_dir:
                            check_dir = exist_run_dir    
            else:
                check_dir = base_dir
            if check_dir:
                fix_folder_name = get_fix_folder_name(args, model_type)
                # pre_turn_name = ""
                # if p_meta['template']['take_last_output']:
                #     pre_turn_name = args.pre_turn_name[model_type][rid]
                dependencies = args.dependency_chain_postfix_map[m_type][rid]
                fd_name_no_date = args.FolderNameGenerator.get_folder_name_no_date(
                    run_multiturn, dependencies, rid, p_meta, fix_folder_name)
                last_output_dir = is_turn_res_found(fd_name_no_date, check_dir)
                # print(f"********{last_output_dir}")
            # if args.log_dir == "":
            if last_output_dir:    
                args.last_output_dir = last_output_dir
                #args.output_dir_history.append(last_output_dir)
                args.output_dir_history[m_type][rid] = last_output_dir
                args.turns_to_skip[m_type].append(rid)
                continue
            else:
                if not where_to_start_get:
                    args.multimodal_start_from = modal_id
                    args.multiturn_start_from = rid
                    #sys_dt = datetime.now().strftime("%Y%m%d%H%M%S")
                    # by default
                    if exist_run_dir:
                        sys_dt = exist_run_dir.split("_")[-1]
                        fd_name = fd_name_no_date + f"_{sys_dt}" if check_dir == base_dir else fd_name_no_date
                        args.current_output_dir = os.path.join(check_dir, fd_name)
                        args.scheme_dir = exist_run_dir
                        #args.log_dir = os.path.join(exist_run_dir, args.eval_folder_name)
                        args.log_dir = args.scheme_dir
                        args.start_sys_time = sys_dt
                    where_to_start_get = True
                    #return args
            # else: # check whether to skip any run after
            #     if last_output_dir:
            #         args.turns_to_skip[model_type].append(rid)
    # Regen results: All 'predictions.json' files found, but no results.json
    if (args.log_dir == "") and (exist_run_dir):
        assert last_output_dir != ""
        args.regen_results = True
        args.current_output_dir = last_output_dir
        args.output_dir = args.current_output_dir
        args.scheme_dir = exist_run_dir
        # args.log_dir = last_output_dir
        args.log_dir = args.scheme_dir
        args.start_sys_time = exist_run_dir.split("_")[-1]
    return args

def gen_current_output_dir(args, tid, p_meta):
    # dict_args = vars(args)
    #is_eval_turn = p_meta['template']['should_evaluate']
    is_eval_turn = p_meta['template']['should_evaluate'] if 'should_evaluate' in p_meta['template'] else p_meta['template']["versions"][p_meta["version"]]['should_evaluate']
    current_step_model = args.step_model_map[args.current_m_type]
    base_dir = os.path.join(
        args.root_output_dir, args.task,
        args.dataset_split,
        f"seed-{args.seed}",
        current_step_model,
        # args.step_model_map[args.current_m_type],
        # dict_args[args.current_model_type]
    )
    if args.current_m_type.startswith('llm'):
        base_dir = os.path.join(base_dir, args.lmm, f"BS-{args.ori_per_device_eval_batch_size}")
    if not current_step_model.startswith('gpt'):
        current_step_model_size = int(current_step_model.split("-")[-1].strip('bf'))
        if (current_step_model_size <= 13) and (args.use_greedy_decoding_for_mini_models):
            base_dir = os.path.join(args.root_output_dir, args.task, args.dataset_split, current_step_model)
    if current_step_model.startswith('gpt'):
        base_dir = os.path.join(args.root_output_dir, args.task, args.dataset_split, current_step_model)
    fix_folder_name = get_fix_folder_name(args, args.current_model_type)
    # pre_turn_name = ""
    # if p_meta['template']['take_last_output']:
    #     pre_turn_name = args.pre_turn_name[args.current_model_type][tid]
    dependencies = args.dependency_chain_postfix_map[args.current_m_type][tid]
    fd_name_no_date = args.FolderNameGenerator.get_folder_name_no_date(
        args.run_multiturn, dependencies, tid, p_meta, fix_folder_name)
    if is_eval_turn:
        #parent_dir = args.log_dir
        parent_dir = args.scheme_dir
        current_output_dir = os.path.join(args.scheme_dir, fd_name_no_date)
    else:
        parent_dir = base_dir
        current_output_dir = os.path.join(base_dir, fd_name_no_date + f"_{args.start_sys_time}")
        if (args.run_multiturn) and (tid > 0):
            current_output_dir = os.path.join(args.scheme_dir, fd_name_no_date)
            
    # # Remove previous unfinished dir
    # if os.path.exists(parent_dir):
    #     is_turn_res_found(fd_name_no_date, parent_dir)
    return current_output_dir

def _check_before(args, check_dir):
    # check_dir: results/fhm/seed-42/llama3.1-8bf (final model)
    if os.path.exists(check_dir):
        next_check_dir = ""
        for fd in os.listdir(check_dir):
            # results/fhm/seed-42/llama3.1-8bf/
            if fd.startswith(args.eval_folder_name):
                assert args.has_eval_turn is False
                res_save_path = os.path.join(check_dir, fd)
                if 'predictions.json' in os.listdir(res_save_path):
                    print(f"Existing experiment results detected in {res_save_path}, skip this run.")
                    args.skip_run = True
                else:
                    print("Unfinished run detected, checking where to restart from ......")
                    os.system(f"rm -r {res_save_path}")
                    continue

            if "_".join(fd.split("_")[:-1]) == args.results_dir_name_no_date:
                next_check_dir = os.path.join(check_dir, fd) # S1_len-256_GPU-2_2024xxxxx
                contents = os.listdir(next_check_dir)
                for step in contents:
                    if step.startswith(args.eval_folder_name):
                        res_save_path = os.path.join(next_check_dir, step)
                        #if any([res_file in contents for res_file in ['result.json']]):
                        if f"result{args.target_result_surfix}.json" in os.listdir(res_save_path):
                            print(f"Existing experiment results detected in {res_save_path}, skip this run.")
                            args.skip_run = True
                        else:
                            if 'predictions.json' in os.listdir(res_save_path):
                                if args.has_eval_turn:
                                    print(f"Existing experiment predictions file detected in {res_save_path}, will regen results to this dir.")
                                else:
                                    print(f"Existing experiment results detected in {res_save_path}, skip this run.")
                                    args.skip_run = True
                            else:
                                print("Unfinished run detected, checking where to restart ...")
                        break
            
        #if further_check:
        if not args.skip_run:
            print("Checking where to start from ......")
            args = check_start_from(args, next_check_dir) 
        # args.multimodal_start_from
        # args.multiturn_start_from
        # args.current_output_dir
        # args.log_dir
        # args.start_sys_time
        #break
    # No record found, create result store dir
    if (not args.skip_run) and (args.log_dir == ""):
        # create log_dir at scheme-level
        sys_dt = datetime.now().strftime("%Y%m%d%H%M%S")
        # args.results_dir_name_no_date: M2T_llava1.6-7bf_len-1024_GPU-2
        scheme_fd_name = args.results_dir_name_no_date + f"_{sys_dt}"
        args.start_sys_time = sys_dt
        #args.log_dir = os.path.join(check_dir, scheme_fd_name, args.eval_folder_name)
        args.scheme_dir = os.path.join(check_dir, scheme_fd_name)
        args.log_dir = args.scheme_dir
    return args

def get_fix_folder_name(args, model_type):
    dict_args = vars(args)
    args_used_in_name = []
    if model_type == 'llm':
        args_used_in_name.append(['llm_max_new_tokens','len'])
    if model_type == 'lmm':
        args_used_in_name.append(['lmm_max_new_tokens','len'])
    fix_folder_name = []
    for arg_name, rename in args_used_in_name:
        fix_folder_name.append(f"{rename}-{dict_args[arg_name]}")
    
    if (model_type == 'llm') and args.llm.startswith("qwen2.5"):
        fix_folder_name.append(f"BS-{args.ori_per_device_eval_batch_size}")

    #if not args.scheme.startswith("GPT"):
    fix_folder_name.append(f"GPU-{args.world_size}")
    return fix_folder_name

def check_before_running(args):
    args.skip_run = False
    args.regen_results = False
    args.has_eval_turn = False
    args.FolderNameGenerator = FolderName(args)
    args.eval_folder_name = ""
    args.results_dir_name_no_date = ""

    args.multipt_start_from, args.multimodal_start_from, args.multiturn_start_from = 0, 0, 0
    args.current_output_dir, args.last_output_dir, args.log_dir, args.scheme_dir, args.start_sys_time = "", "", "", "", ""

    if args.local_rank <= 0:
        for sid, p_meta in args.scheme_dict[args.decision_m_type]['prompt'].items():
            should_evaluate = p_meta['template']['should_evaluate'] if 'should_evaluate' in p_meta['template'] else p_meta['template']["versions"][p_meta["version"]]['should_evaluate']
            if should_evaluate:
                args.has_eval_turn = True
                # pre_turn_name = ""
                # if p_meta['template']['take_last_output']:
                #     pre_turn_name = args.pre_turn_name[args.decision_model_type][sid]
                dependencies = args.dependency_chain_postfix_map[args.decision_m_type][sid]
                args.eval_folder_name = args.FolderNameGenerator.get_folder_name_no_date(
                    args.scheme_dict[args.decision_m_type]['multi-turn'], 
                    dependencies, sid, p_meta, fix_folder_name=None)
                #print(f'check_before_running= {args.eval_folder_name}')
        
        dict_args = vars(args)
        tmp = [] 
        for m_type in args.scheme_dict:
            mt = m_type.split("_")[0] # llm_1, llm_2
            if (mt != args.decision_model_type) and (args.step_model_map[m_type] not in tmp):
                tmp.append(args.step_model_map[m_type])
        folder_name = [args.scheme] + tmp
        #if 
        # args_used_in_name = []
        # if args.llm_max_new_tokens == args.lmm_max_new_tokens:
        #     args_used_in_name.append(['max_new_tokens','len'])
        # else:
            
        # fix_folder_name = []
        # for arg_name, rename in args_used_in_name:
        #     fix_folder_name.append('{}-{}'.format(rename, dict_args[arg_name]))
        # fix_folder_name.append(f"GPU-{args.world_size}")
        # args.folder_surfix = fix_folder_name

        fix_folder_name = get_fix_folder_name(args, args.decision_model_type)
        folder_name_no_date = '_'.join(folder_name + fix_folder_name)
        args.results_dir_name_no_date = folder_name_no_date
        
        if not args.has_eval_turn:
            print("There is no evluation turn.")
            final_schedule = args.scheme_dict[args.decision_m_type]
            run_mutltit = final_schedule['multi-turn']
            final_rid = max(list(final_schedule['prompt'].keys()))
            final_p_meta = final_schedule['prompt'][final_rid]
            # pre_turn_name = ""
            # if final_p_meta['template']['take_last_output']:
            #     pre_turn_name = args.pre_turn_name[args.decision_model_type][final_rid]
            dependencies = args.dependency_chain_postfix_map[args.decision_m_type][sid]
            args.eval_folder_name = args.FolderNameGenerator.get_folder_name_no_date(
                run_mutltit, dependencies, final_rid, final_p_meta, fix_folder_name)
            
        # check_dir is where the results stored, it's under the decision model folder
        check_dir = os.path.join(
            args.root_output_dir, args.task, 
            args.dataset_split,
            f"seed-{args.seed}",
            dict_args[args.decision_model_type]
        )
        if args.decision_model_type == 'llm':
            check_dir = os.path.join(check_dir, args.lmm, f"BS-{args.ori_per_device_eval_batch_size}")
        if not args.decision_model.startswith('gpt'):
            if (args.decision_model_size <= 13) and (args.use_greedy_decoding_for_mini_models):
                check_dir = os.path.join(args.root_output_dir, args.task, args.dataset_split, dict_args[args.decision_model_type])
        if not os.path.exists(check_dir):
            os.makedirs(check_dir, exist_ok=True)
        args = _check_before(args, check_dir)
    
    torch.distributed.barrier(device_ids=[args.local_rank])
     
    # Broadcast
    # skip_run
    args.skip_run = [args.skip_run]
    torch.distributed.broadcast_object_list(args.skip_run, src=0, device=args.device)
    args.skip_run = args.skip_run[0]
    # regen_results
    args.regen_results = [args.regen_results]
    torch.distributed.broadcast_object_list(args.regen_results, src=0, device=args.device)
    args.regen_results = args.regen_results[0]

    if (not args.skip_run) and (not args.regen_results):
        args.has_eval_turn = [args.has_eval_turn]
        args.eval_folder_name = [args.eval_folder_name]
        args.results_dir_name_no_date = [args.results_dir_name_no_date]
        args.multimodal_start_from = [args.multimodal_start_from]
        args.multiturn_start_from = [args.multiturn_start_from]
        args.output_dir_history = [args.output_dir_history]
        args.turns_to_skip = [args.turns_to_skip]
        args.output_dir = [args.output_dir]
        args.current_output_dir = [args.current_output_dir]
        args.last_output_dir = [args.last_output_dir]
        args.log_dir = [args.log_dir]
        args.scheme_dir = [args.scheme_dir]
        args.start_sys_time = [args.start_sys_time]
        for item in [args.has_eval_turn, args.eval_folder_name, args.results_dir_name_no_date, args.multimodal_start_from, args.multiturn_start_from, args.output_dir_history, args.turns_to_skip, args.output_dir, args.current_output_dir, args.last_output_dir, args.log_dir, args.scheme_dir, args.start_sys_time]:
            torch.distributed.broadcast_object_list(item, src=0, device=args.device)
        args.has_eval_turn = args.has_eval_turn[0]
        args.eval_folder_name = args.eval_folder_name[0]
        args.results_dir_name_no_date = args.results_dir_name_no_date[0]
        args.multimodal_start_from = args.multimodal_start_from[0]
        args.multiturn_start_from = args.multiturn_start_from[0]
        args.output_dir_history = args.output_dir_history[0]
        args.turns_to_skip = args.turns_to_skip[0]
        args.output_dir = args.output_dir[0]
        args.current_output_dir = args.current_output_dir[0]
        args.last_output_dir = args.last_output_dir[0]
        args.log_dir = args.log_dir[0]
        args.scheme_dir = args.scheme_dir[0]
        args.start_sys_time = args.start_sys_time[0]
        # args = [args]
        # torch.distributed.broadcast_object_list(args, src=0, device=initial_args.device)
        # args = args[0]
        if (args.local_rank <= 0) and (not os.path.exists(args.scheme_dir)):
            os.makedirs(args.scheme_dir)
            print(f"In check_before_running: args.current_output_dir = {args.current_output_dir}")
        torch.distributed.barrier(device_ids=[args.local_rank])
    return args
    
def setup_wandb(args):
    args.run_name = "_".join([args.task, args.exp_args.model.model_tag])
    if ("wandb" in args.report_to) and (args.local_rank <= 0):
        print("start wandb...")
        import wandb
        init_args = {}
        if "MLFLOW_EXPERIMENT_ID" in os.environ:
            init_args["group"] = os.environ["MLFLOW_EXPERIMENT_ID"]
        # Get system's datetime
        sys_dt = datetime.now().strftime("%Y%m%d%H%M%S")
        wandb.init(
            project=os.getenv("WANDB_PROJECT", "fallacy"),
            name='{}_{}'.format(args.run_name, sys_dt),
            entity=os.getenv("WANDB_ENTITY", 'fengjunp-nus'),
            **init_args,
        )
        wandb.config.update(args, allow_val_change=True)
    torch.distributed.barrier(device_ids=[args.local_rank])
def setup_logging(args):
    #------------------------------- Set up logging --------------------------------#
    # Initialize the logger
    if (args.report_to == 'wandb') and (not args.regen_results):
        setup_wandb(args)
    # Reset logging handler
    # Remove all handlers associated with the root logger object.
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
    log_file_name = '{}-{}.log'.format('run', args.start_sys_time)
    log_file = os.path.join(args.log_dir, log_file_name)
    # if os.path.exists(log_file):
    #     os.system(f"rm -r {log_file}")
    # log_file = os.path.join(args.log_dir, log_file_name)
    #log_file_name = 'run.log'
    logging.basicConfig(filename=log_file,
                        filemode='a',
                        format='%(asctime)s - %(levelname)s - %(name)s -   %(message)s',
                        datefmt='%m/%d/%Y %H:%M:%S',
                        level=logging.INFO if args.local_rank <= 0 else logging.WARN)
    logger.info("Process rank: %s, device: %s, n_gpu: %s, distributed training: %s, 16-bits training: %s",
                args.local_rank, args.device, args.n_gpu, bool(args.local_rank != -1), args.fp16)
    # Set seed
    set_seed(args.seed)    

class ProcessorDataCollator:
    def __init__(self, processor):
        super(ProcessorDataCollator, self).__init__()
        self.processor = processor

    def __call__(self, batch_features: List[Dict[str, Any]]) -> Dict[str, Any]:
        batch_text, batch_images = [], []
        for one_data in batch_features:
            batch_text.append(one_data['text'])
            batch_images.extend([Image.open(img_path) for img_path in one_data['img_paths']])
        return self.processor(
            images=batch_images,
            text=batch_text,
            padding=True,
            return_tensors="pt"
        )
        
def run(args, model=None, type=None, evaluator=None):
    if not args.logging_set:
        setup_logging(args)
    if (evaluator is None) and (args.should_evaluate):
        # evaluator = utils.tool.get_evaluator(args.exp_args.evaluate.tool)(args)
        evaluator = utils.tool.get_evaluator(args.config.evaluate.meta_evaluator)(args)
    
    if model is None:
        model = Model(args)
    # if args.exp_args.model.model_tag.startswith("t5"):
    #     train_dataset, eval_dataset = None, None
    #     if args.do_train:
    #         train_dataset = TokenizedDataset(args, model.tokenizer, split='train')
    #         eval_dataset = TokenizedDataset(args, model.tokenizer, split='dev')
    #     test_dataset = TokenizedDataset(args, model.tokenizer, split='test')
    #     early_stopping_callback = EarlyStoppingCallback(early_stopping_patience=args.exp_args.seq2seq.patience if args.exp_args.seq2seq.patience else 5)
    # else:
    train_dataset, eval_dataset, early_stopping_callback = None, None, None
    test_dataset = None
    if args.local_rank <= 0:
        #args.task_args = Configure.Get(args.task_arg_path)
        test_dataset = TokenizedDataset(
            args,
            model.tokenizer if model.type == 'llm' else model.processor, 
            split=args.split,
            model_type=model.type,
            model_tag=model.model_tag
        )
    torch.distributed.barrier(device_ids=[args.local_rank])
    test_dataset = [test_dataset]
    for item in [test_dataset]:
        torch.distributed.broadcast_object_list(item, src=0, device=args.device)
    test_dataset = test_dataset[0]
    #------------------------------- Create Trainer --------------------------------#
    if model.type == 'llm':
        data_collator = DataCollatorWithPadding(model.tokenizer, padding="longest")
    if model.type == 'lmm':
        data_collator = ProcessorDataCollator(model.processor)
    trainer = EvaluateFriendlyTrainer(
        args=args,
        evaluator=evaluator,
        model=model,
        processing_class=model.tokenizer if model.type == 'llm' else model.processor,
        #tokenizer=model.tokenizer
        data_collator = data_collator,
        train_dataset=train_dataset,
        eval_dataset=eval_dataset,
        callbacks=[early_stopping_callback] if early_stopping_callback is not None else None
    )
    logger.info('***** Trainer built successfully. ***** \n')
    if args.local_rank <= 0:
        print('***** Trainer built successfully. ***** \n')
    # if args.local_rank == 0:
    #     torch.distributed.barrier()  

    # End of barrier to make sure only the first process in distributed training download model & vocab
    if len(test_dataset) == 0:
        print(f"NO data in test dataset. Will skip this run.")
        os.system(f"rm -r {args.current_output_dir}")
        del evaluator
        return
    
    if model.model_tag.startswith("t5"):
        # Load model weights (for --do_train=False or post finetuning).
        if args.load_weights_from:
            state_dict = torch.load(os.path.join(args.load_weights_from, transformers.WEIGHTS_NAME), map_location="cpu")
            trainer.model.load_state_dict(state_dict, strict=True)
            print("***** Load the previous checkpoint. *****\n")
            logger.info("***** Load the previous checkpoint. *****\n")
            # release memory
            del state_dict
    # Training
    if args.do_train:
        # Detect last checkpoint and check whether to train from scratch or to train from last checkpoint
        last_checkpoint = None
        if os.path.isdir(args.output_dir) and not args.overwrite_output_dir:
            last_checkpoint = get_last_checkpoint(args.output_dir)
            if last_checkpoint is None and len(os.listdir(args.output_dir)) > 0:
                raise ValueError(
                    f"Output directory ({args.output_dir}) already exists and is not empty. "
                    "Use --overwrite_output_dir to overcome."
                )
            elif last_checkpoint is not None and args.resume_from_checkpoint is None:
                logger.info(
                    f"Checkpoint detected, resuming training at {last_checkpoint}. To avoid this behavior, change "
                    "the `--output_dir` or add `--overwrite_output_dir` to train from scratch."
                )
        checkpoint = None
        if args.resume_from_checkpoint is not None:
            checkpoint = args.resume_from_checkpoint
        elif last_checkpoint is not None:
            checkpoint = last_checkpoint
        start_time = time.time()
        train_result = trainer.train(resume_from_checkpoint=checkpoint)
        trainer.save_model()  # Saves the tokenizer too for easy upload
        metrics = train_result.metrics
        max_train_samples = len(train_dataset)
        metrics["train_samples"] = min(max_train_samples, len(train_dataset))
        trainer.log_metrics("train", metrics)
        trainer.save_metrics("train", metrics)
        trainer.save_state()
        train_time = start_time - time.time()
        logger.info(f"train_time = {train_time}")
    # Evaluation
    if args.do_eval:
        start_time = time.time()
        logger.info("***** Evaluate *****")
        metrics = trainer.evaluate(metric_key_prefix="eval")
        max_eval_samples = len(eval_dataset)
        metrics["eval_samples"] = min(max_eval_samples, len(eval_dataset))
        trainer.log_metrics("eval", metrics)
        trainer.save_metrics("eval", metrics)
        eval_time = start_time - time.time()
        logger.info(f"eval_time = {eval_time}")
    # Predict
    if args.do_predict:
        logger.info("***** Predict *****")
        test_outputs = trainer.predict(
            test_dataset=test_dataset #if test_dataset else eval_dataset
        )
        if args.should_evaluate:
            metrics = test_outputs.metrics
            metrics["predict_samples"] = len(test_dataset)
            trainer.log_metrics("predict", metrics)
            if not args.do_not_save_results:
                trainer.save_metrics("predict", metrics)
    #del model
    del evaluator
    return

def run_gpt(args):
    cost = 0
    if args.local_rank <= 0:
        test_dataset = TokenizedDataset(
            args,
            split=args.split,
            model_type='gpt',
            model_tag=args.current_model
        )
        cost = run_gpt_inference(args, test_dataset)
        print(f"Finished running {len(test_dataset)} entries spending ${cost}.")
    torch.distributed.barrier(device_ids=[args.local_rank])
    cost = [cost]
    torch.distributed.broadcast_object_list(cost, src=0, device=args.device)
    cost = cost[0]
    return cost

def gather_previous_outputs(args):
    first_file = os.path.join(args.output_dir_history[0], 'predictions.json')
    target_file = os.path.join(args.output_dir_history[-1], "predictions_gather.json")
    assert os.path.exists(first_file)
    if not os.path.exists(target_file):
        all_data = {}
        for item in json.load(open(first_file)):
            item['img_info'] = []
            item["processed_output"] = [item["processed_output"]]
            all_data[item['id']] = item
        for dir in args.output_dir_history[1:]:
            info_type = dir.split("/")[-1].split("_")[0].split("-")[0]
            file = os.path.join(dir, 'predictions.json')
            #print(file)
            assert os.path.exists(file)
            for item in json.load(open(file)):
                po = item["processed_output"]
                if isinstance(po, dict):
                    if (po['flag'] == 1) and (po['output'] != ""):
                        all_data[item['id']]['img_info'].append(info_type)
                        all_data[item['id']]["processed_output"].append(po['output'])
                if isinstance(po, str) and (po != ""):
                    all_data[item['id']]['img_info'].append(info_type)
                    all_data[item['id']]["processed_output"].append(po)
        new_data = []
        for id, item in all_data.items():
            item["processed_output"] = " ".join([op for op in item["processed_output"]])
            new_data.append(item)
        with open(target_file, "w") as f:
            json.dump(new_data, f, indent=4,)     
    return 

def run_model(args):
    # Run each model's prompt schedule
    model_cost = 0.
    if not args.run_gpt:
        model = Model(args)
        if not model.model_tag.startswith("qwen2.5"):
            if model.model_size <= 8:
                args.set_per_device_eval_batch_size = MAP_BATCH_SIZE[model.model_tag]['mini']
            else:
                args.set_per_device_eval_batch_size = MAP_BATCH_SIZE[model.model_tag]['small']
        else:
            args.set_per_device_eval_batch_size = copy.deepcopy(args.ori_per_device_eval_batch_size)
    args.run_multiturn = args.current_prompt_schedule['multi-turn']
    #for rid, p_meta in args.current_prompt_schedule['prompt'].items():
    for r_order, rid in enumerate(args.current_prompt_schedule['prompt']):
        p_meta = args.current_prompt_schedule['prompt'][rid]
        run_this_turn = True
        if (args.current_modal_id == args.multimodal_start_from) and (rid < args.multiturn_start_from):
            run_this_turn = False
        if rid in args.turns_to_skip[args.current_m_type]:
            run_this_turn = False
        if run_this_turn:
            args.current_round = rid
            args.current_prompt_meta = p_meta
            args.should_evaluate = p_meta['template']['should_evaluate'] if 'should_evaluate' in p_meta['template'] else p_meta['template']["versions"][p_meta["version"]]['should_evaluate']
            
            if args.current_output_dir == "":
                args.current_output_dir = gen_current_output_dir(args, rid, p_meta)
            args.output_dir = args.current_output_dir
            args.output_dir_history[args.current_m_type][rid] = args.current_output_dir
            if not os.path.exists(args.output_dir):
                os.makedirs(args.output_dir, exist_ok=True)
            
            if args.local_rank <= 0:
                print(f"Start running step-{rid}: {p_meta['template']['name']}-{p_meta['version']}")
                print(f"current output_dir = {args.output_dir}")
                print(f"last_output_dir = {args.last_output_dir}")
                tmp = pprint.pformat(args.output_dir_history)
                print(f"output_dir_history:{tmp}")
            torch.distributed.barrier(device_ids=[args.local_rank])
            if not args.run_gpt:
                args.per_device_eval_batch_size = args.set_per_device_eval_batch_size
                if args.task in ['harmc', 'harmp', 'multioff', 'mami']:
                    if (args.run_multiturn) and (rid > 0):
                        if (args.per_device_eval_batch_size > 2):
                            args.per_device_eval_batch_size = args.per_device_eval_batch_size - 2
                elif args.task in ['fhm', 'pridemm']:
                    if "batch_size" in p_meta:
                        args.per_device_eval_batch_size = p_meta['batch_size']
                    else:
                        if (args.run_multiturn) and (rid > 0):
                            #and ("new_conversation" not in p_meta):
                            reduce_by = 2
                            if (args.task == 'fhm') and (args.set_per_device_eval_batch_size == 32):
                                reduce_by = 4 if r_order > 1 else 2
                            reduce_num = reduce_by * r_order
                            if (args.set_per_device_eval_batch_size > reduce_num):
                                args.per_device_eval_batch_size = args.set_per_device_eval_batch_size - reduce_num
                            if args.should_evaluate:
                                args.per_device_eval_batch_size = 16
                # if (args.run_multiturn) and (rid > 0):
                #     if (args.per_device_eval_batch_size > 2):
                #         args.per_device_eval_batch_size = args.per_device_eval_batch_size - 2
                print(f"args.per_device_eval_batch_size = {args.per_device_eval_batch_size}; args.do_sample={args.do_sample}")

                update_args = args
                if ('max_new_tokens' in p_meta):
                    update_args = copy.deepcopy(args)
                    if (args.current_m_type.startswith('llm')):
                        update_args.llm_max_new_tokens = p_meta["max_new_tokens"]
                    if (args.current_m_type.startswith('lmm')):
                        update_args.lmm_max_new_tokens = p_meta["max_new_tokens"]
                if args.should_evaluate:
                    update_args.do_sample = False
                
                model.setup_gen_kwargs(update_args)
                print(model.model.dtype)
                run(args, model)
                #run_if_oom(args, model)
            else:
                this_cost = run_gpt(args)
                model_cost += this_cost
                
            args.last_output_dir = args.output_dir
            args.current_output_dir = ""
            args.use_all_previous_outputs = False
            # prepare next output_dir
    if not args.run_gpt:
        del model
    return model_cost

def make_cache_root(args):
    args.cache_root = os.path.join('cache', args.task)
    os.makedirs(args.cache_root, exist_ok=True)
    return args

def regen_results(args):
    if args.has_eval_turn:
        setup_logging(args)
        evaluator = utils.tool.get_evaluator(args.config.evaluate.meta_evaluator)(args)
        assert 'predictions.json' in os.listdir(args.current_output_dir)
        all_pg = json.load(open(os.path.join(args.current_output_dir, 'predictions.json')))
        predictions, golds = [], []
        for one_data in all_pg:
            pred = one_data.pop("prediction")
            predictions.append(pred)
            golds.append(one_data)
        evaluator.evaluate(preds=predictions, golds=golds, section="inference", epoch=None)
        return

def get_precede_step_map(args):
    precede_step = {'m_type': None, 'rid': None}
    precede_step_map = {m_type: {} for m_type in args.scheme_dict}
    for m_type, p in args.scheme_dict.items():
        for rid, p_meta in p['prompt'].items():
            precede_step_map[m_type][rid] = precede_step
            precede_step = {'m_type': m_type, 'rid': rid}
    return precede_step_map

def traceback_for_dp_chain(pre_steps, dp_name_list, pre_steps_map):
    '''
    dp_chain: chain of dependency, 
    the dependencies of every step involved are included to form a chain
    changes to any of the step in the chain indicates one unique experiment setting
    '''
    dp_steps = []
    if dp_name_list is None:
        return dp_steps
    sids = list(pre_steps.keys())
    sids.reverse()
    pre_steps_ = {sid: pre_steps[sid] for sid in sids}
    for sid, s in pre_steps_.items():
        if s['prompt_name'] in dp_name_list:
            dp_steps.append(sid)
            dp_steps.extend(traceback_for_dp_chain(pre_steps_map[s['m_type']][s['rid']], s['dp_name'], pre_steps_map))
    return dp_steps

def get_dataload_dp(pre_steps, dp_name_list):
    '''
    dataload_dp: direct dependencies regarding data loading for generation
    only the previous steps, the output of which will be used in the current step, are inlcuded
    disregarding the dependencies of these steps
    '''
    direct_dp_steps = []
    # add to list following the same order in which the steps are executed
    for sid, s in pre_steps.items():
        if s['prompt_name'] in dp_name_list:
            direct_dp_steps.append({'m_type': s['m_type'], 'rid': s['rid']})
    return direct_dp_steps

def get_generation_dependency(args):
    '''
    Goal: To obtain folder name dependency postfix for each step.
    '''
    dict_args = vars(args)
    dependency_chain_postfix_map = {m_type: {} for m_type in args.scheme_dict}
    dataload_dependency_map = {m_type: {} for m_type in args.scheme_dict}
    step_chain = {}
    pre_steps_map = {m_type: {} for m_type in args.scheme_dict}
        
    step_idx = 0
    for m_type, p in args.scheme_dict.items():
        # m_type: llm_1, llm_2
        model_tag = args.step_model_map[m_type]
        
        for rid, p_meta in p['prompt'].items():
            step_idx += 1
            pre_steps_map[m_type][rid] = step_chain # is a dict

            #dp_name = p_meta['template']['gen_depend_on']
            if 'gen_depend_on' in p_meta['template']:
                # all versions of this prompt share one same dependency type
                dp_name = p_meta['template']['gen_depend_on']
            else:
                # each version specifies one dependency type
                dp_name = p_meta['template']['versions'][p_meta["version"]]['gen_depend_on']

            if dp_name is None:
                dependency_chain_postfix_map[m_type][rid] = ""
                dataload_dependency_map[m_type][rid] = None

            if isinstance(dp_name, list): # ["Human"]
                this_pre_steps = pre_steps_map[m_type][rid]
                dataload_dependency_map[m_type][rid] = get_dataload_dp(this_pre_steps, dp_name)

                # reorder 
                all_dp_step_ids = traceback_for_dp_chain(this_pre_steps, dp_name, pre_steps_map)
                assert set(all_dp_step_ids).issubset(set(list(this_pre_steps.keys())))
                #this_pre_steps.reverse()
                sids = list(this_pre_steps.keys())
                sids.reverse()
                this_pre_steps_ = {sid: this_pre_steps[sid] for sid in sids}
                all_dp_steps_in_model_groups = {}
                for sid, s in this_pre_steps_.items():
                    if sid in all_dp_step_ids:
                        if (s['m_type']) not in all_dp_steps_in_model_groups:
                            all_dp_steps_in_model_groups[s['m_type']] = [s['postfix']]
                        else:
                            all_dp_steps_in_model_groups[s['m_type']].append(s['postfix'])
                dp_postfix = []
                for smt, pls in all_dp_steps_in_model_groups.items():
                    tmp = "_".join(pls)
                    smodel = args.step_model_map[smt]
                    if smodel != model_tag:
                        tmp = f"({smodel}:{tmp})"
                    dp_postfix.append(tmp)
                dependency_chain_postfix_map[m_type][rid] = "_".join(dp_postfix).strip("_")
            step_chain[step_idx] = {
                'm_type': m_type, 
                'rid': rid, 
                'prompt_name':p_meta['template']['name'], 
                'dp_name': dp_name,#p_meta['template']['gen_depend_on']
                'postfix': f"{p_meta['template']['name']}-{p_meta['version']}-{p_meta['out_format']}"
            }
            
    return dependency_chain_postfix_map, dataload_dependency_map

def get_step_model_map(args):
    model_specifications = {
        'lmm': args.lmm.split(","), 
        'llm': args.llm.split(",")
    }
    step_model_map = {}
    for m in list(args.scheme_dict.keys()):
        mt = m.split("_")[0]
        mp = model_specifications[mt]
        if len(mp) == 1:
            step_model_map[m] = mp[0]
        else:
            assert len(mp) > 1
            idx = int(m.split("_")[1]) - 1
            step_model_map[m] = mp[idx] 
    return step_model_map

def set_output_randomness_params(args):
    # Set output randomness params
    def set_randomness(args):
        if args.seed == 42:
            # Use greedy decoding, no sampling, deterministic, ensuring reproducibility
            args.do_sample = False
            args.temperature = 0.
            args.top_p = 1.0
        else:
            args.do_sample = True
            args.temperature = 0.
            args.top_p = 0.9
        return args
    
    current_model_size = int(args.current_model.split("-")[-1].strip('bf'))
    if args.current_model.startswith('gpt'):
        return set_randomness(args)
    else:
        current_model_size = int(args.current_model.split("-")[-1].strip('bf'))
        if (current_model_size <= 13) and (args.use_greedy_decoding_for_mini_models):
            args.do_sample = False
            return args
        else:
            return set_randomness(args)

def main():
    # Get args
    parser = HfArgumentParser((WrappedTrainingArguments,))
    args, = parser.parse_args_into_dataclasses()
    args.ddp_find_unused_parameters = False

    # Setup CUDA, GPU & distributed training
    if args.local_rank == -1 or args.no_cuda:
        print("!!!! Use multi-GPU training with Data Parallel !!!!")
        device = torch.device("cuda" if torch.cuda.is_available() and not args.no_cuda else "cpu")
    # if args.local_rank <= 0:
    print(f"device = {args.device}, local_rank={args.local_rank}, n_gpu={args.n_gpu}")

    # Read in meta arguments
    args.config = Configure.Get(args.cfg)
    args.logging_set = False
    args.root_output_dir = args.output_dir
    active_task_list = TASK_LIST if args.which_task == 'all' else [t.strip() for t in args.which_task.split(',')] 
    args.active_task_list = active_task_list
    if args.local_rank <= 0:
        print(args.active_task_list)
    args.last_output_dir = ""
    args.skip_run = False
    args.ori_per_device_eval_batch_size = args.per_device_eval_batch_size

    args.use_all_previous_outputs = False
    args.gather_dependencies = False

    run_cost = 0.
    for task, load_dataset_from in args.config.load_dataset_from:
        if args.local_rank <= 0:
            print(f"task = {task}; load_dataset_from={load_dataset_from}")
        torch.distributed.barrier(device_ids=[args.local_rank])
        if task in active_task_list:
            
            args.task = task
            args.load_dataset_from = load_dataset_from

            # Once we have scheme dict, we can obtain the mapping of chains or postfix
            args.scheme_dict = PROMPT_MAP[task][args.scheme]
            # This is to find out the preceding step of every step
            args.precede_step_map = get_precede_step_map(args)
            # This is to find out the folder name postfix of chain of previous steps
            args.step_model_map = get_step_model_map(args)
            args.dependency_chain_postfix_map, args.dataload_dependency_map = get_generation_dependency(args)
            # print(args.dependency_chain_postfix_map)
            # print(args.dataload_dependency_map)
            # print(args.step_model_map)
  
            # args.pre_turn_name = get_scheme_chain(args)
             
            args.decision_m_type = list(args.scheme_dict)[-1]
            args.decision_model_type = args.decision_m_type.split("_")[0] # in case, llm_1, llm_2
            args.decision_model = args.step_model_map[args.decision_m_type]
            if not args.decision_model.startswith('gpt'):
                args.decision_model_size = int(args.decision_model.split("-")[-1].strip('bf'))
            args.output_dir_history = {m_type: {} for m_type in args.scheme_dict}
            args.turns_to_skip = {m_type: [] for m_type in args.scheme_dict}
            
            surfix = ""
            if args.load_data_surfix != "-":
                surfix = f"_{args.load_data_surfix}"
            args.dataset_split = f"{args.split}{surfix}"
            
            # if args.local_rank <= 0:
            #     for i in range(50):
            #         print(i)
            #         time.sleep(1)
            # torch.distributed.barrier(device_ids=[args.local_rank])
            
            args = check_before_running(make_cache_root(args))
            
            if args.skip_run:
                break
            if args.regen_results:
                if args.local_rank <= 0:
                    regen_results(args)
                torch.distributed.barrier(device_ids=[args.local_rank])
                continue
            
            if args.local_rank <= 0:
                print(f"Main result dir = {args.scheme_dir}")
                start_model = list(args.scheme_dict)[args.multimodal_start_from]
                start_turn = args.scheme_dict[start_model]['prompt'][args.multiturn_start_from]['template']['name']
                print(f"Start from running {start_model} from turn {args.multiturn_start_from}: {start_turn}")
            torch.distributed.barrier(device_ids=[args.local_rank])

            setup_logging(args)
            args.logging_set = True
            for modal_id, item in enumerate(args.scheme_dict.items()):
                if modal_id >= args.multimodal_start_from:
                    m_type, schedule = item[0], item[1]
                    args.current_modal_id = modal_id
                    args.current_m_type = m_type # llm_1, llm_2, lmm_1
                    args.current_model_type = m_type.split("_")[0] # llm or lmm
                    args.current_prompt_schedule = schedule # {'prompt': {}, 'multi-turn':True or False}
                    args.current_model = args.step_model_map[m_type]
                    args.run_gpt = False
                    if args.current_model.startswith('gpt'):
                        args.run_gpt = True
                    if not args.run_gpt:
                        args = set_output_randomness_params(args)

                    this_cost = run_model(args)
                    if this_cost > 0:
                        run_cost += this_cost    
    if (run_cost > 0) and (args.local_rank <= 0):
        print(f"Spent a TOTAL of ${round(run_cost,3)} running on {args.active_task_list}.")

    torch.distributed.destroy_process_group()

if __name__ == "__main__":
    main()