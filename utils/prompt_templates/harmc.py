from utils.tool import *
from utils.knowledge.harmc import *

from_raw_data = '{from_raw_data}'
from_dependency = '{from_dependency}'
from_previous_turn = '{from_previous_turn}'
# --------------------------- For Multimodal LMMs --------------------#
Introduce = '''This is an online meme related to the COVID-19 pandemic.'''
VLREASONING = {
    'name': "VLReasoning", 'should_evaluate': False, 'take_image': True,
    'gen_depend_on': None,
    'versions': {
        'CoT': {
            "INS": f'''{Introduce} Classify the meme as either harmful or harmless based on widely accepted values, established knowledge, and social norms. Now, let's analyze step by step:'''
        },
    },
    'output_format': {
        'v0': {"INS": '''''', 'post_process_func': post_process_to_remove_gibberish},
    },
}

check_aux = "{check_aux}"
check_dependency = '''{check_dependency}'''
introduce = f'''This is a meme with an overlaid caption: "{from_raw_data}".'''

DESCRIBE = {
    'name': "Describe", 'should_evaluate': False,'take_image': True,'gen_depend_on': None,
    'versions': {
        'v0': {"INS" : '''What is shown in the meme?'''},
    },
    'output_format': {
        'v0': {"INS": "", 'post_process_func': post_process_to_remove_gibberish},
    }
}

# CELEB = {
#     'name': "Celeb", 'should_evaluate': False, 'take_image': True, 'gen_depend_on': None,
#     'versions': {
#         'trump': {"INS" : f'''Is Donald Trump in the image?'''},
#         'USpolitician': {"INS": '''Does this image feature any politican of the United States? If yes, who are they?'''},
#         'leaders': {"INS": '''Does this image feature any head of state? If yes, who are they?'''}
#     },
#     'output_format': {
#         'v0': {"INS": '''Start your response with "Yes," or "No," before giving further explanation.''', 'post_process_func': extract_yes_or_no}
#     }
# }

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
        'trump': {"INS" : f'''Is {cname_map['trump']} in the image?'''},
        #'trump': {"INS" : f'''Is {cname_map['trump']} depicted in the image?'''},
        'biden': {"INS" : f'''Is {cname_map['biden']} depicted in the image?'''},
        'obama': {"INS" : f'''Is {cname_map['obama']} depicted in the image?'''},
        'hillary': {"INS" : f'''Is {cname_map['hillary']} depicted in the image?'''},
        'b&o': {"INS" : f'''Does this image feature {cname_map['biden']} and {cname_map['obama']}?'''},
        #'bern': {"INS" : f'''Is {cname_map['bern']} portrayed in the image?'''},
        #'gary': {"INS" : f'''Is {cname_map['gary']} portrayed in the image?'''},
        'party': {"INS" : f'''Is any political party explicitly involved in this image?'''},
        # 'party1': {"INS" : f'''Is any political party involved in this image?'''}
        'country': {"INS" : f'''Is any country, region or government body explicitly involved in this image?'''},
    },
    'output_format': {
        'v0': {"INS": '''Start your response with "Yes," or "No," before giving the explanation.''', 'post_process_func': extract_yes_or_no},
    }
}

CELEB = {
    'name': "Celeb", 'should_evaluate': False, 'take_image': True, 'gen_depend_on': None,
    'versions': {
        'trump': {"INS" : f'''Is {cname_map['trump']} in the image?'''},
        'politician': {"INS": '''Does this image feature any politican of the United States? If yes, who are they?'''},
        'leaders': {"INS": '''Does this image feature any head of state? If yes, who are they?'''},
        'celeb': {"INS": '''Is any politician or celebrity portrayed in the image? If yes, who?'''},
        # 'leaders': {"INS": '''Is any head of state portrayed in the image?'''},
    },
    'output_format': {
        'v0': {"INS": '''Start your response with "Yes," or "No," before giving further explanation.''', 'post_process_func': extract_yes_or_no},
    }
}

# --------------------------- For Unimodal LLMs --------------------#

