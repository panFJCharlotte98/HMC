from utils.knowledge.mami import *
from utils.tool import *

from_raw_data = '{from_raw_data}'
from_dependency = '{from_dependency}'
from_previous_turn = '{from_previous_turn}'
# --------------------------- For Multimodal LMMs --------------------#
VLREASONING = {
    'name': "VLReasoning", 'should_evaluate': False, 'take_image': True,
    'gen_depend_on': None,
    'versions': {
        'CoT': {
            "INS": f'''Classify this meme as either misogynistic or non-misogynistic based on widely accepted values, social norms, and the established understanding of harmful stereotypes, biases, and discriminatory narratives. Now, let's analyze step by step:'''
        },
    },
    'output_format': {
        'v0': {"INS": '''''', 'post_process_func': post_process_to_remove_gibberish},
    },
}

DESCRIBE = {
    'name': "Describe",
    'should_evaluate': False,
    'take_image': True,
    'gen_depend_on': None,
    'versions': {
        'v0': {"INS" : f'''The overlaid text on the image reads: "{from_raw_data}". Question: What is shown in the image? Describe within three sentences. DO NOT assume the nature of the image's tone or intent as humorous, comical, playful or lighthearted in your description.'''},
    },
    'output_format': {
        'v0': {"INS": "", 'post_process_func': False},
    }
}

check_dependency = '''{check_dependency}'''
HUMAN = {
    'name': "Human", 'should_evaluate': False, 'take_image': True, 'gen_depend_on': None,
    'versions': {
        'v0': {"INS" : '''Is there any human subject in the given image? Ignore any overlaid text or caption.'''},
    },
    'output_format': {
        'v0': {"INS": '''Start your response with "Yes," or "No," before giving any further explanation.''', 'post_process_func': extract_yes_or_no}
    }
}

Ignore = '''Ignore any overlaid text or caption in the image.'''
check_if_no_human_dependency = '''{check_if_no_human_dependency}'''
GENITAL = {
    'name': "Genital", 'should_evaluate': False, 'take_image': True, 'gen_depend_on': [HUMAN['name']],
    'versions': {
        'f': {"INS" : f'''{check_if_no_human_dependency}Ignore any overlaid text or caption in the image. Are there any visual elements in the image that apparently resemble the shape of a female vagina?'''},
        'm': {"INS" : f'''{check_if_no_human_dependency}Ignore any overlaid text or caption in the image. Are there any visual elements in the image that apparently resemble the shape of a male's genital like penis?'''},
    },
    'output_format': {
        'v0': {"INS": '''Start your response with "Yes," or "No," before giving further explanation.''', 'post_process_func': extract_yes_or_no},
    }
}

GENDER = {
    'name': "Gender", 'should_evaluate': False, 'take_image': True, 'gen_depend_on': [HUMAN['name']],
    'versions': {
        'v0': {"INS" : f'''{check_dependency}{Ignore} What is/are the gender(s) of the human subject(s) in the image?'''}
    },
    'output_format': {
        'v0': {"INS": '''''', 'post_process_func': False},
    }
}

SEX = {
    'name': "Sex", 'should_evaluate': False, 'take_image': True, 'gen_depend_on': [HUMAN['name']],
    'versions': {
        'v0': {"INS" : f'''{check_dependency}Does the image's visual content contain adult content? {Ignore}'''},
    },
    'output_format': {
        'v0': {"INS": '''Start your response with "Yes," or "No," before giving further explanation.''', 'post_process_func': extract_yes_or_no},
    }
}

FEMALE = {
    'name': "Female", 'should_evaluate': False, 'take_image': True, 'gen_depend_on': [HUMAN['name']],
    'versions': {
        'v0': {"INS" : f'''{check_dependency}{Ignore} Is/Are there any human subject(s) in the image female?'''}
    },
    'output_format': {
        'v0': {"INS": '''Start your response with "Yes," or "No," before giving further explanation.''', 'post_process_func': extract_yes_or_no},
    }
}

