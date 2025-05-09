#/data/fengjun/hf_downloaded_models llm/mllm

import os
import torch
import torch.nn as nn    
from transformers import (
    AutoConfig, AutoModelForCausalLM, AutoTokenizer,
    LlavaNextConfig, LlavaNextProcessor, LlavaNextForConditionalGeneration, AutoModelForImageTextToText,
    LlavaConfig, LlavaForConditionalGeneration,
    Qwen2VLConfig, AutoProcessor, Qwen2VLForConditionalGeneration, 
    # Qwen2_5_VLConfig, Qwen2_5_VLForConditionalGeneration,
    MllamaConfig, MllamaForConditionalGeneration,
    LlamaConfig, LlamaForCausalLM, LlamaTokenizer,
    BitsAndBytesConfig,
    T5Config, T5ForConditionalGeneration, T5Tokenizer,
    LlamaTokenizerFast
)
from utils.configure import Configure

DEFAULT_MODEL_CACHE = "/data/fengjun/hf_downloaded_models"
LLMs = ['llama3.1', 'qwen2.5']
LMMs = ['llama3.2', 'qwen2-vl', 'qwen2.5-vl', 'llava1.6', 'llava1.5']

MODEL_CLASSES = {
    # LLM
    'llama3.1': (AutoConfig, AutoModelForCausalLM, AutoTokenizer),
    'qwen2.5': (AutoConfig, AutoModelForCausalLM, AutoTokenizer),
    'mistral': (AutoConfig, AutoModelForCausalLM, AutoTokenizer),
    'llama2': (LlamaConfig, LlamaForCausalLM, LlamaTokenizer),
    # LMM
    'llava1.5': (LlavaConfig, LlavaForConditionalGeneration, AutoProcessor),
    'llava1.6': (LlavaNextConfig, AutoModelForImageTextToText, AutoProcessor),
    'qwen2-vl': (Qwen2VLConfig, Qwen2VLForConditionalGeneration, AutoProcessor),
    # 'qwen2.5-vl': (Qwen2_5_VLConfig, Qwen2_5_VLForConditionalGeneration, AutoProcessor),
    'llama3.2': (MllamaConfig, MllamaForConditionalGeneration, AutoProcessor),
    # PLM
    't5': (T5Config, T5ForConditionalGeneration, T5Tokenizer)
}

