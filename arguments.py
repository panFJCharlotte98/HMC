from dataclasses import dataclass, field
from typing import Optional, Literal
from transformers import TrainingArguments

@dataclass
class WrappedTrainingArguments(TrainingArguments):
    cfg: str = None
    # --------------------- meta args ---------------------- #
    # llm: Literal['llama3.1', 'qwen2.5-7bf', 'qwen2.5-14bf'] = 'llama3.1'
    # lmm: Literal['llava1.6', 'llama3.2', 'qwen2-vl'] = 'llava1.6'
    llm: str = field(
        default=None, 
        metadata={"help": "what llm to run. (avail: 'llama3.1-8bf', 'qwen2.5-7bf', 'qwen2.5-14bf')", 
                  }
    )
    lmm: str = field(
        default='llava1.6-7bf,qwen2-vl-7bf', 
        metadata={"help": "what lmm to run. (avail: 'llava1.5-7bf', 'llava1.5-13bf', 'llava1.6-7bf', 'llava1.6-8bf', 'llava1.6-13bf', 'llama3.2-11bf', 'qwen2-vl-7bf', 'qwen2.5-vl-7bf')", 
        }
    )
    which_task : str = field(
        default="all", 
        metadata={"help":"what tasks (datasets) to run.",}
    )
    split: str = field(
        default="test", 
        metadata={"help":"which dataset split to run inference on",
                  "choices" : ['train', 'dev', 'test']}
    )
    load_data_surfix : str = field(
        default="-", 
        metadata={"help":"local dataset file surfix",
                  "choices" : ["-", 'toy', 'seen', 'unseen', 'seen_ffc', 'unseen_ffc']}
    )
    scheme : str = field(
        default="S1", 
        metadata={"help":"prompt scheme, the selected prompt formats",}
    )
    use_resized_img : Optional[bool] = field(
        default=False, 
        metadata={"help": ""}
    )
    use_greedy_decoding_for_mini_models : Optional[bool] = field(
        default=False, 
        metadata={"help": ""}
    )
    run_fewshot : Optional[bool] = field(
        default=False, 
        metadata={"help": "whether to run few-shot experiments."}
    )
    run_multiprompt : Optional[bool] = field(
        default=False, 
        metadata={"help": "whether to run multiple prompts consecutively."}
    )
    include_chat_history : Optional[bool] = field(
        default=False, 
        metadata={"help": "whether to include previous chat history to allow for multi-turn chat when running multiple prompts consecutively."}
    )
    use_mask_img : Optional[bool] = field(
        default=False, 
        metadata={"help": ""}
    )
    use_dataset_cache: bool = field(
        default=False, 
        metadata={"help":"use cached dataset."}
    )
    n_fewshots: int = field(
        default=1, 
        metadata={"help":"N-way K-shot examples to prompt LLMs for few-shot experiments. K examples for each of the N classes."}
    )
    load_weights_from: Optional[str] = field(
        default=None, 
        metadata={"help": "The directory to load the model weights from."}
    )
    do_not_save_results: Optional[bool] = field(
        default=False, 
        metadata={"help": ""}
    )
    
    quantization:Optional[bool] = field(
        default=True, 
        metadata={"help":"whehter to load quantized model."}
    ) 
    
    # --------------------- Generation-specific args ---------------------- #
    ### Parameters that control the length of the output
    llm_max_new_tokens: Optional[int] = field(
        default=256, 
        metadata={"help":"The maximum numbers of tokens to generate"}
    )
    lmm_max_new_tokens: Optional[int] = field(
        default=256, 
        metadata={"help":"The maximum numbers of tokens to generate"}
    )
    use_cache: Optional[bool] = field(
        default=True, 
        metadata={"help": "[optional] Whether or not the model should use the past last key/values attentions Whether or not the model should use the past last key/values attentions (if applicable to the model) to speed up decoding."}
    )
    ### Parameters for manipulation of the model output logits
    do_sample: Optional[bool] = field(
        default=False, 
        metadata={"help": "Whether or not to use sampling; If set to False, use greedy decoding otherwise."}
    )
    top_p: Optional[float] = field(
        default=1.0, 
        metadata={"help": "[optional] If set to float < 1, only the smallest set of most probable tokens with probabilities that add up to top_p or higher are kept for generation. When decoding text, samples from the top p percentage of most likely tokens; lower to ignore less likely tokens."}
    )
    temperature: Optional[float] = field(
        default=1.0, 
        metadata={"help": "[optional] The value used to modulate the next token probabilities. Adjusts randomness of outputs, greater than 1 is random and 0 is deterministic, 0.75 is a good starting value."}
    )
    top_k : Optional[int] = field(
        default=50, 
        metadata={"help": "[optional] The number of highest probability vocabulary tokens to keep for top-k-filtering. When decoding text, samples from the top k most likely tokens; lower to ignore less likely tokens"}
    )
    repetition_penalty: Optional[float] = field(
        default=1.0, 
        metadata={"help": "The parameter for repetition penalty. 1.0 means no penalty."}
    )
    length_penalty: Optional[int] = field(
        default=1.0, 
        metadata={"help": "[optional] Exponential penalty to the length that is used with beam-based generation."}
    )
    # --------------------- Other args ---------------------- #
    cache_dir: Optional[str] = field(
        default="",
        metadata={"help": "Optional directory to store the pre-trained models downloaded from s3 (instread of the default one)"},
    )
    regen_results : Optional[bool] = field(
        default=False, 
        metadata={"help": ""}
    )
    target_result_surfix : Optional[str] = field(
        default="", 
        metadata={"help": ""}
    )
