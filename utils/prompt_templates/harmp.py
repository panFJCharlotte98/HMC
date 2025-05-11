from utils.tool import *
from utils.knowledge.harmp import *

from_raw_data = '{from_raw_data}'
from_dependency = '{from_dependency}'
# --------------------------- For Multimodal LMMs --------------------#
VLREASONING = {
    'name': "VLReasoning", 'should_evaluate': False, 'take_image': True,
    'gen_depend_on': None,
    'versions': {
        'CoT': {
            "INS": f'''This is an online meme related to U.S. politics. Classify the meme as either harmful or harmless based on widely accepted values, established knowledge, and social norms. Now, let's analyze step by step:'''
        },
    },
    'output_format': {
        'v0': {"INS": '''''', 'post_process_func': post_process_to_remove_gibberish},
    },
}

check_dependency = '''{check_dependency}'''
GPT_DIRECT_CLASSIFY = {
    'name': "Classify",
    'should_evaluate': False,
    'take_image': True,
    'gen_depend_on': None,
    'versions': {
        'v0': {'INS': f'''Classify this meme as either harmful or harmless.'''},
        'v1': {'INS': f'''This is an online meme related to U.S. politics. Classify this meme as either harmful or harmless based on widely accepted values, established knowledge, and social norms.'''},
    },
    'output_format': {
        'v0': {"INS": '''''', 'post_process_func': post_process_to_remove_gibberish}
    },
}

GPT_DESCRIBE = {
    'name': "Describe", 'should_evaluate': False, 'take_image': True, 'gen_depend_on': None,
    'versions': {
        'v0': {'INS': f'''This is an online meme related to U.S. politics. Describe the visual content of the meme without interpretation. If there is any overlaid caption, transcribe it exactly as shown without paraphrasing.'''},
    },
    'output_format': {
        'v0': {"INS": '''''', 'post_process_func': post_process_to_remove_gibberish}
    },
}

DESCRIBE = {
    'name': "Describe", 'should_evaluate': False,'take_image': True,'gen_depend_on': None,
    'versions': {
        'v0': {"INS" : '''What is shown in this meme?'''},
    },
    'output_format': {
        'v0': {"INS": "", 'post_process_func': post_process_description},
    }
}

cname = "{cname}"
cname_map = {
    'trump': "Donald Trump",
    'biden': "Joe Biden",
    'obama': "Barack Obama",
    'hillary': "Hillary Clinton",
    'b&o': "Biden and Obama",
    #'bern': "Bernie Sanders",
    #'gary': "Gary Johnson",
}
celeb_kw = {
    'trump': ['trump', 'donald'],
    'hillary': ['hillary', 'clinton'],
    'obama': ['obama', 'barack', 'michelle'],
    'biden': ['joe', 'biden'],
    #'bern': ['bernie', 'bern'],
    #'gary': ['gary', 'johnson'],
}
party_kw = ['democrat', 'republican', 'green party', 'libertarian', 'voter']
AUX = {
    'name': "Aux", 'should_evaluate': False, 'take_image': True, 'gen_depend_on': None,
    'versions': {
        'trump': {"INS" : f'''Is {cname_map['trump']} depicted in the image?'''},
        'biden': {"INS" : f'''Is {cname_map['biden']} depicted in the image?'''},
        'obama': {"INS" : f'''Is {cname_map['obama']} depicted in the image?'''},
        'hillary': {"INS" : f'''Is {cname_map['hillary']} depicted in the image?'''},
        'b&o': {"INS" : f'''Does this image feature {cname_map['biden']} and {cname_map['obama']}?'''},
        'party': {"INS" : f'''Is any political party explicitly involved in this image?'''},
        # 'party1': {"INS" : f'''Is any political party involved in this image?'''},
        #'bern': {"INS" : f'''Is {cname_map['bern']} portrayed in the image?'''},
        #'gary': {"INS" : f'''Is {cname_map['gary']} portrayed in the image?'''},
    },
    'output_format': {
        'v0': {"INS": '''Start your response with "Yes," or "No," before giving the explanation.''', 'post_process_func': extract_yes_or_no},
    }
}

CELEB = {
    'name': "Celeb", 'should_evaluate': False, 'take_image': True, 'gen_depend_on': None,
    'versions': {
        'celeb': {"INS": '''Is any politician or celebrity portrayed in the image? If yes, who?'''},
        'leaders': {"INS": '''Is any head of state portrayed in the image?'''}
    },
    'output_format': {
        'v0': {"INS": '''Start your response with "Yes," or "No," before giving further explanation.''', 'post_process_func': extract_yes_or_no},
    }
}

# --------------------------- For Unimodal LLMs --------------------#