FEMALE_SEXUAL = {
    'name': "Sexual", 'should_evaluate': False, 'take_image': True, 'gen_depend_on': [FEMALE['name']],
    'versions': {
        'sexy': {"INS" : f'''{check_dependency}Does the image's visual content highlight the sexiness of the female's figure in a way that is sexually provocative? {Ignore}'''},
        'body': {"INS" : f'''{check_dependency}{Ignore} Does this image highlight sexual body parts of the female subject(s), such as the breast, the hip/buttock, or the genital?'''},
        'fat': {"INS" : f'''{check_dependency}{Ignore} Does/Do the female subject(s) in the image appear to be overweight?'''},
        'fat1': {"INS" : f'''{check_dependency}{Ignore} Does/Do the female subject(s) in the image appear to be of large body size (considered as fat)?'''},
    },
    'output_format': {
        'v0': {"INS": '''Start your response with "Yes," or "No," before giving any further explanation.''', 'post_process_func': extract_yes_or_no},
    }
}

APPEARANCE = {
    'name': "Appearance", 'should_evaluate': False, 'take_image': True, 'gen_depend_on': [FEMALE['name']],
    'versions': {
        'v0': {"INS" : f'''{check_dependency}{Ignore} What are the distinctive physical appearance characteristics of the female subject(s) in the image?'''},
    },
    'output_format': {
        'v0': {"INS": '''''', 'post_process_func': False},
    }
}

# --------------------------- For Unimodal LLMs --------------------#
UNIFY_SYS = '''You are a helpful assistant.''' #'''You are an expert in meme content comprehension and hatefulness detection.'''
INTEGRATE = {
    'name': "Integrate", 'should_evaluate': False, 'take_image': False, 'gen_depend_on': [HUMAN['name'], GENDER['name'], SEX['name'], FEMALE['name'], FEMALE_SEXUAL['name'], APPEARANCE['name'], DESCRIBE['name']],
    'versions': {
        'v1': {
            "INS": f'''Given the following information provided about an image, and disregarding any information about overlaid text or captions, synthesize and rephrase these information into a unified, comprehensive description of the image content. DO NOT ASSUME the nature of the image's tone and intent as humorous, comical, playful or lighthearted in the description. Information: "{from_dependency}"'''
        },
    },
    'output_format': {
        'v0': {"INS": '''''', 'post_process_func': post_process_to_remove_gibberish},
    }
}

# # Reasoning
from_Integrate = "{from_Integrate}"
REASONING_STAGE1 = {}
for t_abbr, t_dict in STAGE1_GL.items():
    type_name, type_gl = t_dict['type'].lower(), t_dict['guideline']
    REASONING_STAGE1[t_abbr] = {
        'gen_depend_on': [INTEGRATE['name']],
        'INS': [
            f'''Given the following image-caption content, which may or may not be an online meme,''',
            '''classify the content as either misogynistic or non-misogynistic based on common values, knowledge, social norms and the provided guidelines.''',
            f'''Guidelines: {type_gl}''',
            f'''**Image-caption content you need to classify**: {from_Integrate}''',
            f'''The caption overlaid on the image reads "{from_raw_data}".''',
            '''Now, let's analyze by applying all the guidelines one by one:'''
        ],
}

from_Integrate_after_check = '''{from_Integrate_after_check}'''
from_raw_data_after_check = '''{from_raw_data_after_check}'''
check_stage1_pred_cls = '''{check_stage1_pred_cls}'''
REASONING_STAGE2 = {}
for t_abbr, t_dict in STAGE2_GL.items():
    type_gl = t_dict['guideline']
    REASONING_STAGE2[t_abbr+"*"] = {
        'gen_depend_on': [INTEGRATE['name']],
        'INS': f'''{check_stage1_pred_cls}Given the following image-caption content, which may or may not be an online meme, classify the content as either misogynistic or non-misogynistic based on common values, knowledge, social norms and the provided guidelines. Guidelines: {type_gl}\n**Image-caption content you need to classify**: {from_Integrate_after_check} The caption overlaid on the image reads "{from_raw_data_after_check}". Now, let's analyze by applying all the guidelines one by one:''',
    }