UNIFY_SYS = '''You are a helpful assistant.''' #'''You are an expert in meme content comprehension and hatefulness detection.'''
from_Integrate = "{from_Integrate}"
from_data_text = "{from_data_text}"
INTEGRATE = {
    'name': "Integrate", 'should_evaluate': False, 'take_image': False, 'gen_depend_on': [CELEB['name'], DESCRIBE['name']],
    'versions': {
        'v0': {
            "INS": [
                f'''Given the following information provided about an online meme, synthesize these information into a coherent, unified, and neutral description of the meme's content. Exclude any assumption about the meme's tone or intent. **Information**: {from_dependency}''',
                f'''{from_data_text}'''
            ]
        },
        'v1': {
            "INS": [
                f'''Given the following information provided about an online meme, synthesize and rephrase these information into a coherent, unified, and neutral description of the meme's content, **Information**: {from_dependency}''',
                f'''{from_data_text}'''
            ]
        },
        'ori': {
            "INS": f'''Given the following information provided about an online meme, and disregarding any information about overlaid text or captions, synthesize and rephrase these information into a unified, detailed description of the image content. Information: "{from_dependency}"'''
        }
    },
    'output_format': {
        'v0': {"INS": '''''', 'post_process_func': post_process_to_remove_gibberish},
    }
}

assign_guidelines = "{assign_guidelines}"
REASONING = {
    'name': "Reasoning", 'should_evaluate': False, 'take_image': False,
    'versions': {
        'CoT+': {
            'gen_depend_on': [INTEGRATE['name']],
            'INS': [
                f'''Given the following description of an online meme related to COVID-19 pandemic,''',
                '''classify the meme content as either harmful or harmless based on widely accepted values, established knowledge and social norms.''', #and the provided guidelines
                f'''**Here are some guidelines for your reference**: {assign_guidelines}''',
                #Description of the meme
                f'''**Meme content you need to classify**: {from_dependency}''',
                #'''Now, let's analyze by applying the guidelines one by one:''',
                '''Now, let's think step by step:'''
            ]
        },
        'CoT': {
            'gen_depend_on': [INTEGRATE['name']],
            'INS': [
                f'''Given the following description of an online meme related to COVID-19 pandemic, classify the meme content as either harmful or harmless based on widely accepted values, established knowledge and social norms.''',
                f'''**Meme content you need to classify**: {from_dependency}''',
                '''Now, let's analyze step by step:'''
            ]
        }
    },
    'output_format': {
        'v0': {"INS": '''''', 'post_process_func': post_process_to_remove_gibberish},
    }
}