UNIFY_SYS = '''You are a helpful assistant.'''
from_data_text = "{from_data_text}"
INTEGRATE = {
    'name': "Integrate", 'should_evaluate': False, 'take_image': False, 'gen_depend_on': [AUX['name'], CELEB['name'], DESCRIBE['name']],
    'versions': {
        'v1': {
            "INS": [
                f'''Given the following information provided about an online meme, synthesize these information into a coherent, unified, and neutral description of the meme's content. Exclude any assumption about the meme's tone or intent. **Information**: {from_dependency}''',
                f'''{from_data_text}'''
            ]
        },
    },
    'output_format': {
        'v0': {"INS": '''''', 'post_process_func': post_process_description},
    }
}

assign_guidelines = "{assign_guidelines}"
REASONING = {
    'name': "Reasoning", 'should_evaluate': False, 'take_image': False,
    'versions': {
        # 'CoT': {
        #     'gen_depend_on': [INTEGRATE['name']],
        #     'INS': [
        #         f'''Given the following description of an online meme related to U.S. politics, classify the meme content as either harmful or harmless based on widely accepted values, established knowledge and social norms.''',
        #         f'''**Description of the meme you need to classify**: {from_dependency}''',
        #         '''Now, let's analyze step by step:'''
        #     ]
        # },
        'CoT': {
            'gen_depend_on': [INTEGRATE['name']],
            'INS': [
                f'''Given the following description of an image related to U.S. politics, classify the image content as either harmful or harmless based on common values, knowledge and social norms.''',
                f'''**Description of the image**: {from_dependency}''',
                '''Now, let's analyze step by step:'''
            ]
        },
        'CoT+': {
            'gen_depend_on': [INTEGRATE['name']],
            'INS': [
                f'''Given the following description of an image related to U.S. politics, classify the image content as either harmful or harmless based on common values, knowledge, social norms and the provided guidelines.''',
                f'''**Guidelines**: {assign_guidelines}''',
                f'''**Description of the image**: {from_dependency}''',
                '''Now, let's analyze by applying the guidelines one by one:'''
            ]
        },
        # 'CoT+': {
        #     'gen_depend_on': [INTEGRATE['name']],
        #     'INS': [
        #         f'''Given the following description of an online meme related to U.S. politics,''',
        #         '''classify the meme content as either harmful or harmless based on widely accepted values, established knowledge, social norms and the provided guidelines.''',
        #         f'''**Guidelines**: {assign_guidelines}''',
        #         f'''**Description of the meme you need to classify**: {from_dependency}''',
        #         '''Now, let's analyze step by step:'''
        #         # '''Now, let's analyze by applying the guidelines one by one:'''
        #     ]
        # },
    },
    'output_format': {
        'v0': {"INS": '''''', 'post_process_func': post_process_to_remove_gibberish},
    }
}

