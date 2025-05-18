from torch.utils.data import Dataset
from collections import Counter
import torch
import json
import math
import os
import numpy as np
import copy
import random
from tqdm import tqdm
import logging
import pandas as pd
from typing import Any, Callable, Dict, List, NewType, Optional, Tuple, Union
import numpy as np
from transformers.tokenization_utils_base import PreTrainedTokenizerBase
from transformers.utils import PaddingStrategy
from utils.configure import Configure
import datasets
import utils
from transformers.feature_extraction_utils import BatchFeature
torch.serialization.add_safe_globals([BatchFeature])
from utils.prompt_templates.fhm import FHM_PROMPT_SCHEMES
from utils.prompt_templates.harmc import HARMC_PROMPT_SCHEMES
from utils.prompt_templates.harmp import HARMP_PROMPT_SCHEMES
from utils.prompt_templates.mami import MAMI_PROMPT_SCHEMES
from utils.prompt_templates.multioff import MultiOFF_PROMPT_SCHEMES
from utils.knowledge.mami import MAMI_TYPE_ABBR_NAME_MAP
from utils.prompt_templates.pridemm import PrideMM_PROMPT_SCHEMES
from utils.prompt_templates.goatbench import GOATBENCH_PROMPT_SCHEMES
from utils.tool import extract_target_group_context

#from utils.format_utils import format_tokens
# from utils.format_prompt import LLM_format_prompt, LMM_format_prompt
# from utils.prompt_templates import argotario_prompt, logic_prompt, elecdebate_prompt, propaganda_prompt, mafalda_prompt, covid_prompt, reddit_prompt

from utils.prompt_templates import *
from utils.format_prompt import LLM_format_prompt, LMM_format_prompt

PROMPT_MAP = {
    "fhm": FHM_PROMPT_SCHEMES,
    "harmc": HARMC_PROMPT_SCHEMES,
    "harmp": HARMP_PROMPT_SCHEMES,
    "mami": MAMI_PROMPT_SCHEMES,
    "multioff": MultiOFF_PROMPT_SCHEMES,
    "pridemm": PrideMM_PROMPT_SCHEMES,
    "gb_hateful": GOATBENCH_PROMPT_SCHEMES["hateful"],
    "gb_offensive": GOATBENCH_PROMPT_SCHEMES["offensive"],
    "gb_misogynistic": GOATBENCH_PROMPT_SCHEMES["misogynistic"],
    "gb_harmful": GOATBENCH_PROMPT_SCHEMES["harmful"],
}

logger = logging.getLogger(__name__)
    
class DataItem(object):
    def __init__(
        self,
        idx,
        inputs,
        label = None,
        attrs = None
    ):
        self.idx = idx
        self.inputs = inputs
        self.label = label
        self.attrs = attrs

torch.serialization.add_safe_globals([DataItem])

