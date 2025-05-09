#!/usr/bin/env python
# -*- coding: utf-8 -*-
# encoding=utf8
import numpy as np
import utils.tool
from utils.configure import Configure
from collections.abc import Mapping

class EvaluateTool(object):
    """
    The meta evaluator
    """
    def __init__(self, args):
        self.args = args

    def evaluate(self, preds, golds, section, epoch=None):
        args = self.args
        summary = {}
        wait_for_eval = {}
        for pred, gold in zip(preds, golds):
            if gold['task'] not in wait_for_eval.keys():
                wait_for_eval[gold['task']] = {'preds': [], "golds":[]}
            wait_for_eval[gold['task']]['preds'].append(pred)
            wait_for_eval[gold['task']]['golds'].append(gold)
        for task, preds_golds in wait_for_eval.items():
            args.current_eval_task = task
            evaluator = utils.tool.get_evaluator(args.config.evaluate.task_evaluator)(args)
            summary_tmp = evaluator.evaluate(preds_golds['preds'], preds_golds['golds'], section, epoch)
            for key, metric in summary_tmp.items():  # TODO
                summary[f'{task}:{key}'] = metric
        all_metrics, all_f1, all_acc = [], [], []
        for k, v in summary.items():
            if k.split(":")[1] == 'f1':
                all_f1.append(float(v))
            elif k.split(":")[1] == 'acc':
                all_acc.append(float(v))
            all_metrics.append(float(v))
        summary['avr_f1'] = float(np.mean(all_f1))
        summary['avr_acc'] = float(np.mean(all_acc))
        summary['avr'] = float(np.mean(all_metrics))
        return summary