DECISION = {
    'name': "Decision", 'should_evaluate': True, 'take_image': False,
    'versions': {
        'v0': {
            'gen_depend_on': None,
            'INS': f'''If you just classified the image content as harmful, output "Conclusion: Harmful." Otherwise, output "Conclusion: Harmless."''',
        },
        'v1': {
            'gen_depend_on': None,
            'INS': f'''If you just classified the meme content as harmful, output "Conclusion: Harmful." Otherwise, output "Conclusion: Harmless."''',
        },
        'gpt': {
            'gen_depend_on': [GPT_DIRECT_CLASSIFY['name']],
            'INS': f'''If you just classified the meme content as harmful, output "Conclusion: Harmful." Otherwise, output "Conclusion: Harmless."''',
        },
        'vl': {
            'gen_depend_on': None,
            'INS': f'''If you just classified the meme as harmful, output "Conclusion: Harmful." Otherwise, output "Conclusion: Harmless."''',
        },
    },
    'output_format': {
        'v0': {"INS": '''''', 'post_process_func': harmc_extract_classification_label},
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

M2T = {
    'lmm_1': {
        'prompt': {
            0: {'template': CELEB, "version": "celeb", "out_format": 'v0'},
            1: {'template': CELEB, "version": "leaders", "out_format": 'v0'},
            2: {'template': DESCRIBE, "version": "v0", "out_format": 'v0'},
        },
        'multi-turn': False},
    'lmm_2': {
        'prompt': {
            0: {'template': AUX, "version": "trump", "out_format": 'v0'},
            1: {'template': AUX, "version": "biden", "out_format": 'v0', "load_from_prestep": True},
            2: {'template': AUX, "version": "obama", "out_format": 'v0', "load_from_prestep": True},
            3: {'template': AUX, "version": "hillary", "out_format": 'v0', "load_from_prestep": True},
            4: {'template': AUX, "version": "b&o", "out_format": 'v0', "load_from_prestep": True},
            5: {'template': AUX, "version": "party", "out_format": 'v0', "load_from_prestep": True},
        },
        'multi-turn': False},
    'llm_1': {
        'prompt': {
            0: {'template': INTEGRATE, "version": "v1", "out_format": 'v0', "load_from_prestep": True, "return_prestep_path": False},
        },
        'multi-turn': False
    },
}

# ******************************************************************************************* # 
GPT = {
    'lmm': {
        'prompt': {
            0: {'template': GPT_DIRECT_CLASSIFY, "version": "v1", "out_format": 'v0'},
        },
        'multi-turn': False},
    'llm': {
        'multi-turn': True,
        'prompt': {
            1: {'template': DECISION, "version": "gpt", "out_format": 'v0'},
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

p1 = {
    'llm_2': {
        'multi-turn': True,
        'prompt': {
            0: {'template': REASONING, "version": "CoT+", "out_format": 'v0', 'max_new_tokens': 1536},
            1: {'template': DECISION, "version": "v0", "out_format": 'v0'},
        }
    }
}

# Unimodal baseline: Inference with LLM
b2 = {
    'llm_2': {
        'multi-turn': True,
        'prompt': {
            0: {'template': REASONING, "version": "CoT", "out_format": 'v0', 'max_new_tokens': 1536},
            1: {'template': DECISION, "version": "v0", "out_format": 'v0'},
        }
    }
}

B2 = dict(**M2T, **b2)
PP = dict(**M2T, **p1)
# ******************************************************************************************* # 

HARMP_PROMPT_SCHEMES = {
    'M2T': M2T,
    'B1': B1,
    'B2': B2,
    'GPT': GPT,
    'PP': PP,
    'GPT_DESCRIBE': GPT_describe
}

def assign_guidelines_(js):
    aux_info = js["aux_info"]
    Rules = [TYPES["general"]]
    
    assert "processed_prediction" in js
    text_lower = js["processed_prediction"].lower()
    text_words = [w.replace("'s", "").replace("’s", "") for w in text_lower.split()]
    politician_mentions = []
    for _, kwl in celeb_kw.items():
        politician_mentions.extend(kwl)
    if any([w in text_words for w in politician_mentions]):
        Rules.append(TYPES['politicians'])
    
    # political parties
    # if any([w in text_lower for w in party_kw]):
    #     Rules.append(TYPES['party'])

    for k, v in aux_info.items():
        if (k in cname_map) and (v['flag']):
            if TYPES['politicians'] not in Rules:
                Rules.append(TYPES['politicians'])
            if (k in ['biden', 'b&o']) and (TYPES[cname_map['biden']] not in Rules):
                Rules.append(TYPES[cname_map['biden']])
        if (k =='party') and v['flag'] and (TYPES[k] not in Rules):
            Rules.append(TYPES[k])

    GL = " ".join([f"{i+1}. {rule}" for i, rule in enumerate(Rules)]) if len(Rules) > 1 else Rules[0]
    return GL

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
    
    if from_data_text in tmp:
        if js['text']:
            prompt = f'''Also, some overlaid text in the image is recognized as: "{js['text']}"'''
        else:
            prompt = ""
        return tmp.format(from_data_text = prompt), js
    
    if assign_guidelines in tmp:
        assert "aux_info" in js
        return tmp.format(assign_guidelines = assign_guidelines_(js)), js

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
    if cname in ins_output_format:
        ins_output_format = ins_output_format.format(cname = cname_map[p_version])
    img_history = []

    if isinstance(prompt, list):
        ins = []
        for item in prompt:
            item, js = fill_placeholder(item, js)
            ins.append(item)
        if ins_output_format:
            ins.append(ins_output_format)
        text_content = " ".join(" ".join(ins).split())
    if isinstance(prompt, str):
        text_content, js = fill_placeholder(prompt, js)
        text_content = " ".join(" ".join([text_content, ins_output_format]).split()).strip()
        
    
    if js is not None:
        if args.current_model_type == 'llm':
            usr_pt = {"role": "user", "content": text_content}
        if args.current_model_type == 'lmm':
            img_path = js["img"]
            if args.use_resized_img:
                resized_img = "img_768"
                if args.current_model.startswith('qwen2'):
                    resized_img = "img_768_1280"
                img_path = js[resized_img] if ((resized_img in js) and js[resized_img]) else js["img"]
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
                                    
        js['chat_history'] = dialog
        js['task'] = args.task
        js['img_history'] = img_history
    return js

def prompt_harmp(args, model_tag, js):
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