def generate_t5_seq2seq_datasets(args, split, cache_folder):
    #seq2seq_cache_path = os.path.join("/".join(cache_path.split("/")[:-1]),  "seq2seq_" + cache_path.split("/")[-1])
    seq2seq_cache_path = os.path.join(cache_folder, 'seq2seq_datasets.cache')
    
    if args.use_dataset_cache and os.path.exists(seq2seq_cache_path):
        seq2seq_datasets = torch.load(seq2seq_cache_path)
        return seq2seq_datasets[split]
    else:
        meta_tuning_data = {}
        if args.do_multitask:
            for task, load_dataset_from in args.config.load_dataset_from:
                if task in args.active_task_list:
                    data_files = {sp: load_dataset_from + f"{sp}.json" for sp in ['train', 'dev', 'test']}
                    task_raw_datasets_split: datasets.DatasetDict = datasets.load_dataset('json', data_files=data_files)
                    task_seq2seq_dataset_split: tuple = utils.tool.get_constructor(args.config.task_seq2seq.constructor)(task, args).\
                        to_seq2seq(task_raw_datasets_split) 
                    meta_tuning_data[cfg_path] = task_seq2seq_dataset_split

        if args.exp_args.model.do_multitask:
            for task, cfg_path in args.exp_args.arg_paths:
                if task in args.active_task_list:
                    task_args = Configure.Get(cfg_path)
                    task_args.bert = args.exp_args.bert
                    data_files = {sp: task_args.dataset.load_from + f"{sp}.json" for sp in ['train', 'dev', 'test']}
                    task_raw_datasets_split: datasets.DatasetDict = datasets.load_dataset('json', data_files=data_files)
                    task_seq2seq_dataset_split: tuple = utils.tool.get_constructor(task_args.seq2seq.constructor)(task_args, args).\
                        to_seq2seq(task_raw_datasets_split) 
                    meta_tuning_data[cfg_path] = task_seq2seq_dataset_split
        else:
            task_args = Configure.Get(args.task_arg_path)
            task_args.bert = args.exp_args.bert
            data_files = {sp: task_args.dataset.load_from + f"{sp}.json" for sp in ['train', 'dev', 'test']}
            task_raw_datasets_split: datasets.DatasetDict = datasets.load_dataset('json', data_files=data_files)
            task_seq2seq_dataset_split: tuple = utils.tool.get_constructor(task_args.seq2seq.constructor)(task_args, args).\
                to_seq2seq(task_raw_datasets_split)
            meta_tuning_data[args.task_arg_path] = task_seq2seq_dataset_split
        seq2seq_dataset_split: tuple = utils.tool.get_constructor(args.exp_args.seq2seq.constructor)(args.exp_args).to_seq2seq(meta_tuning_data)
        seq2seq_train_dataset, seq2seq_dev_dataset, seq2seq_test_dataset = None, None, None 
        if len(seq2seq_dataset_split) == 2:
            seq2seq_train_dataset, seq2seq_dev_dataset = seq2seq_dataset_split
        elif len(seq2seq_dataset_split) == 3:
            seq2seq_train_dataset, seq2seq_dev_dataset, seq2seq_test_dataset = seq2seq_dataset_split
        else:
            raise ValueError("Other split not support yet.")
        seq2seq_datasets = {'train': seq2seq_train_dataset, 'dev': seq2seq_dev_dataset, 'test': seq2seq_test_dataset}
        torch.save(seq2seq_datasets, seq2seq_cache_path)
        print(f"**** Cache seq2seq {args.task}-{split} dataset to {seq2seq_cache_path} ****")
        return seq2seq_datasets[split]
    