class Model(nn.Module):   
    def __init__(self, args):
        super(Model, self).__init__()
        type = args.current_model_type
        self.type = type
        self.name = args.current_model # llava1.6-7bf
        self.model_tag = "-".join(self.name.split("-")[:-1]).strip("-")
        self.model_size = int(self.name.split("-")[-1].strip('bf')) # as int
        model_size = self.name.split("-")[-1]
        if self.type == 'llm':
            assert self.model_tag in LLMs
            model_id = os.path.join(DEFAULT_MODEL_CACHE, 'llm', f"{self.model_tag}/{model_size}")
        if self.type == 'lmm':
            assert self.model_tag in LMMs
            model_id = os.path.join(DEFAULT_MODEL_CACHE, 'mllm', f"{self.model_tag}/{model_size}")

        # if type == 'llm':
        #     self.name = args.llm
        #     self.model_tag = "-".join(args.llm.split("-")[:-1]).strip("-")
        #     assert self.model_tag in LLMs
        #     self.model_size = int(args.llm.split("-")[-1].strip('bf')) # as int
        #     model_size = args.llm.split("-")[-1]
        #     model_id = os.path.join(DEFAULT_MODEL_CACHE, 'llm', f"{self.model_tag}/{model_size}")
        # if type == 'lmm':
        #     self.name = args.lmm
        #     self.model_tag = "-".join(args.lmm.split("-")[:-1]).strip("-")
        #     assert self.model_tag in LMMs
        #     self.model_size = int(args.lmm.split("-")[-1].strip('bf'))
        #     model_size = args.lmm.split("-")[-1]
        #     model_id = os.path.join(DEFAULT_MODEL_CACHE, 'mllm', f"{self.model_tag}/{model_size}")

        tokenizer_kwargs = {}
        config_class, model_class, tokenizer_class = MODEL_CLASSES[self.model_tag]
        config = config_class.from_pretrained(model_id, cache_dir=args.cache_dir if args.cache_dir else None)
        if type == 'llm':
            tokenizer = tokenizer_class.from_pretrained(model_id, **tokenizer_kwargs)
        if type == 'lmm':
            processor_kwargs = {}
            if self.model_tag.startswith('llava'):
                processor_kwargs = {
                    'patch_size': config.vision_config.patch_size,
                    'vision_feature_select_strategy': config.vision_feature_select_strategy
                }
            if self.model_tag.startswith('qwen2.5-vl'):
                processor_kwargs.update({'use_fast': False})
            processor = tokenizer_class.from_pretrained(model_id, **processor_kwargs)
        quantization_config = BitsAndBytesConfig(load_in_8bit = True if self.model_size >= 13 else False) #llm_int8_threshold=200.0
        # "device_map": accelerator.process_index; 'device_map': 'auto'
        kwargs = {'torch_dtype': torch.bfloat16, 'low_cpu_mem_usage':True} 
        #'quantization_config': quantization_config
        # if self.model_tag.startswith('qwen2.5'):
        #     kwargs = {'torch_dtype': torch.float32,'low_cpu_mem_usage':True} # OOM...
        if self.model_tag in ['qwen2-vl', 'qwen2.5-vl']:
            kwargs['config'] = config
        if type == 'llm':
            tokenizer.padding_side = "left"
            if not self.model_tag.startswith('qwen'):
                # 1. add a new pad token and resize, increase vocab size from 32K to 32K+1, need to resize the embeddings
                # tokenizer.add_special_tokens({"pad_token": "<PAD>"})
                # tokenizer.add_special_tokens({"pad_token":"<pad>"})
                # 2. more common practice
                tokenizer.pad_token = tokenizer.bos_token
            
        model = model_class.from_pretrained(model_id, **kwargs)
        # 1. add a new pad token and resize, increase vocab size from 32K to 32K+1, need to resize the embeddings
        # if (type == 'llm') and (not self.model_tag.startswith('qwen')):
        #     model.resize_token_embeddings(len(tokenizer))

        if type == 'lmm':
            if self.model_tag != 'llama3.2':
                processor.tokenizer.padding_side = "left"
            if self.model_tag.startswith('llava'):
                processor.patch_size = model.config.vision_config.patch_size
                processor.vision_feature_select_strategy = model.config.vision_feature_select_strategy
                #processor.tokenizer.pad_token = processor.tokenizer.eos_token
        
        #model.resize_token_embeddings(len(tokenizer))
        self.model = model
        self.config = config
        self.args = args
        if type == 'llm':
            self.tokenizer = tokenizer
            self.model.config.pad_token_id = tokenizer.pad_token_id
            self.model.generation_config.pad_token_id = tokenizer.pad_token_id
            # print(f"tokenizer bos token id = {tokenizer.bos_token_id}")
            # print(f"tokenizer eos token id = {tokenizer.eos_token_id}")
            # print(f"tokenizer pad token id = {tokenizer.pad_token_id}")
        if type == 'lmm':
            self.processor = processor
            self.model.generation_config.pad_token_id = processor.tokenizer.pad_token_id
            # print(f"tokenizer bos token id = {processor.tokenizer.bos_token_id}")
            # print(f"tokenizer eos token id = {processor.tokenizer.eos_token_id}")
            # print(f"tokenizer pad token id = {processor.tokenizer.pad_token_id}")
        self.model.eval()
        
        # Set up inference generation kwargs
        self.setup_gen_kwargs(args)
        if args.local_rank <= 0:
            print(f"{self.model_tag} model from {model_id} loaded and intialized successfully...")

    def setup_gen_kwargs(self, args):
        self.args = args
        if self.type == 'llm':
            if self.model_tag.startswith("qwen2.5"):
                print(f"max_new_tokens for {self.model_tag}: {args.llm_max_new_tokens}")
                if args.do_sample:
                    self.gen_kwargs = {
                        "max_new_tokens": args.llm_max_new_tokens,
                        "do_sample" : args.do_sample,
                        "temperature": args.temperature,
                        "top_p": args.top_p,
                    }
                else:
                    self.gen_kwargs = {
                        "max_new_tokens": args.llm_max_new_tokens,
                    }
            if self.model_tag.startswith("llama3"):
                terminators = [
                    self.tokenizer.eos_token_id,
                    self.tokenizer.convert_tokens_to_ids("<|eot_id|>")
                ]
                self.gen_kwargs = {
                    "max_new_tokens": args.llm_max_new_tokens,
                    "eos_token_id": terminators,
                    "do_sample" : args.do_sample,
                    "top_p": args.top_p,
                    "temperature": args.temperature,
                }
            if self.model_tag.startswith("mistral"):
                self.gen_kwargs = {
                    "max_new_tokens": args.llm_max_new_tokens,
                    "do_sample" : args.do_sample,
                }
            if self.model_tag.startswith("llama2"):
                self.gen_kwargs = {
                    "max_new_tokens": self.args.llm_max_new_tokens,
                    "do_sample" : self.args.do_sample,
                    "top_p": self.args.top_p,
                    "temperature": self.args.temperature,
                    "use_cache": self.args.use_cache,
                    "top_k" : self.args.top_k,
                    "repetition_penalty": self.args.repetition_penalty,
                    "length_penalty": self.args.length_penalty,
                    "pad_token_id": self.model.tokenizer.pad_token_id
                }
        if self.type == 'lmm':
            if self.model_tag in ['llava1.6', 'qwen2-vl', 'qwen2.5-vl', 'llama3.2', 'llava1.5']:
                if args.do_sample:
                    self.gen_kwargs = {
                        "max_new_tokens": args.lmm_max_new_tokens,
                        "do_sample" : args.do_sample,
                        "temperature": args.temperature,
                        "top_p": args.top_p,
                    }
                else:
                    # VLMs smaller than 13B with do_sample=False by default when args.use_greedy_decoding_for_mini_models= True
                    self.gen_kwargs = {
                        "max_new_tokens": args.lmm_max_new_tokens,
                    }

    def forward(
        self, 
        input_ids, 
        attention_mask, 
        labels, 
    ):
        loss = self.model(
            input_ids=input_ids,
            attention_mask=attention_mask,
            labels=labels,
            use_cache=False,
        ).loss
        return {'loss': loss}


