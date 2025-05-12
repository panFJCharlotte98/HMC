# Copyright (c) Meta Platforms, Inc. and affiliates.
# This software may be used and distributed according to the terms of the Llama 2 Community License Agreement.

import json
import numpy as np
from typing import List, Literal, TypedDict
from transformers.tokenization_utils_base import PreTrainedTokenizerBase


Role = Literal["user", "assistant", "system"]

class Message(TypedDict):
    role: Role
    content: str

Dialog = List[Message]

B_INST, E_INST = "[INST]", "[/INST]"
B_SYS, E_SYS = "<<SYS>>\n", "\n<</SYS>>\n\n"

def mistral_format_prompt(dialog, tokenizer):
    # split the system prompt as one round of user-assitant conversation
    assert dialog[0]['role'] == 'system'
    chat_history = dialog[1:]
    # sys_instructions = dialog[0]['content'].split('\n')
    # new_sys_inst = '\n'.join([sys_instructions[0].replace("You are", "I will be"),
    #            sys_instructions[1].replace("Please ensure that your responses are", "I will give responses that are"),
    #            sys_instructions[2].replace("Your response should", "My response will"),
    #            "I will always " + sys_instructions[3].replace("Answer", "answer"),
    #            ])
    # pseudo_system = [
    #     {"role": "user", "content": "Hi, I'm User. In the following conversations, you should take the role as a fallacy detection expert."},
    #     {"role": "assistant", "content": "Hi, User! Sure, in the following conversations, " + new_sys_inst}
    # ]
    # dialog = pseudo_system + chat_history

    dialog = chat_history
    
    dialog_tokens = tokenizer.apply_chat_template(
        dialog,
        return_tensors="np",
        add_generation_prompt=True,
    )[0].tolist()

    return dialog_tokens

def qwen2_format_prompt(dialog, tokenizer):
    assert dialog[0]['role'] == 'system'
    formatted_dialog = tokenizer.apply_chat_template(
        dialog,
        tokenize=False,
        add_generation_prompt=True
    )
    model_inputs = tokenizer([formatted_dialog], return_tensors="np")
    
    dialog_tokens = model_inputs.input_ids.tolist()[0]
    
    attention_mask = model_inputs.attention_mask.tolist()[0]
    
    return (dialog_tokens, attention_mask)

def qwen3_format_prompt(args, dialog, tokenizer):
    assert dialog[0]['role'] == 'system'
    formatted_dialog = tokenizer.apply_chat_template(
        dialog,
        tokenize=False,
        add_generation_prompt=True,
        enable_thinking=args.enable_thinking
    )
    model_inputs = tokenizer([formatted_dialog], return_tensors="np")
    
    dialog_tokens = model_inputs.input_ids.tolist()[0]
    
    attention_mask = model_inputs.attention_mask.tolist()[0]
    
    return (dialog_tokens, attention_mask)

def llama2_format_prompt(dialog, tokenizer):
    if dialog[0]["role"] == "system":
        dialog = [
        {
            "role": dialog[1]["role"],
            "content": B_SYS
            + dialog[0]["content"]
            + E_SYS
            + dialog[1]["content"],
        }
    ] + dialog[2:]
    assert all([msg["role"] == "user" for msg in dialog[::2]]) and all(
        [msg["role"] == "assistant" for msg in dialog[1::2]]
    ), (
        "model only supports 'system','user' and 'assistant' roles, "
        "starting with user and alternating (u/a/u/a/u...)"
    )
    """
    Please verify that your tokenizer support adding "[INST]", "[/INST]" to your inputs.
    Here, we are adding it manually.
    """
    dialog_tokens: List[int] = sum(
        [
            tokenizer.encode(
                f"{B_INST} {(prompt['content']).strip()} {E_INST} {(answer['content']).strip()} ",
                # max_length=args.max_input_length, 
                # padding='max_length',
            )
            for prompt, answer in zip(dialog[::2], dialog[1::2])
        ],
        [],
    )
    assert (
        dialog[-1]["role"] == "user"
    ), f"Last message must be from user, got {dialog[-1]['role']}"
    dialog_tokens += tokenizer.encode(
        f"{B_INST} {(dialog[-1]['content']).strip()} {E_INST}",
        # max_length=args.max_input_length, 
        # padding='max_length',
    )
    #assert dialog_tokens[-1] == 2
    return dialog_tokens

def llama3_format_prompt(dialog, tokenizer):
    # # Copied from llama3 github repo
    # def encode_header(message: Message) -> List[int]:
    #     tokens = []
    #     tokens.extend(tokenizer.encode("<|start_header_id|>"))
    #     tokens.extend(tokenizer.encode(message["role"])) #bos=False, eos=False
    #     tokens.extend(tokenizer.encode("<|end_header_id|>"))
    #     tokens.extend(tokenizer.encode("\n\n")) #bos=False, eos=False
    #     return tokens

    # def encode_message(message: Message) -> List[int]:
    #     tokens = encode_header(message)
    #     tokens.extend(
    #         tokenizer.encode(message["content"].strip()) #bos=False, eos=False
    #     )
    #     tokens.extend(tokenizer.encode("<|eot_id|>"))
    #     return tokens
    
    # dialog_tokens = []
    # dialog_tokens.extend(tokenizer.encode("<|begin_of_text|>"))
    # for message in dialog:
    #     dialog_tokens.extend(encode_message(message))
    # # Add the start of an assistant message for the model to complete.
    # dialog_tokens.extend(encode_header({"role": "assistant", "content": ""}))
    
    # Or, use transformers tokenizer apply chat template https://huggingface.co/meta-llama/Meta-Llama-3-8B-Instruct
    dialog_tokens = tokenizer.apply_chat_template(
        dialog,
        add_generation_prompt=True,
        return_tensors="np"
    )[0].tolist()
    return dialog_tokens

def LLM_format_prompt(args, model_tag, dialog, tokenizer):
    """
    1. Format input prompts by adding special tokens;
    2. Encode tokens to vocab ids.
    """
    if model_tag.startswith('llama2'):
        return llama2_format_prompt(dialog, tokenizer)
    
    if model_tag.startswith('llama3'): 
        return llama3_format_prompt(dialog, tokenizer)

    if model_tag.startswith('mistral'): 
        return mistral_format_prompt(dialog, tokenizer)
    
    if model_tag.startswith('qwen'):
        if model_tag.startswith('qwen3'):
            return qwen3_format_prompt(args, dialog, tokenizer)
        return qwen2_format_prompt(dialog, tokenizer)

def LMM_format_prompt(processor, dialog, image_paths=None):
    # Template simply formats your prompt, you still have to tokenize it and obtain pixel values for your images
    format_prompt = processor.apply_chat_template(dialog, add_generation_prompt=True)
    return {'text': format_prompt, 'img_paths': image_paths}
    