class TokenizedDataset(Dataset):
    def __init__(
        self,
        args,
        tokenizer_or_processor=None,
        split='test',
        model_type='lmm',
        model_tag=None,
    ):
        self.args = args
        self.model_type = model_type
        self.model_tag = model_tag
        if args.run_gpt:
            self.op = "formatted"
        else:
            self.op = "tokenized"
            if model_type == 'lmm':
                self.processor = tokenizer_or_processor
            if model_type == 'llm':
                self.tokenizer = tokenizer_or_processor

        self.split = split
        
        cache_file = f"{split}_{self.op}_data.cache"
        cache_folder = os.path.join(args.cache_root, self.model_tag)
        os.makedirs(cache_folder, exist_ok=True)
        cache_path = os.path.join(cache_folder, cache_file)

        self.load_and_cache_data(cache_folder, cache_path)
    
    def load_and_cache_data(self, cache_folder, cache_path):
        args = self.args
        if args.use_dataset_cache and os.path.exists(cache_path):
            print(f"**** Loading {self.op} {self.split} data from cache in {cache_path} ****")
            self.examples = torch.load(cache_path, weights_only=True)
        else:
            print(f"**** Generating {self.op} {args.scheme}-{args.task}-{self.split} dataset for {self.model_tag} from prompted seq2seq data ****")
            # if args.exp_args.model.model_tag.startswith("t5"):
            #     seq2seq_dataset = generate_t5_seq2seq_datasets(args, self.split, cache_folder)
            # else:
            seq2seq_dataset = self.generate_llm_seq2seq_datasets(cache_folder, cache_path)
            self.examples = []
            if seq2seq_dataset:
                i = 0
                for item in tqdm(seq2seq_dataset):
                    if args.run_gpt:
                        self.examples.append(item)
                    else:
                        self.examples.append(self.tokenize_input(i, item))
                    i += 1
                #self.examples = self.examples[:42]
                if args.use_dataset_cache:
                    cached_data = self.examples
                    torch.save(cached_data, cache_path)
                    # torch.serialization.add_safe_globals([type(cached_data)])
                    print(f"**** Cache {self.op} {args.task}-{self.split} dataset to {cache_path} ****")
    
    def __len__(self):
        return len(self.examples)

    def __getitem__(self, i):
        if self.model_tag.startswith("t5"):
            item = {
                'input_ids': torch.LongTensor(self.examples[i].inputs[0]),
                'attention_mask': torch.LongTensor(self.examples[i].inputs[1]),
                'labels': self.examples[i].label
            }
        if self.args.run_gpt:
            item = self.examples[i]
        else:
            if self.model_type == 'llm':
                if self.model_tag.startswith('qwen'):
                    item = {
                        'input_ids': torch.LongTensor(self.examples[i].inputs[0]),
                        'attention_mask': torch.LongTensor(self.examples[i].inputs[1])
                    }
                else:
                    item = {
                        'input_ids': torch.LongTensor(self.examples[i].inputs),
                    } 
            if self.model_type == 'lmm':
                item = self.examples[i].inputs
        return item
    
    # def prepare_task_seq2seq_datasets_from_local(self, args):
    #     data_files = {args.split: args.load_dataset_from + f"{args.split}.json"}
    #     #data_files = {'test': task_args.dataset.load_from + "test_toy.json"}
    #     task_raw_datasets_split: datasets.DatasetDict = datasets.load_dataset('json', data_files=data_files)
    #     # task_seq2seq_dataset_split: tuple = utils.tool.get_constructor(task_args.seq2seq.constructor)(task_args, args).to_seq2seq(task_raw_datasets_split)
    #     task_seq2seq_dataset_split: tuple = utils.tool.get_constructor(args.config.task_seq2seq.constructor)(args.task, args).to_seq2seq(task_raw_datasets_split, self.model_tag) 
    #     seq2seq_dataset_split = {'train':task_seq2seq_dataset_split[0], 'dev':task_seq2seq_dataset_split[1], 'test':task_seq2seq_dataset_split[2]}
    #     return seq2seq_dataset_split
    
    # def prepare_task_seq2seq_datasets_from_data_files(self, args, data_files):
    #     #data_files = {'test': task_args.dataset.load_from + "test_toy.json"}
    #     task_raw_datasets_split: datasets.DatasetDict = datasets.load_dataset('json', data_files=data_files)
    #     # task_seq2seq_dataset_split: tuple = utils.tool.get_constructor(task_args.seq2seq.constructor)(task_args, args).to_seq2seq(task_raw_datasets_split)
    #     task_seq2seq_dataset_split: tuple = utils.tool.get_constructor(args.config.task_seq2seq.constructor)(args.task, args).\
    #         to_seq2seq(task_raw_datasets_split, self.model_tag) 
    #     seq2seq_dataset_split = {'train':task_seq2seq_dataset_split[0], 'dev':task_seq2seq_dataset_split[1], 'test':task_seq2seq_dataset_split[2]}
    #     return seq2seq_dataset_split
    
    def gather_dependency_outputs(self, args, dp_list):
        '''
        dp_list: [{'m_type': 'lmm', 'rid': 0}, {'m_type': 'lmm', 'rid': 1}, {'m_type': 'lmm', 'rid': 2}, ...]
        target format:
        "gathered_predictions": {
            "Human": "There is a human subject ....",
            "Race": "...",
            "Gender": "...",
            "Appearance": "...",
            "Describe": "... similar machines."
        },
        "processed_dependency_prediction": "There is a human subject xxxxxx similar machines."
        '''
        target_file_path = os.path.join(
            args.output_dir_history[args.current_m_type][args.current_round], 
            "gathered_dependency_predictions.json"
        )
        if not os.path.exists(target_file_path):
            dp_outputs = {}
            for dp in dp_list:
                pred_save_path = os.path.join(args.output_dir_history[dp['m_type']][dp['rid']], 'predictions.json')
                for item in json.load(open(pred_save_path)):
                    # if args.task == 'fhm':
                    #     this_info = pred_save_path.split("/")[-2].split("_")[0].split("-")[0]
                    #if args.task in ['fhm', 'harmc', 'harmp', 'mami', 'multioff', 'pridemm']:
                    this_info = "-".join(pred_save_path.split("/")[-2].split("_")[0].split("-")[0:2])
                    this_pred = item.pop("processed_prediction")
                    for attr in ["prediction", "chat_history"]:
                        item.pop(attr)
                    gather = False
                  
                    # dict_condition = isinstance(this_pred, dict) and (this_pred['flag'] in [0,1]) and (this_pred['output'] != "")
                    #if args.task in ['fhm', 'mami', 'harmc', 'harmp', 'multioff', 'pridemm']:
                    dict_condition = isinstance(this_pred, dict) and (this_pred['flag'] == 1) and (this_pred['output'] != "")
                    if dict_condition:
                        pred_output = this_pred['output']
                        gather = True
                    if isinstance(this_pred, str) and (this_pred != ""):
                        pred_output = this_pred
                        gather = True
                    if item["id"] not in dp_outputs:
                        if gather:
                            item["gathered_predictions"] = {this_info: pred_output}
                        else:
                            item["gathered_predictions"] = {}
                        dp_outputs[item["id"]] = item
                    else:
                        if gather:
                            dp_outputs[item["id"]]["gathered_predictions"][this_info] = pred_output
            
            new_data = []
            for id, one_data in dp_outputs.items():
                if args.current_prompt_meta['template']['name'] == "Integrate":
                    ### For reproducibility
                    info_ls = []
                    for info_name, info_pred in one_data["gathered_predictions"].items():
                        info_ls.append(info_pred)
                    if args.task in ["fhm", "gb_hateful"]:
                        info_ls = []
                        for info_name, info_pred in one_data["gathered_predictions"].items():
                            if not info_name.startswith('Describe'):
                                info_ls.append(info_pred)
                            else:
                                Dl = info_pred
                        info_ls.append(Dl)
                        one_data["processed_dependency_prediction"] = " ".join(info_ls) if len(info_ls) > 1 else info_ls[0]
                    elif args.task in ['mami', 'gb_misogynistic', 'gb_harmful', 'harmp', 'harmc', 'pridemm']:
                        one_data["processed_dependency_prediction"] = " ".join([f"{iid+1}. {info}" for iid, info in enumerate(info_ls)])
                    else:
                        one_data["processed_dependency_prediction"] = " ".join([f"{iid+1}. {info}" for iid, info in enumerate(info_ls)]) if len(info_ls) > 1 else info_ls[0]
                else:
                    one_data["processed_dependency_prediction"] = " ".join([pred for _, pred in one_data["gathered_predictions"].items()])
                new_data.append(one_data)
            
            with open(target_file_path, "w") as f:
                json.dump(new_data, f, indent=4,)
        return target_file_path
    
    def fhm_combine_dependency_outputs(self, args, dp_list, align_w_max=True):
        '''
        dp_list: [{'m_type': 'lmm', 'rid': 0}, {'m_type': 'lmm', 'rid': 1}, {'m_type': 'lmm', 'rid': 2}, ...]
        Target format: Combine outputs of different dependency steps, each output is an attribute":
        "Integrate": "output",
        "IntegrateTGContext": "output",
        "id": 03456
        '''
        dp_res_file_dict = {}
        _n_data = []
        for dp in dp_list:
            this_dp_p_meta = args.scheme_dict[dp['m_type']]['prompt'][dp['rid']]
            dp_name = this_dp_p_meta['template']['name']
            # dp_version = this_dp_p_meta["version"]
            # dp_outformat = this_dp_p_meta["out_format"]
            # dp_key = f"{dp_name}-{dp_version}-{dp_outformat}"
            res_dir = args.output_dir_history[dp['m_type']][dp['rid']] 
            dp_key = dp_name
            n_data = len(json.load(open(os.path.join(res_dir, 'predictions.json'))))
            dp_res_file_dict[dp_key] = {
                'path': res_dir,
                'n_data': n_data
            }
            _n_data.append(n_data)
        if args.local_rank <= 0:
            print(dp_res_file_dict)
        if align_w_max:
            for k, v in dp_res_file_dict.items():
                if v['n_data'] == max(_n_data):
                    align_with = k
                    break
        else:
            for k, v in dp_res_file_dict.items():
                if v['n_data'] == min(_n_data):
                    align_with = k
                    break
        target_file_path = os.path.join(
            args.output_dir_history[args.current_m_type][args.current_round], 
            "combined_dependency_predictions.json"
        )
        data_to_add = {k: {} for k, _ in dp_res_file_dict.items() if k != align_with}
        target_group = {}
        for k, v in dp_res_file_dict.items():
            if k != align_with:
                for item in json.load(open(os.path.join(dp_res_file_dict[k]['path'], 'predictions.json'))):
                    data_to_add[k][item['id']] = item['processed_prediction']
                    if (item['id'] not in target_group) and ('TargetGroup' in item):
                        target_group[item['id']] = item['TargetGroup'] 
        new_data = []
        for item in json.load(open(os.path.join(dp_res_file_dict[align_with]['path'], 'predictions.json'))):
            if item['id'] in target_group:
                item['TargetGroup'] = target_group[item['id']]
            else:
                item['TargetGroup'] = []
            item[align_with] = item["processed_prediction"]
            for attr in ["prediction", "chat_history", "processed_prediction"]:
                item.pop(attr)
            for k, v in data_to_add.items():
                if item['id'] in v:
                    dp_pred = v[item['id']]
                    if k == "IntegrateTGContext":
                        if args.current_model.startswith('qwen2.5'):
                            dp_pred = extract_target_group_context(item, v[item['id']], use_ori=False)
                    item[k] = dp_pred
                else:
                    item[k] = ""
            new_data.append(item)
        with open(target_file_path, "w") as f:
            json.dump(new_data, f, indent=4,)
        return target_file_path    
    
    def mami_gather_step_decisions(self, args, dp_list):
        target_file_path = os.path.join(
            args.output_dir_history[args.current_m_type][args.current_round], 
            "gathered_prestep_decisions.json"
        )
        if not os.path.exists(target_file_path):
            dp_outputs = {} # item id as key
            for dp in dp_list:
                step_abbr = args.output_dir_history[dp['m_type']][dp['rid']].split("/")[-1].split("_")[1].split("-")[1]
                step_type = MAMI_TYPE_ABBR_NAME_MAP[step_abbr.strip("*")]
                pred_save_path = os.path.join(args.output_dir_history[dp['m_type']][dp['rid']], 'predictions.json')
                print(pred_save_path)
                for item in json.load(open(pred_save_path)):
                    pp = item.pop("processed_prediction")
                    for attr in ["prediction", "chat_history"]:
                        item.pop(attr) 
                    if item['id'] not in dp_outputs:
                        if step_abbr.endswith("*"):
                            item["prestep_decisions"] = {step_type: {'final': pp}}
                        else:
                            item["prestep_decisions"] = {step_type: {'init': pp}}
                        dp_outputs[item['id']] = item
                    else:
                        if step_abbr.endswith("*"):
                            if step_type not in dp_outputs[item['id']]["prestep_decisions"]:
                                dp_outputs[item['id']]["prestep_decisions"][step_type] = {'final': pp}
                            else:
                                dp_outputs[item['id']]["prestep_decisions"][step_type]['final'] = pp
                        else:
                            if step_type not in dp_outputs[item['id']]["prestep_decisions"]:
                                dp_outputs[item['id']]["prestep_decisions"][step_type] = {'init': pp}
                            else:
                                dp_outputs[item['id']]["prestep_decisions"][step_type]['init'] = pp     
            new_data = []
            for id, one_data in dp_outputs.items():
                new_data.append(one_data)
            with open(target_file_path, "w") as f:
                json.dump(new_data, f, indent=4,)
        
        # ##########################################################
        # new_data = []
        # for item in json.load(open(target_file_path)):
        #     for step, step_dict in item["prestep_decisions"]:
        #         if not step_dict['final']:
        #             item["prestep_decisions"][step]['final'] = {
        #                 "pred_label": "",
        #                 "ori_pred_text": ""
        #             }
        #     new_data.append(item)
        # with open(target_file_path, "w") as f:
        #     json.dump(new_data, f, indent=4,)
        # ##########################################################
        return target_file_path
    
    def get_pre_step_output(self, args, dp_data_path, load_from={}, return_prestep_path=True):
        """
        Incorperate dependency outputs with preceding step output
        """
        if not load_from:
            pre_step = args.precede_step_map[args.current_m_type][args.current_round] # {'m_type': m_type, 'rid': rid}
            pre_step_outputs_path = os.path.join(args.output_dir_history[pre_step['m_type']][pre_step['rid']], "predictions.json")
        else:
            pre_step_outputs_path = os.path.join(args.output_dir_history[load_from['m_type']][load_from['rid']], "predictions.json")
        if (dp_data_path != "") and (dp_data_path != pre_step_outputs_path): # has dependency   
            if return_prestep_path:
                dp_data = {}
                for item in json.load(open(dp_data_path)):
                    dp_data[item['id']] = item
                new_data = []
                for item in json.load(open(pre_step_outputs_path)):
                    dp_item = dp_data[item['id']]
                    dp_key = "processed_dependency_prediction"
                    dp_pred_key = dp_key
                    if dp_pred_key not in dp_item:
                        dp_pred_key = "processed_prediction"
                    if (args.task in ['mami', 'gb_misogynistic']) and ('gather_step_decisions' in args.current_prompt_meta):
                        dp_key = "prestep_decisions"
                        dp_pred_key = dp_key
                    item[dp_key] = dp_item[dp_pred_key]
                    if "gathered_predictions" in dp_item:
                        #################################################
                        # # print(dp_item["gathered_predictions"])
                        # # exit()
                        # g_pred = {}
                        # for k, v in dp_item["gathered_predictions"].items():
                        #     g_pred[k] = v if v is not None else ""
                        # item["gathered_predictions"] = g_pred
                        # # print(item["gathered_predictions"])
                        # # exit()
                        #################################################
                        item["gathered_predictions"] = dp_item["gathered_predictions"]
                    new_data.append(item)
                with open(pre_step_outputs_path, "w") as f:
                    json.dump(new_data, f, indent=4,)
                return pre_step_outputs_path
            else:
                prestep_data = {}
                verbose_keys = list(set(list(json.load(open(dp_data_path))[0].keys()) + ['prediction', "processed_prediction"]))
                for item in json.load(open(pre_step_outputs_path)):
                    prestep_data[item['id']] = {k: v for k, v in item.items() if k not in verbose_keys}
                new_data = []
                for item in json.load(open(dp_data_path)):
                    if (args.task == "gb_harmful") and (args.current_prompt_meta['template']['name'] == "Integrate"):
                        if item['id'] in prestep_data:
                            item.update(prestep_data[item['id']])
                            new_data.append(item)
                    else:
                        assert item['id'] in prestep_data
                        item.update(prestep_data[item['id']])
                        new_data.append(item)
                with open(dp_data_path, "w") as f:
                    json.dump(new_data, f, indent=4,)   
                return dp_data_path 
        return pre_step_outputs_path
    def gbharmful_gather_reasoning(self, args, dp_list):
        target_file_path = os.path.join(
            args.output_dir_history[dp_list[-1]['m_type']][dp_list[-1]['rid']], 
            'predictions.json'
        )
        assert os.path.exists(target_file_path)
        # if not os.path.exists(target_file_path):
        dp_outputs = {} # item id as key
        for item in json.load(open(target_file_path)):
            iid = item["id"]
            itask = item["subtask"]
            dp_outputs[f"{itask}_{iid}"] = item
        for dp in dp_list[:-1]:
            pred_save_path = os.path.join(args.output_dir_history[dp['m_type']][dp['rid']], 'predictions.json')
            print(pred_save_path)
            for item in json.load(open(pred_save_path)):
                iid = item["id"]
                itask = item["subtask"]
                assert f"{itask}_{iid}" not in dp_outputs
                dp_outputs[f"{itask}_{iid}"] = item
        new_data = []
        for id, one_data in dp_outputs.items():
            new_data.append(one_data)
        with open(target_file_path, "w") as f:
            json.dump(new_data, f, indent=4,)
        return target_file_path
    def fhm_post_process_gen_context(self, args, dp_list):
        from utils.tool import post_process_gen_target_group_context
        dp_gen = {'m_type': "", "rid": 0}
        dp_integrate = {}
        for dp in dp_list:
            this_dp_p_meta = args.scheme_dict[dp['m_type']]['prompt'][dp['rid']]
            dp_name = this_dp_p_meta['template']['name']
            if dp_name == "GenTGContext":
                dp_gen['m_type'] = dp['m_type']
                dp_gen['rid'] = dp['rid']
            else:
                dp_integrate['m_type'] = dp['m_type']
                dp_integrate['rid'] = dp['rid']

        gen_context_path = os.path.join(args.output_dir_history[dp_gen['m_type']][dp_gen['rid']], "predictions.json")
        processed_gen_outputs = {}
        for item in json.load(open(gen_context_path)):
            processed_gen_outputs[item["id"]] = {
                "gen_tg_context": post_process_gen_target_group_context(item, item["processed_prediction"]),
                "TargetGroup": item["TargetGroup"]
            }
        
        new_data = []
        if dp_integrate:
            integrate_path = os.path.join(args.output_dir_history[dp_integrate['m_type']][dp_integrate['rid']], "predictions.json")
            for item in json.load(open(integrate_path)):
                if item["id"] in processed_gen_outputs:
                    item.update(processed_gen_outputs[item["id"]])
                else:
                    item["gen_tg_context"], item["TargetGroup"] = [], []
                new_data.append(item)
        else:
            for item in json.load(open(gen_context_path)):
                item["processed_prediction"] = processed_gen_outputs[item["id"]]["gen_tg_context"]
                new_data.append(item)
        save_to = os.path.join(
            args.output_dir_history[args.current_m_type][args.current_round], 
            "after_processed_GenTGContext.json"
        )
        with open(save_to, "w") as f:
            json.dump(new_data, f, indent=4,)
        return save_to
    
    def read_in_gpt_description(self, data_path, raw_data_path):
        gpt_descriptions = {}
        for item in json.load(open(raw_data_path)):
            gpt_descriptions[item['id']] = item["gpt_description"]
        new_data = []
        for item in json.load(open(data_path)):
            if "gpt_description" not in item:
                item["gpt_description"] = gpt_descriptions[item['id']]
            new_data.append(item)
        with open(data_path, "w") as f:
            json.dump(new_data, f, indent=4,)
        return data_path
    
    def generate_llm_seq2seq_datasets(self, cache_folder, cache_path):
        def get_raw_data_path(args):
            # No dependency on previous steps, directly load data from local dir
            surfix = ""
            if args.load_data_surfix != "-":
                surfix = f"_{args.load_data_surfix}"
            data_path = args.load_dataset_from + f"{args.split}{surfix}.json"
            return data_path
        args = self.args
        seq2seq_cache_path = os.path.join(cache_folder,  "seq2seq_" + cache_path.split("/")[-1])
        if args.use_dataset_cache and os.path.exists(seq2seq_cache_path):
            return torch.load(seq2seq_cache_path, weights_only=True)
        else:
            tmp = args.dataload_dependency_map[args.current_m_type][args.current_round]
            if tmp is None:
                # No dependency on previous steps, directly load data from local dir
                surfix = ""
                if args.load_data_surfix != "-":
                    surfix = f"_{args.load_data_surfix}"
                data_path = args.load_dataset_from + f"{args.split}{surfix}.json"
                dp_path = ""
                if (args.run_multiturn) and (args.current_round > 0):
                    if ('new_conversation' not in args.current_prompt_meta):
                        data_path = self.get_pre_step_output(args, dp_path)
                    else:
                        if ('depend_on_prestep' in args.current_prompt_meta) and (args.current_prompt_meta['depend_on_prestep']):
                            data_path = self.get_pre_step_output(args, dp_path)
                if ("load_from_prestep" in args.current_prompt_meta):
                    data_path = self.get_pre_step_output(args, dp_path)
            else: # tmp is a list: [{'m_type': 'lmm', 'rid': 0}]
                assert isinstance(tmp, list)
                if len(tmp) == 1:
                    data_path = os.path.join(args.output_dir_history[tmp[0]['m_type']][tmp[0]['rid']], "predictions.json")
                    # FHM-specific
                    if (args.task in ["fhm", "gb_hateful"]) and (args.current_prompt_meta['template']['name'] == "IntegrateTGContext") and (args.current_prompt_meta['version'] == "v1"):
                        data_path = self.fhm_post_process_gen_context(args, tmp)
                else:
                    if args.current_prompt_meta['template']['name'] == "Integrate":
                        # gather outputs from direct dependencies
                        data_path = self.gather_dependency_outputs(args, tmp)
                    # FHM-specific
                    if (args.task in ["fhm", "gb_hateful"]) and (args.current_prompt_meta['template']['name'] == "Reasoning") and (args.current_prompt_meta['version'] == "CoT+"):
                        data_path = self.fhm_combine_dependency_outputs(args, tmp)
                    if (args.task == ["fhm", "gb_hateful"]) and (args.current_prompt_meta['template']['name'] == "Reasoning") and (args.current_prompt_meta['version'] == "CoT++"):
                        data_path = self.fhm_post_process_gen_context(args, tmp)
                    # MAMI-specific
                    if ('gather_step_decisions' in args.current_prompt_meta):
                        data_path = self.mami_gather_step_decisions(args, tmp)
                    # GB_Harmful-specific
                    if (args.task == "gb_harmful") and (args.current_prompt_meta['template']['name'] == "Decision"):
                        data_path = self.gbharmful_gather_reasoning(args, tmp)

                if args.run_multiturn and (args.current_round > 0):
                    if ('new_conversation' not in args.current_prompt_meta):
                        # Besides depencies, also need to see the chat history of preceding steps
                        data_path = self.get_pre_step_output(args, data_path)
                    else:
                        if ('depend_on_prestep' in args.current_prompt_meta) and (args.current_prompt_meta['depend_on_prestep']):
                            data_path = self.get_pre_step_output(args, data_path)
                if ("load_from_prestep" in args.current_prompt_meta):
                    assert "return_prestep_path" in args.current_prompt_meta
                    data_path = self.get_pre_step_output(args, data_path, return_prestep_path=args.current_prompt_meta["return_prestep_path"])
                if ("load_from" in args.current_prompt_meta):
                    assert "return_load_from_path" in args.current_prompt_meta
                    data_path = self.get_pre_step_output(args, data_path, load_from=args.current_prompt_meta["load_from"], return_prestep_path=args.current_prompt_meta["return_load_from_path"])
            
            if args.current_prompt_meta["version"] == 'CoT+GD':
                raw_data_path = get_raw_data_path(args)
                data_path = self.read_in_gpt_description(data_path, raw_data_path)

            seq2seq_test_dataset = None
            if os.path.exists(data_path):
                data_files = {args.split: data_path}
                task_seq2seq_dataset_split: tuple = utils.tool.get_constructor(args.config.task_seq2seq.constructor)(args.task, args).\
                    to_seq2seq(datasets.load_dataset('json', data_files=data_files), self.model_tag) 
                seq2seq_dataset_split = {
                    'train':task_seq2seq_dataset_split[0], 
                    'dev':task_seq2seq_dataset_split[1], 
                    'test':task_seq2seq_dataset_split[2]
                }
                seq2seq_test_dataset = seq2seq_dataset_split[args.split]

                # if (args.current_modal_id == 0) and (args.current_round == 0):
                #     # Prepare dataset from ori data files only at the very beginning
                #     seq2seq_test_dataset = self.prepare_task_seq2seq_datasets_from_local(args)[args.split]
                # else:
                #     # Prepare dataset from last output dir
                #     data_path = os.path.join(args.last_output_dir, "predictions.json")
                #     if args.use_all_previous_outputs:
                #         data_path = os.path.join(args.last_output_dir, "predictions_gather.json")
                #     data_files = {'test': data_path}
                #     seq2seq_dataset_split: tuple = utils.tool.get_constructor(args.config.task_seq2seq.constructor)(args.task, args).\
                #         to_seq2seq(datasets.load_dataset('json', data_files=data_files), self.model_tag) 
                #     _, _, seq2seq_test_dataset = seq2seq_dataset_split
                
                if args.use_dataset_cache:
                    torch.save(seq2seq_test_dataset, seq2seq_cache_path)
                    if args.local_rank <= 0:
                        prompt_name = args.current_prompt_meta['template']['name']
                        prompt_ver = args.current_prompt_meta['version']
                        print(f"**** Cache seq2seq {args.task}-{args.split}-{args.current_model_type}-{prompt_name}-{prompt_ver} dataset to {seq2seq_cache_path} ****")
            return seq2seq_test_dataset
    
    def tokenize_input(self, idx, js):
        if self.model_tag.startswith("t5"):
            t5_mtask_args = args.exp_args
            seq_in = js['seq_in']
            seq_out = js['label'][0].lower()
            # Concatenate description if any.
            if t5_mtask_args.model.use_description and t5_mtask_args.model.concatenate_description:
                seq_in = "{} ; {}".format(js["description"], seq_in)
            tokenized_input = tokenizer(
                text=seq_in,
                # Enable truncation to max length for t5-3b
                padding="max_length",
                truncation=True,
                max_length=t5_mtask_args.model.max_input_length,
                # We found that set it as large as possible can boost the performance significantly
                # , meanwhile, due to the t5 uses a relative position coding, we need to manually
                # assign the max input length into some large numbers, instead of using the "max_model_length"
                # ,which the default is 512, which will hurt the performance a lot.
            )
            tokenized_inferred = tokenizer(
                text=seq_out,
                padding="max_length",
                truncation=True,
                max_length=t5_mtask_args.model.generation_max_length,
                # We set the max_length of "seq_out" during training is the same with the one in inference.
            )
            tokenized_inferred_input_ids = torch.LongTensor(tokenized_inferred.data["input_ids"])
            # Here -100 will let the model not to compute the loss of the padding tokens.
            # "In addition, we must make sure that padding token id’s of the labels (input_ids of target sequence) 
            # are not taken into account by the loss function. In PyTorch and Tensorflow, this can be done 
            # by replacing them with -100, which is the ignore_index of the CrossEntropyLoss." ---hugging face illustration
            tokenized_inferred_input_ids[tokenized_inferred_input_ids == tokenizer.pad_token_id] = -100
            
            label = tokenized_inferred_input_ids
            input_ids = tokenized_input.data["input_ids"]
            attention_mask = tokenized_input.data["attention_mask"]  
            inputs = (input_ids, attention_mask)
            return DataItem(idx, inputs, label, js)
        else:
            label = js['label']
            dialog = js['chat_history'] # list of messages
            if self.model_type == 'llm':
                inputs = LLM_format_prompt(self.args, self.model_tag, dialog, self.tokenizer)
                return DataItem(idx, inputs, label, js)
            if self.model_type == 'lmm':
                return DataItem(idx, LMM_format_prompt(self.processor, dialog, js['img_history']), label, js)
    