GPT_DIRECT_CLASSIFY = {
    'name': "Classify", 'should_evaluate': False, 'take_image': True, 'gen_depend_on': None,
    'versions': {
        'v0': {'INS': f'''{Introduce} Classify this meme as either harmful or harmless.'''},
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
            'INS': f'''If you just classified the image as harmful, output "Conclusion: Harmful." Otherwise, output "Conclusion: Harmless."''',
        },
        'v1': {
            'gen_depend_on': None,
            'INS': f'''If you just classified the meme content as harmful, output "Conclusion: Harmful." Otherwise, output "Conclusion: Harmless."''',
        },
        'vl': {
            'gen_depend_on': None,
            "INS": f'''If you just classified the meme as harmful, output "Conclusion: Harmful." Otherwise, output "Conclusion: Harmless."''',
        },
        'gpt': {
            'gen_depend_on': [GPT_DIRECT_CLASSIFY['name']],
            "INS": f'''If you just classified the meme content as harmful, output "Conclusion: Harmful." Otherwise, output "Conclusion: Harmless."''',
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

GPT = {
    'lmm': {
        'prompt': {
            0: {'template': GPT_DIRECT_CLASSIFY, "version": "v0", "out_format": 'v0'},
        },
        'multi-turn': False
    },
    'llm': {
        'multi-turn': True,
        'prompt': {
            1: {'template': DECISION, "version": "gpt", "out_format": 'v0'},
        }
    }
}

# M2T = {
#     'lmm': {
#         'prompt': {
#                 0: {'template': CELEB, "version": "trump", "out_format": 'v0'},
#                 1: {'template': CELEB, "version": "USpolitician", "out_format": 'v0'},
#                 2: {'template': CELEB, "version": "leaders", "out_format": 'v0'},
#                 3: {'template': DESCRIBE, "version": "v0", "out_format": 'v0'},
#         },
#         'multi-turn': False},
#     'llm_1': {
#         'prompt': {
#                 0: {'template': INTEGRATE, "version": "v0", "out_format": 'v0'},    
#         },
#         'multi-turn': False},
# }

M2T = {
    'lmm_1': {
        'prompt': {
            0: {'template': CELEB, "version": "politician", "out_format": 'v0'},
            1: {'template': CELEB, "version": "leaders", "out_format": 'v0'},
            2: {'template': CELEB, "version": "trump", "out_format": 'v0'},
            #2: {'template': CELEB, "version": "celeb", "out_format": 'v0'},####
            3: {'template': DESCRIBE, "version": "v0", "out_format": 'v0'},
        },
        'multi-turn': False},
    'lmm_2': {
        'prompt': {
            0: {'template': AUX, "version": "trump", "out_format": 'v0'},
            1: {'template': AUX, "version": "biden", "out_format": 'v0', "load_from_prestep": True},####
            2: {'template': AUX, "version": "obama", "out_format": 'v0', "load_from_prestep": True},
            3: {'template': AUX, "version": "b&o", "out_format": 'v0', "load_from_prestep": True},
            # # 3: {'template': AUX, "version": "hillary", "out_format": 'v0', "load_from_prestep": True},
            # 3: {'template': AUX, "version": "party", "out_format": 'v0', "load_from_prestep": True},
            # 4: {'template': AUX, "version": "country", "out_format": 'v0', "load_from_prestep": True},
        },
        'multi-turn': False},
    'llm_1': {
        'prompt': {
            0: {'template': INTEGRATE, "version": "v1", "out_format": 'v0', "load_from_prestep": True, "return_prestep_path": False},  
            # 0: {'template': INTEGRATE, "version": "v0", "out_format": 'v0', "load_from_prestep": True, "return_prestep_path": False},    
            # 1: {'template': AUXT, "version": "party", "out_format": 'v0',
            # 'max_new_tokens': 256}, 
        },
        'multi-turn': False
    },
}

# Unimodal baseline: Inference with LLM
b2 = {
    'llm_2': {
        'multi-turn': True,
        'prompt': {
            0: {'template': REASONING, "version": "CoT", "out_format": 'v0'},
            1: {'template': DECISION, "version": "v1", "out_format": 'v0'},
        }
    }
}
# ******************************************************************************************* # 
# Proposed Pipeline
p1 = {
    'llm_2': {
        'multi-turn': True,
        'prompt': {
            0: {'template': REASONING, "version": "CoT+", "out_format": 'v0'},#'max_new_tokens': 1536
            1: {'template': DECISION, "version": "v1", "out_format": 'v0'},
        }
    }
}
PP = dict(**M2T, **p1)
B2 = dict(**M2T, **b2)
# ******************************************************************************************* # 

HARMC_PROMPT_SCHEMES = {
    "B1": B1,
    "B2": B2,
    "GPT": GPT,
    'M2T': M2T,
    'PP': PP,
}

def assign_guidelines_(js):
    # aux_info = js["aux_info"]
    # #Rules = [R_interpret, R_implicit]
    # Rules = [R_implicit_ori, R_interpret_ori]

    # assert "processed_prediction" in js
    # text_lower = js["processed_prediction"].lower()
    # text_words = [w.replace("'s", "").replace("’s", "") for w in text_lower.split()]
    
    # # # Politicians
    # politician_mentions = []
    # for name, kwl in celeb_kw.items():
    #     if name in ['trump']:
    #         politician_mentions.extend(kwl)
    # if any([w in text_words for w in politician_mentions]):
    #     Rules.append(TYPES[cname_map['trump']])
    
    # # China
    # if any([w in text_lower for w in ['china', 'chinese']]):
    #     Rules.append(TYPES["China"])

    # # Others in case not inclued yet
    # for k, v in aux_info.items():
    #     if (v['flag']):
    #         if (k in cname_map):
    #             if (k in ['trump', 'biden']) and (TYPES[cname_map[k]] not in Rules):
    #                 Rules.append(TYPES[cname_map[k]])
    #         # if k == "country":
    #         #     Rules.append(R_general)   
    # #basic.reverse()
    # GL = " ".join([f"{i+1}. {rule}" for i, rule in enumerate(Rules)]) if len(Rules) > 1 else Rules[0]

    GL = KNOWLEDGE
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
    if from_data_text in tmp:
        if js['text']:
            prompt = f'''Also, some overlaid text in the image is recognized as: "{js['text']}"'''
        else:
            prompt = ""
        return tmp.format(from_data_text = prompt), js
    if assign_guidelines in tmp:
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

def prompt_harmc(args, model_tag, js):
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