REASONING_BASELINE = {
    'CoT': {
        'gen_depend_on': [INTEGRATE['name']],
        'INS': [
            f'''Given the following image-caption content, which may or may not be an online meme, classify the content as either misogynistic or non-misogynistic based on common values, knowledge and social norms.''',
            f'''**Image-caption content you need to classify**: {from_Integrate}''',
            f'''The caption overlaid on the image reads "{from_raw_data}".''',
            '''Now, let's analyze step by step:'''
        ]
    },
}

REASONING_VERS = dict(**REASONING_BASELINE, **REASONING_STAGE1, **REASONING_STAGE2)
REASONING = {
    'name': "Reasoning", 'should_evaluate': False, 'take_image': False,
    'versions': REASONING_VERS,
    'output_format': {
        'v0': {"INS": '''''', 'post_process_func': post_process_to_remove_gibberish},##########################
    }
}

# # Step Decision
STEP_DECISION_STAGE1 = {}
for t_abbr, t_dict in STAGE1_GL.items():
    type_name = t_dict['type']
    STEP_DECISION_STAGE1[t_abbr] = {
        'should_evaluate': False,
        'gen_depend_on': None,
        'INS': f'''If you just found evidence that suggests {type_name.lower()}, output "Conclusion: Misogynistic ({type_name})." If you just classified the content as misogynistic based on other reasons, output "Conclusion: Misogynistic (reason_in_a_phrase)." Otherwise, just output "Conclusion: Non-misogynistic."'''
    }
STEP_DECISION_STAGE2 = {}
for t_abbr, _ in STAGE2_GL.items():
    STEP_DECISION_STAGE2[t_abbr+"*"] = {
        'should_evaluate': False,
        'gen_depend_on': None,
        'INS': f'''If you just classified the image-caption content as misogynistic, output "Conclusion: Misogynistic." Otherwise, output "Conclusion: Non-misogynistic."''',
    }
STEP_DECISION_STAGE1_OUTPUT_EXTRATOR = {}
for t_abbr, t_dict in STAGE1_GL.items():
    this_extractor = MAMI_Extractor(t_dict['type'])
    STEP_DECISION_STAGE1_OUTPUT_EXTRATOR[t_abbr] = {
        "INS": '''''', 'post_process_func': this_extractor.mami_extract_stage_decision_label
    }
STEP_DECISION_OUTPUT_ORI = {
    'v1': {"INS": '''''', 'post_process_func': mami_extract_stage_decision_label},
}
STEP_DECISION = {
    'name': "StepDecision", 'take_image': False,
    'versions': dict(**STEP_DECISION_STAGE1, **STEP_DECISION_STAGE2),
    'output_format': dict(**STEP_DECISION_OUTPUT_ORI, **STEP_DECISION_STAGE1_OUTPUT_EXTRATOR)
}

GPT_DIRECT_CLASSIFY = {
    'name': "Classify", 'should_evaluate': False, 'take_image': True, 'gen_depend_on': None,
    'versions': {
        'v1': {'INS': f'''Common forms of misogynistic content include harmful stereotypes about women, objectification of women, body shaming, and promoting violence against women. Based on this definition, is this meme considered misogynistic?'''},
        'v0': {'INS': f'''Classify this meme as either misogynistic or non-misogynistic.'''},
    },
    'output_format': {
        'v0': {"INS": '''''', 'post_process_func': post_process_to_remove_gibberish}
    },
}

GPT_DESCRIBE = {
    'name': "Describe", 'should_evaluate': False, 'take_image': True, 'gen_depend_on': None,
    'versions': {
        'v0': {'INS': f'''This is an online meme about women. Describe the visual content of the meme without interpretation. If there is any overlaid caption, transcribe it exactly as shown without paraphrasing.'''},
    },
    'output_format': {
        'v0': {"INS": '''''', 'post_process_func': post_process_to_remove_gibberish}
    },
}

