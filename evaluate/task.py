import os
import copy
import numpy as np
import json
import regex
from sklearn.metrics import roc_auc_score, f1_score, precision_score, recall_score, balanced_accuracy_score, accuracy_score, confusion_matrix, classification_report
import pprint
import random
from utils.tool import extract_json_output
from utils.knowledge.mami import MAMI_TYPE_ABBR_NAME_MAP
import torch
from datetime import datetime
import logging
logger = logging.getLogger(__name__)


MAP_TO_LABEL = {'hateful': 1, 'non-hateful': 0, 'harmful':1, 'benign':0, 'yes': 1, 'no': 0, '1': 1, '0': 0, '999': 'gen_error'}
MAP_TO_SEEN = {0: 'unseen', 1: 'seen'}
class EvaluateTool(object):
    """
    The task evaluator
    """
    def __init__(self, args):
        self.args = args
        self.task = args.current_eval_task
        self.output_dir = args.output_dir
        if args.decision_model_type == 'finetune':
            self.output_dir = os.path.join(args.output_dir, self.task)
            os.makedirs(self.output_dir, exist_ok=True)
        for sid, p_meta in args.scheme_dict[args.decision_m_type]['prompt'].items():
            should_evaluate = p_meta['template']['should_evaluate'] if 'should_evaluate' in p_meta['template'] else p_meta['template']["versions"][p_meta["version"]]['should_evaluate']
            if should_evaluate:
                self.post_process_func = p_meta['template']['output_format'][p_meta['out_format']]['post_process_func']
                break
    def confirm_mami_pred_label(self, step_decisions):
        # step_decisions: dict
        # {'Harmful Stereotypes': {
        # 'init': {'pred_label': 1, 'ori_pred_text': "xxx"}, 
        # 'final': {'pred_label': 1, 'ori_pred_text': "xxx"}, 
        # }
        # }
        def get_label(res):
            if res in [404]:
                return 1
            if isinstance(res, dict):
                return res['pred_label']
        # miso_commits = []
        # for type, step_res in step_decisions.items():
        #     if 'final' in step_res:
        #         if get_label(step_res['final']):
        #             miso_commits.append(type)
        #     else:
        #         assert 'init' in step_res
        #         if get_label(step_res['init']):
        #             miso_commits.append(type)
        # final_pred_label = 0
        # if len(miso_commits) > 0:
        #     final_pred_label = 1
        miso_type_res = {}
        for type, step_res in step_decisions.items():
            if 'final' in step_res:
                s_label = get_label(step_res['final'])
            else:
                assert 'init' in step_res
                s_label = get_label(step_res['init']) # 0,1,2
            miso_type_res[type] = 1 if s_label == 1 else 0
            if type.lower().startswith("advocating violence"):
                miso_type_res[type] = 1 if s_label !=0 else 0
        
        final_pred_label = 1
        if all([v==0 for v in list(miso_type_res.values())]):
            final_pred_label = 0
        return {'pred_label': final_pred_label, 'miso_commits': miso_type_res}
    
    def confirm_pridemm_pred_label(self, step_decisions):
        assert isinstance(step_decisions["s1"], dict)
        s1_pred = step_decisions["s1"]["pred_label"]
        
        s2_pred = None
        if isinstance(step_decisions["s2"], dict):
            s2_pred = step_decisions["s2"]["pred_label"]
        
        final_pred_label = 0
        if any([s1_pred, s2_pred]):
            final_pred_label = 1
        return {'pred_label': final_pred_label}
    
    def evaluate(self, preds, golds, section='predict', epoch=None):
        args = self.args
        summary = {}
        predictions, labels, failed, incorrect, correct = [], [], [], [], []
        n_failed_ = {'seen':0, 'unseen':0}
        pred_labels, gt_labels = [], []
        if self.task == 'fhm':
            pred_labels_all, gt_labels_all = {'seen': [], 'unseen': []}, {'seen': [], 'unseen': []}

        for pred, gold in zip(preds, golds):
            if 'prediction' in gold:
                gold.pop('prediction')
            if self.task == 'fhm':
                split = MAP_TO_SEEN[gold['is_seen']]
                gt_labels = gt_labels_all[split]
                pred_labels = pred_labels_all[split]
            gt_labels.append(gold['label'])
            
            if not callable(self.post_process_func): # By default
                output = extract_json_output(pred, keys=["explanation"])
            elif callable(self.post_process_func):
                output = self.post_process_func(pred)
            
            #20240222
            if (self.task == 'mami') and ("StepDecision" in args.eval_folder_name):
                #and (args.current_prompt_meta['template']['name'] == "StepDecision"):
                # output is the processed prediction of final step "violence"
                # output = {'pred_label': 0/1/2, 'ori_pred_text': "conclusion: ..."}
                step_decisions = gold["prestep_decisions"]
                this_step_abbr = args.eval_folder_name.replace("round", "").strip("-").split("-")[1]#args.current_prompt_meta["version"]
                this_step_type = MAMI_TYPE_ABBR_NAME_MAP[this_step_abbr.strip("*")]
                if this_step_abbr.endswith("*"):
                    step_decisions[this_step_type] = {'final': output}
                else:
                    step_decisions[this_step_type] = {'init': output}
                output = self.confirm_mami_pred_label(step_decisions)

            if (self.task == 'pridemm') and ("StepDecision" in args.eval_folder_name):
                output = self.confirm_pridemm_pred_label(gold["step_decision"])

            if output in [404]:
                one_fail = dict(**{'prediction': pred}, **gold)
                failed.append(one_fail)
                pred_labels.append((-1) * gold['label'] + 1)
            else:
                pred_label = output['pred_label']
                pred_labels.append(pred_label)

                tmp = {'prediction': pred_label, 'ori_output': pred}
                if 'ori_pred_label' in output: 
                    tmp.update({'ori_pred_label': output['ori_pred_label']})
                if (self.task == 'mami') and ('miso_commits' in output):
                    tmp.update({'pred_sub_label': output['miso_commits']})
                one_success = dict(**tmp, **gold)
                if pred_label != gold['label']:
                    incorrect.append(one_success)
                else:
                    correct.append(one_success)
                                                                                                                 
            # # CE7454
            # if output in ['failed_to_extract_json', 'gen_error']:
            #     one_fail = dict(**{'prediction': pred, 'error_type': output}, **gold)
            #     failed.append(one_fail)
            #     pred_labels.append((-1) * gold['label'] + 1)
            # else:
            #     pred_label = None
            #     for key in ['hateful', 'decision', 'flag']:
            #         if key in output:
            #             try:
            #                 pred_label = MAP_TO_LABEL[str(output[key]).lower()]
            #                 if pred_label == 'gen_error':
            #                     one_fail = dict(**{'prediction': pred, 'error_type': pred_label}, **gold)
            #                     failed.append(one_fail)
            #                     pred_label = (-1) * gold['label'] + 1
            #             except:
            #                 try:
            #                     value = output[key].lower()
            #                     if any(w in value for w in ['non', 'not']):
            #                         pred_label = MAP_TO_LABEL['non-hateful']
            #                     else:
            #                         pred_label = MAP_TO_LABEL['hateful']
            #                 except:
            #                     pred_label = (-1) * gold['label'] + 1
            #             pred_labels.append(pred_label)
            #             break
                
            #     if pred_label is None:
            #         one_fail = dict(**{'prediction': output, 'error_type': "Unspecified dict key"}, **gold)
            #         failed.append(one_fail)
            #         pred_labels.append((-1) * gold['label'] + 1)
            #     else:
            #         one_success = dict(**{'prediction': pred_label, 'extracted_output': output}, **gold)
            #         if pred_label != gold['label']:
            #             incorrect.append(one_success)
            #         else:
            #             correct.append(one_success)
        
        #align, notalign = [], []
        icannot_statistics = {'align': [], 'notalign':[]}
        if (self.task == 'fhm') and (args.scheme == 'S4') and (args.regen_results) and (args.target_result_surfix == '_icannot'):
            print("I cannot ....")
            failed, incorrect, correct = [], [], []
            pred_labels_all, gt_labels_all = {'seen': [], 'unseen': []}, {'seen': [], 'unseen': []}
            for pred, gold in zip(preds, golds):
                if 'prediction' in gold:
                    gold.pop('prediction')
                split = MAP_TO_SEEN[gold['is_seen']]
                gt_labels = gt_labels_all[split]
                pred_labels = pred_labels_all[split]
                gt_labels.append(gold['label'])
                #pred_label_found = False
                pred_label_icannot = None
                for msg in gold["chat_history"]:
                    if msg['role'] == "assistant":
                        if msg["content"].startswith("I cannot"):
                            pred_label_icannot = 1
                            #pred_labels.append(1)
                            #pred_label_found = True
                            break
                #if not pred_label_found:
                if not callable(self.post_process_func): # By default
                    output = extract_json_output(pred, keys=["explanation"])
                elif callable(self.post_process_func):
                    output = self.post_process_func(pred)
                if output in ['failed_to_extract_json', 'gen_error']:
                    one_fail = dict(**{'prediction': pred, 'error_type': output}, **gold)
                    failed.append(one_fail)
                    pred_label = (-1) * gold['label'] + 1
                    #pred_labels.append((-1) * gold['label'] + 1)
                else:
                    pred_label = None
                    for key in ['hateful', 'decision', 'flag']:
                        if key in output:
                            try:
                                pred_label = MAP_TO_LABEL[str(output[key]).lower()]
                                if pred_label == 'gen_error':
                                    one_fail = dict(**{'prediction': pred, 'error_type': pred_label}, **gold)
                                    failed.append(one_fail)
                                    pred_label = (-1) * gold['label'] + 1
                            except:
                                try:
                                    value = output[key].lower()
                                    if any(w in value for w in ['non', 'not']):
                                        pred_label = MAP_TO_LABEL['non-hateful']
                                    else:
                                        pred_label = MAP_TO_LABEL['hateful']
                                except:
                                    pred_label = (-1) * gold['label'] + 1
                            #pred_labels.append(pred_label)
                            break
                    if pred_label is None:
                        one_fail = dict(**{'prediction': output, 'error_type': "Unspecified dict key"}, **gold)
                        failed.append(one_fail)
                        pred_label = (-1) * gold['label'] + 1
                        #pred_labels.append((-1) * gold['label'] + 1)
                    else:
                        one_success = dict(**{'prediction': pred_label, 'extracted_output': output}, **gold)
                        if pred_label != gold['label']:
                            incorrect.append(one_success)
                        else:
                            correct.append(one_success)
                    if (pred_label_icannot == 1):
                        pred_label = pred_label_icannot
                        one_icannot = dict(**{'prediction': pred_label, 'extracted_output': output}, **gold)
                        if (gold['label'] == 1):
                            icannot_statistics['align'].append(one_icannot)
                        else:
                            icannot_statistics['notalign'].append(one_icannot)
                #assert pred_label is not None
                pred_labels.append(pred_label)
            for tag, item in icannot_statistics.items():
                if (len(item) > 0):
                    summary[f'n_icannot_{tag}'] = len(item)
        # Metric result
        if self.task == 'fhm':
            gt_labels = gt_labels_all['seen'] + gt_labels_all['unseen']
            pred_labels = pred_labels_all['seen'] + pred_labels_all['unseen']
            #print(len(pred_labels))

        summary['acc'] = round(accuracy_score(gt_labels, pred_labels),4)
        summary['f1'] = round(f1_score(gt_labels, pred_labels, average = 'macro'),4)
        summary['precision'] = round(precision_score(gt_labels, pred_labels, average= 'macro', zero_division=0.), 4)
        summary['recall'] = round(recall_score(gt_labels, pred_labels, average= 'macro'), 4)
        summary['recall_pos'] = round(recall_score(gt_labels, pred_labels, average= 'binary', pos_label=1), 4)
        summary['recall_neg'] = round(recall_score(gt_labels, pred_labels, average= 'binary', pos_label=0), 4)
        summary['precision_pos'] = round(precision_score(gt_labels, pred_labels, average= 'binary', pos_label=1), 4)
        summary['precision_neg'] = round(precision_score(gt_labels, pred_labels, average= 'binary', pos_label=0), 4)
        summary['balanced_acc'] = round(balanced_accuracy_score(gt_labels, pred_labels), 4)
        summary['roc_auc'] = round(roc_auc_score(gt_labels, pred_labels), 4)
        summary_report = copy.deepcopy(summary)
        
        if self.task == 'fhm':
            if args.split == 'test':
                for item in failed:
                    if item['is_seen']:
                        n_failed_['seen'] += 1
                    else:
                        n_failed_['unseen'] += 1
                for split in ['seen', 'unseen']:
                    summary[f'n_failed_{split}'] = n_failed_[split]
                    pred, gt = pred_labels_all[split], gt_labels_all[split]
                    if pred and gt:
                        summary[f"acc_{split}"] = round(accuracy_score(gt, pred),4)
                        summary[f'f1_{split}'] = round(f1_score(gt, pred, average = 'macro'),4)
                        summary[f'precision_{split}'] = round(precision_score(gt, pred, average= 'macro', zero_division=0.), 4)
                        summary[f'recall_{split}'] = round(recall_score(gt, pred, average= 'macro'), 4)
                        summary[f'balanced_acc_{split}'] = round(balanced_accuracy_score(gt, pred), 4)
                        summary[f'roc_auc_{split}'] = round(roc_auc_score(gt, pred), 4)
                        summary[f'recall_pos_{split}'] = round(recall_score(gt, pred, average= 'binary', pos_label=1), 4)
                        summary[f'recall_neg_{split}'] = round(recall_score(gt, pred, average= 'binary', pos_label=0), 4)
                        summary[f'precision_pos_{split}'] = round(precision_score(gt, pred, average= 'binary', pos_label=1), 4)
                        summary[f'precision_neg_{split}'] = round(precision_score(gt, pred, average= 'binary', pos_label=0), 4)
        
        # For result aggregation
        summary['n_failed'] = len(failed) 
        summary['task'] = self.task
        summary['llm'] = self.args.llm
        summary['lmm'] = self.args.lmm
        summary['scheme'] = args.scheme
        summary['llm_max_new_tokens'] = self.args.llm_max_new_tokens
        summary['lmm_max_new_tokens'] = self.args.lmm_max_new_tokens    
        summary_print = pprint.pformat(summary)
        
        sep_asterisk = "*" * 10
        newline = "\n"
        badge_metric = f"{newline}{sep_asterisk}report metrics{sep_asterisk}{newline}"
        badge_creport = f"{newline}{sep_asterisk}classification report{sep_asterisk}{newline}"
        badge_cm = f"{newline}{sep_asterisk}confusion matrix{sep_asterisk}{newline}"
        tmp = self.output_dir.split("/")[-1].split("_")
        if len(tmp) > 1:
            tmp = "_".join([tmp[0], tmp[1]])
        else:
            tmp = tmp[0]
        print(self.output_dir)
        log_message = [f"\nResults for: {tmp}"]
        if (args.local_rank <= 0) and (not args.do_not_save_results): # 
            if args.decision_model_type == 'finetune':
                if epoch is not None:
                    self.output_dir = os.path.join(self.output_dir, section+'_', 'epoch_' + str(int(epoch)))
                else:
                    self.output_dir = os.path.join(self.output_dir, section)
                os.makedirs(self.output_dir, exist_ok=True)

            gen_file_names = ['failed', 'incorrect', 'correct', 'result']
            for f_name, f_obj in zip(gen_file_names, [failed, incorrect, correct, summary]):
                f_name = f"{f_name}{args.target_result_surfix}.json"
                with open(os.path.join(self.output_dir, f_name), "w") as f:
                    json.dump(f_obj,f,indent=4,)
                    f.close()
            log_message.append(f'{badge_metric}{summary_print}\n#total:{len(preds)}\n#failed examples:{len(failed)}{badge_metric}')
            # logger.info()
        
        if (not args.do_not_save_results):
            classification_rpt = classification_report(gt_labels, pred_labels, target_names=['non-hateful', 'hateful'], zero_division=0., digits=4)
            conf_matrix = confusion_matrix(gt_labels, pred_labels, labels=[0,1])
            if args.local_rank <= 0:
                log_message.append(badge_creport + classification_rpt)
                log_message.append(badge_cm)
                # logger.info(badge_creport + classification_rpt)
                # logger.info(badge_cm)
                log_message = "\n".join(log_message)
                logger.info(log_message)
                logger.info(conf_matrix)
        
        return summary_report
