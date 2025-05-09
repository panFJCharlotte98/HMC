import copy
import os
import torch
from datasets import DatasetDict
from torch.utils.data import Dataset
from tqdm import tqdm
from utils.prompt_templates.fhm import prompt_fhm
from utils.prompt_templates.harmc import prompt_harmc
from utils.prompt_templates.harmp import prompt_harmp
from utils.prompt_templates.mami import prompt_mami
from utils.prompt_templates.multioff import prompt_multioff
from utils.prompt_templates.pridemm import prompt_pridemm
from utils.prompt_templates.goatbench import prompt_goatbench

class Constructor(object):
    def __init__(self, dataset_name, global_args):
        self.dataset_name = dataset_name
        self.global_args = global_args
        
    def to_seq2seq(self, raw_datasets: DatasetDict, model_tag):
        """
        We do not do cache right here but cache after the datasets have been tokenized.
        Here we just format the input by adding prompts to each data instance.
        """
        train_dataset, dev_dataset, test_dataset = None, None, None
        if 'train' in raw_datasets:
            train_dataset = Seq2SeqDataset(self.dataset_name, model_tag, self.global_args, raw_datasets['train'])
        if 'dev' in raw_datasets:
            dev_dataset = Seq2SeqDataset(self.dataset_name, model_tag, self.global_args, raw_datasets['dev'])
        if 'test' in raw_datasets:
            test_dataset = Seq2SeqDataset(self.dataset_name, model_tag, self.global_args, raw_datasets['test'])

        return train_dataset, dev_dataset, test_dataset

class Seq2SeqDataset(Dataset):
    def __init__(self, dataset_name, model_tag, global_args, raw_datasets):
        self.args = global_args
        task = dataset_name

        if task == 'fhm':
            prompt_func = prompt_fhm
        elif task == 'harmc':
            prompt_func = prompt_harmc
        elif task == 'harmp':
            prompt_func = prompt_harmp
        elif task == 'mami':
            prompt_func = prompt_mami
        elif task == 'multioff':
            prompt_func = prompt_multioff
        elif task == 'pridemm':
            prompt_func = prompt_pridemm
        elif task in ["gb_hateful", "gb_harmful", "gb_misogynistic", "gb_offensive"]:
            prompt_func = prompt_goatbench
        
        self.raw_datasets = raw_datasets
        self.prompted_data = []
        expansion = global_args.config.task_seq2seq.expansion if global_args.config.task_seq2seq.expansion else 1
    
        for expand_id in range(expansion):
            for example in tqdm(self.raw_datasets):
                one_data = copy.deepcopy(example)
                p_example = prompt_func(global_args, model_tag, one_data)
                if p_example is not None:
                    self.prompted_data.append(p_example)

    def __getitem__(self, index):
        return self.prompted_data[index]

    def __len__(self):
        return len(self.prompted_data)
    
    # def update_data(self, new_data):
    #     self.prompted_data = new_data
    #     if self.args.local_rank <= 0:
    #         print('Seq2seq data updated.')