DECISION = {
    'name': "Decision", 'should_evaluate': True, 'take_image': False,
    'versions': {
        'v0': {
            'gen_depend_on': None,
            'INS': f'''If you just classified the image-caption content as misogynistic, output "Conclusion: Misogynistic." Otherwise, output "Conclusion: Non-misogynistic."''',
        },
        'vl': {
            'gen_depend_on': None,
            'INS': f'''If you just classified the meme as misogynistic, output "Conclusion: Misogynistic." Otherwise, output "Conclusion: Non-misogynistic."''',
        },
        'gpt': {
            'gen_depend_on': [GPT_DIRECT_CLASSIFY['name']],
            'INS': f'''If you just classified the meme content as misogynistic, output "Conclusion: Misogynistic." Otherwise, output "Conclusion: Non-misogynistic."''',
            # 'INS': f'''If you just concluded that the meme content is misogynistic, output "Conclusion: Misogynistic." Otherwise, output "Conclusion: Non-misogynistic."''',
        }
    },
    'output_format': {
        'v0': {"INS": '''''', 'post_process_func': mami_extract_classification_label},
    }
}

# Multimodal baseline: Inference with LMM directly
B1 = {
    'lmm': {
        'prompt': {
            0: {'template': VLREASONING, "version": "CoT", "out_format": 'v0'}, 
            1: {'template': DECISION, "version": "vl", "out_format": 'v0'},
        },
        'multi-turn': True
    },
}

GPT = {
    'lmm': {
        'prompt': {
            0: {'template': GPT_DIRECT_CLASSIFY, "version": "v1", "out_format": 'v0'},
        },
        'multi-turn': False
    },
    'llm': {
        'multi-turn': True,
        'prompt': {
            1: {'template': DECISION, "version": "gpt", "out_format": 'v0', 'batch_size':1},
        }
    }
}

GPT_describe = {
    'lmm': {
        'prompt': {
            0: {'template': GPT_DESCRIBE, "version": "v0", "out_format": 'v0'},
        },
        'multi-turn': False
    },
}

M2T = {
    'lmm': {
        'prompt': {
            0: {'template': HUMAN, "version": "v0", "out_format": 'v0'}, 
            1: {'template': GENDER, "version": "v0", "out_format": 'v0'},
            2: {'template': SEX, "version": "v0", "out_format": 'v0'},
            3: {'template': FEMALE, "version": "v0", "out_format": 'v0'},
            4: {'template': FEMALE_SEXUAL, "version": "sexy", "out_format": 'v0'},
            5: {'template': FEMALE_SEXUAL, "version": "body", "out_format": 'v0'},
            6: {'template': FEMALE_SEXUAL, "version": "fat", "out_format": 'v0'},
            7: {'template': FEMALE_SEXUAL, "version": "fat1", "out_format": 'v0'},
            8: {'template': APPEARANCE, "version": "v0", "out_format": 'v0'},
            9: {'template': DESCRIBE, "version": "v0", "out_format": 'v0'},
    },
    'multi-turn': False},
    'llm_1': {
        'prompt': {
            0: {'template': INTEGRATE, "version": "v1", "out_format": 'v0'},    
    },
    'multi-turn': False},
}

# *******************************************************************************************
b2 = {
    'llm_2': {
        'multi-turn': True,
        'prompt': {
            0: {'template': REASONING, "version": "CoT", "out_format": 'v0'},
            1: {'template': DECISION, "version": "v0", "out_format": 'v0'}
        }
    }
}
B2 = dict(**M2T, **b2)

# # Proposed Step-by-step pipeline
p1 = {}
llm_id = 2
for type_name, type_dict in TYPES_META.items():
    if 'Q_if_miso' in type_dict:
        p1[f"llm_{llm_id}"] = {
            'multi-turn': True,
            'prompt': {
                0: {'template': REASONING, "version": type_dict['abbr'], "out_format": 'v0'}, #'max_new_tokens': 512
                1: {'template': STEP_DECISION, "version": type_dict['abbr'], "out_format": type_dict['abbr']},
                2: {'template': REASONING, "version": type_dict['abbr']+"*", "out_format": 'v0', 'depend_on_prestep': True, 'new_conversation': True},
                3: {'template': STEP_DECISION, "version": type_dict['abbr']+"*", "out_format": 'v1'},
            }
        }
        llm_id += 1
for type_name, type_dict in TYPES_META.items():
    if 'Q_if_miso' not in type_dict:
        p1[f"llm_{llm_id}"] = {
            'multi-turn': True,
            'prompt': {
                0: {'template': REASONING, "version": type_dict['abbr'], "out_format": 'v0'}, #'max_new_tokens': 512
                1: {'template': STEP_DECISION, "version": type_dict['abbr'], "out_format": type_dict['abbr']}
            }
        }
        llm_id += 1
fid = llm_id - 1
p1[f"llm_{fid}"]['prompt'][1]['gather_step_decisions'] = True
final_step_version = p1[f"llm_{fid}"]['prompt'][1]["version"]
p1[f"llm_{fid}"]['prompt'][1]['template']['versions'][final_step_version]['gen_depend_on'] = [STEP_DECISION['name']]
p1[f"llm_{fid}"]['prompt'][1]['template']['versions'][final_step_version]['should_evaluate'] = True
PP = dict(**M2T, **p1)

# ******************************************************************************************* # 
MAMI_PROMPT_SCHEMES = {
    'M2T': M2T,
    'B1': B1,
    'B2': B2,
    'GPT': GPT,
    'PP': PP,
    'GPT_DESCRIBE': GPT_describe
}

def get_Integrate_dp_pred(js):
    dp_pred_key = 'processed_dependency_prediction'
    if dp_pred_key not in js:
        dp_pred_key = "processed_prediction"
    dp_pred = js.pop(dp_pred_key)
    assert isinstance(dp_pred, str)
    # Reinforce body shaming cues in image if there's any
    image_info_dict = js.pop("gathered_predictions")
    for info_type, info in image_info_dict.items():
        add_condition = info_type.strip("0123456789").endswith("-fat") or info_type.lower().startswith("sex-")
        if add_condition and (info is not None):
            dp_pred = " ".join([dp_pred, info])
    return dp_pred, js

def fill_placeholder(tmp, js):
    if from_raw_data in tmp:
        return tmp.format(from_raw_data = js['text'].strip('" ')), js
    if "_dependency}" in tmp:
        dp_pred_key = 'processed_dependency_prediction'
        if dp_pred_key not in js:
            dp_pred_key = "processed_prediction"
        if from_dependency in tmp:
            dp_pred = js.pop(dp_pred_key)
            assert isinstance(dp_pred, str)
            return tmp.format(from_dependency = dp_pred), js
        if check_dependency in tmp:
            dp_pred = js.pop(dp_pred_key)
            if isinstance(dp_pred, dict):
                if dp_pred['flag'] == 1:
                    return tmp.replace(check_dependency, ""), js
                else:
                    return "", None
        if check_if_no_human_dependency in tmp:
            dp_pred = js.pop(dp_pred_key)
            if isinstance(dp_pred, dict):
                if dp_pred['flag'] == 0:
                    return tmp.replace(check_if_no_human_dependency, ""), js
                else:
                    return "", None
    if from_Integrate in tmp:
        dp_pred, js = get_Integrate_dp_pred(js)
        return tmp.format(from_Integrate = dp_pred), js
    
    if check_stage1_pred_cls in tmp:
        stage1_pred_key = "processed_prediction"
        stage1_pred = js.pop(stage1_pred_key)
        assert isinstance(stage1_pred, dict)
        if stage1_pred['pred_label'] == 1:
            tmp = tmp.replace(check_stage1_pred_cls, "")
            if (from_Integrate_after_check in tmp) and (from_raw_data_after_check in tmp):
                dp_pred, js = get_Integrate_dp_pred(js)
                tmp = tmp.format(
                    from_raw_data_after_check = js['text'].strip('" '),
                    from_Integrate_after_check = dp_pred
                )
            return tmp, js
        else:
            return "", None
    return tmp, js

def format_chat(args, js):
    p_obj = args.current_prompt_meta['template']
    p_templates = args.current_prompt_meta['template']['versions']
    p_version = args.current_prompt_meta['version']
    prompt = p_templates[p_version]['INS'] 
    sys_pt = None
    if args.current_model_type == 'llm':
        sys_pt_ = p_templates[p_version]['SYS'] if 'SYS' in p_templates[p_version] else UNIFY_SYS
        if args.run_multiturn:
            sys_pt_ = UNIFY_SYS
        sys_pt = {"role": "system", "content": sys_pt_}
    take_image = p_obj['take_image']
    format_version = args.current_prompt_meta["out_format"]
    ins_output_format = p_obj['output_format'][format_version]['INS']
    img_history = []

    if isinstance(prompt, list):
        ins = []
        for item in prompt:
            item, js = fill_placeholder(item, js)
            ins.append(item)
        if ins_output_format:
            ins.append(ins_output_format)
        text_content = " ".join(ins)
    if isinstance(prompt, str):
        text_content, js = fill_placeholder(prompt, js)
        text_content = " ".join([text_content, ins_output_format]).strip()
    
    if js is not None:
        if args.current_model_type == 'llm':
            usr_pt = {"role": "user", "content": text_content}
        if args.current_model_type == 'lmm':
            #img_path = js['img_mask'] if args.use_mask_img else js['img']
            img_path = js['img']
            if take_image:
                content = [{"type": "image"}, {"type": "text", "text": text_content}]
                usr_pt = {"role": "user", "content": content}
                img_history.append(img_path)
            else:
                usr_pt = {"role": "user", "content": [{"type": "text", "text": text_content}]}
            
        dialog = [usr_pt]
        if (args.current_model_type == 'llm') and (sys_pt is not None):
            dialog = [sys_pt, usr_pt]
        if (args.run_multiturn) and (args.current_round > 0) and ('new_conversation' not in args.current_prompt_meta):
            pre_step_prediction = js.pop('prediction')
            if args.current_model_type == 'lmm':
                pre_step_prediction = [{"type": "text", "text": pre_step_prediction}]
                img_history = js['img_history'] + img_history
            
            # #---------------------------------------------------------
            if (args.current_model_type == 'llm') and (p_obj['name'] == "Decision") and (p_version == 'gpt'):
                # Convert multimodal inference to unimodal
                init_pt_text = ""
                for msg in js['chat_history']:
                    if msg["role"] == "user":
                        assert isinstance(msg["content"], list)
                        for info in msg["content"]:
                            if info["type"] == "text":
                                init_pt_text = info["text"].replace("meme", "meme content")
                init_pt = {"role": "user", "content": init_pt_text}
                js['chat_history'] = [sys_pt, init_pt] if sys_pt is not None else [init_pt]
            # #---------------------------------------------------------

            dialog = js['chat_history'] + [{"role" : "assistant", "content" : pre_step_prediction}] + [usr_pt]  
            if (args.current_prompt_meta['template']['name'] == 'Reasoning') and (args.current_prompt_meta['version'].endswith("*")):
                dialog = js['chat_history'][:-1] + [usr_pt]
        
        js['chat_history'] = dialog
        js['task'] = args.task
        js['img_history'] = img_history
    return js

def prompt_mami(args, model_tag, js):
    """
    input:
        js is one data sample in the format of dictionary
        js['text'] is a string of QA in a format like : "A: ....\nB: ..."
    """
    if model_tag.startswith('t5'):
        text = js['text'].lower()
    else:
        js = format_chat(args, js)
    return js