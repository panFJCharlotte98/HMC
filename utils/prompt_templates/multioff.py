from utils.knowledge.multioff import *
from utils.tool import *
from utils.fewshot.multioff import *
import random

from_raw_data = '{from_raw_data}'
from_dependency = '{from_dependency}'
from_previous_turn = '{from_previous_turn}'
# --------------------------- For Multimodal LMMs --------------------#
Introduce = '''This is an online meme related to 2016 U.S. Presidential Election.'''
VLREASONING = {
    'name': "VLReasoning", 'should_evaluate': False, 'take_image': True,
    'gen_depend_on': None,
    'versions': {
        'CoT': {
            "INS": f'''This is an image related to 2016 U.S. Presidential Election. Classify the image as either offensive or non-offensive based on based on common values, knowledge and social norms. Now, let's analyze step by step:'''
        },
    },
    'output_format': {
        'v0': {"INS": '''''', 'post_process_func': post_process_to_remove_gibberish},
    },
}

DESCRIBE = {
    'name': "Describe", 'should_evaluate': False,'take_image': True,'gen_depend_on': None,
    'versions': {
        'v0': {"INS" : '''What is shown in this image?'''},
    },
    'output_format': {
        'v0': {"INS": "", 'post_process_func': post_process_to_remove_gibberish},
    }
}

check_dependency = '''{check_dependency}'''
cname = "{cname}"
cname_map = {
    'trump': "Donald Trump",
    'hillary': "Hillary Clinton",
    'obama': "Barack Obama",
    'bern': "Bernie Sanders",
    'gary': "Gary Johnson",
    'biden': "Joe Biden",
    'b&o': "Biden and Obama",
}
celeb_kw = {
    'trump': ['trump', 'donald'],
    'hillary': ['hillary', 'clinton'],
    'obama': ['obama'],
    'bern': ['bernie', 'bern'],
    'gary': ['gary', 'johnson'],
}
party_kw = ['democrat', 'republican', 'green party', 'libertarian', 'voter']
AUXIN = {
    'name': "Auxi", 'should_evaluate': False, 'take_image': True, 'gen_depend_on': None,
    'versions': {
        'trump': {"INS" : f'''Is {cname_map['trump']} involved in the image?'''},
        'hillary': {"INS" : f'''Is {cname_map['hillary']} involved in the image?'''},
        'obama': {"INS" : f'''Is {cname_map['obama']} portrayed in the image?'''},
        'bern': {"INS" : f'''Is {cname_map['bern']} involved in the image?'''},
        'gary': {"INS" : f'''Is {cname_map['gary']} portrayed in the image?'''},
    },
    'output_format': {
        'v0': {"INS": '''Start your response with "Yes," or "No," before giving the explanation.''', 'post_process_func': extract_yes_or_no},
    }
}
AUX = {
    'name': "Aux", 'should_evaluate': False, 'take_image': True, 'gen_depend_on': None,
    'versions': {
        'lgbt': {"INS" : f'''Is LGBTQ+ community or LGBTQ+ individual portrayed in this image?'''},
        'muslim': {"INS": f'''Is any individual of Middle Eastern descent portrayed in the image?'''},
        'racial': {"INS" : f'''Is any protected racial or minority group (such as African Americans or other colored people) portrayed in this image?'''},
    },
    'output_format': {
        'v0': {"INS": '''Start your response with "Yes," or "No," before giving the explanation.''', 'post_process_func': extract_yes_or_no},
    }
}


CELEB = {
    'name': "Celeb", 'should_evaluate': False, 'take_image': True, 'gen_depend_on': None,
    'versions': {
        'pc': {"INS": '''Is any politician or celebrity portrayed in the image? If yes, who are they?'''},
        'leaders': {"INS": '''Is any head of state portrayed in the image?'''}
    },
    'output_format': {
        'v0': {"INS": '''Start your response with "Yes," or "No," before giving the explanation.''', 'post_process_func': extract_yes_or_no},
    }
}

# --------------------------- For Unimodal LLMs --------------------#
UNIFY_SYS = '''You are a helpful assistant.'''
from_data_text = "{from_data_text}"
INTEGRATE = {
    'name': "Integrate", 'should_evaluate': False, 'take_image': False, 'gen_depend_on': [AUXIN['name'], CELEB['name'], DESCRIBE['name']],
    'versions': {
        'v1': {
            "INS": [
                f'''Given the following information provided about an online meme, synthesize these information into a coherent, unified, and neutral description of the meme's content. DO NOT include any assumption about the meme's tone or intent. **Information**: {from_dependency}''',
                f'''{from_data_text}'''
            ]
        }
    },
    'output_format': {
        'v0': {"INS": '''''', 'post_process_func': post_process_to_remove_gibberish},
    }
}

from_gpt_description = '''{from_gpt_description}'''
auxt_ins = f'''Given the following description of an image related to 2016 U.S. Presidential Election, answer the question:'''
AUXT = {
    'name': "Auxt", 'should_evaluate': False, 'take_image': False, 'gen_depend_on': [INTEGRATE['name']],
    'versions': {
        'party': {
            "INS" : [
                auxt_ins,
                f'''Does this image content explicitly target at any political party or political supporters/opponents as a group? **Description of the image**: {from_dependency}''',
            ]
        },
        'party_GD': {
            "INS" : [
                auxt_ins,
                f'''Does this image content explicitly target at any political party or political supporters/opponents as a group? **Description of the image**: {from_gpt_description}''',
            ]
        },
        'lgbt_t': {
            "INS" : [
                auxt_ins,
                f'''Is LGBTQ+ community or LGBTQ+ issue involved in this image content? **Description of the image**: {from_dependency}''',
            ]
        },
        'lgbt_t_GD': {
            "INS" : [
                auxt_ins,
                f'''Is LGBTQ+ community or LGBTQ+ issue involved in this image content? **Description of the image**: {from_gpt_description}''',
            ]
        },
        'racial_t': {
            "INS" : [
                auxt_ins,
                f'''Is any reference to individuals of protected groups (e.g., African Americans, Muslims, immigrants, etc.) involved in this image content? **Description of the image**: {from_dependency}''',
            ]
        },
        'racial_t_GD': {
            "INS" : [
                auxt_ins,
                f'''Is any reference to individuals of protected groups (e.g., African Americans, Muslims, immigrants, etc.) involved in this image content? **Description of the image**: {from_gpt_description}''',
            ]
        },
    },
    'output_format': {
        'v0': {"INS": '''Start your response with "Yes," or "No," before giving the explanation.''', 'post_process_func': extract_yes_or_no},
    }
}


assign_guidelines = "{assign_guidelines}"
INTRO = '''Given the following description of an image related to 2016 U.S. Presidential Election,'''
BASELINE_CLASSIFY_INS = '''classify the image content as either offensive or non-offensive based on common values, knowledge and social norms.'''
PP_CLASSIFY_INS = '''classify the image content as either offensive or non-offensive based on common values, knowledge, social norms and the provided guidelines.'''
meme2text = f'''**Description of the image**: {from_dependency}'''
guidelines = f'''**Guidelines**: {assign_guidelines}'''
pp_cot_ins = '''Now, let's analyze by applying the guidelines one by one:'''
cot_ins = '''Now, let's analyze step by step:'''
fewshots = '''{fewshots}'''
REASONING = {
    'name': "Reasoning", 'should_evaluate': False, 'take_image': False,
    'versions': {
        'CoT+': {
            'gen_depend_on': [INTEGRATE['name']],
            'INS': [
                f'''{INTRO}''',
                f'''{PP_CLASSIFY_INS}''',
                guidelines,
                meme2text,
                pp_cot_ins
            ]
        },
        'CoT': {
            'gen_depend_on': [INTEGRATE['name']],
            'INS': [
                f'''{INTRO} {BASELINE_CLASSIFY_INS}''',
                meme2text,
                cot_ins
            ]
        },
        'CoT+GD': {
            'gen_depend_on': [INTEGRATE['name']],
            'INS': [
                f'''{INTRO}''',
                f'''{PP_CLASSIFY_INS}''',
                guidelines,
                f'''**Description of the image**: {from_gpt_description}''',
                pp_cot_ins
            ]
        },
        'CoT+qw3': {
            'gen_depend_on': [INTEGRATE['name']],
            'INS': [
                f'''{INTRO}''',
                f'''{PP_CLASSIFY_INS}''',
                guidelines,
                meme2text,
                pp_cot_ins
            ]
        },
        'CoTqw3': {
            'gen_depend_on': [INTEGRATE['name']],
            'INS': [
                f'''{INTRO} {BASELINE_CLASSIFY_INS}''',
                meme2text,
                cot_ins
            ]
        },
        'fsCoT': {
            'gen_depend_on': [INTEGRATE['name']],
            'INS': [
                f'''{INTRO} {BASELINE_CLASSIFY_INS}''',
                fewshots,
                f'''**Description of the image you need to classify**: {from_dependency}''',
                f'''**Classification**: {cot_ins}'''
            ]
        },
    },
    'output_format': {
        'v0': {"INS": '''''', 'post_process_func': post_process_to_remove_gibberish},
    }
}

GPT_DIRECT_CLASSIFY = {
    'name': "Classify", 'should_evaluate': False, 'take_image': True, 'gen_depend_on': None,
    'versions': {
        'v0': {'INS': f'''{Introduce} Classify the meme as either offensive or non-offensive based on widely accepted values, established knowledge, and social norms.'''},
    },
    'output_format': {
        'v0': {"INS": '''''', 'post_process_func': post_process_to_remove_gibberish}
    },
}

main_ins = "What is going on in this image? Describe the content of the image without interpreting any underlying implications."
transcribe = "If there is any overlaid text, transcribe the text without paraphrasing."
marginal_info = "Ignore any watermarks, post timestamps, usernames, or engagement metrics of tweets or webpage posts."
tone = "Do not assume the image's tone or intent to be humorous or lighthearted. Maintain a neutral and descriptive tone."
GPT_DESCRIBE = {
    'name': "Describe", 'should_evaluate': False, 'take_image': True, 'gen_depend_on': None,
    'versions': {
        'v0': {'INS': f'''{Introduce} {main_ins} {transcribe} {marginal_info} {tone} Output your description in one paragraph.'''},
        'v1': {'INS': f'''{Introduce} Describe the visual content of the meme without interpretation. If there is any overlaid caption, transcribe it exactly as shown without paraphrasing.'''},
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
            'INS': f'''If you just classified the image content as offensive, output "Conclusion: Offensive." Otherwise, output "Conclusion: Non-offensive."''',
        },
        'v1': {
            'gen_depend_on': None,
            'INS': f'''If you just classified the meme content as offensive, output "Conclusion: Offensive." Otherwise, output "Conclusion: Non-offensive."''',
        },
        'vl': {
            'gen_depend_on': None,
            'INS': f'''If you just classified the meme as offensive, output "Conclusion: Offensive." Otherwise, output "Conclusion: Non-offensive."''',
        },
        'gpt': {
            'gen_depend_on': [GPT_DIRECT_CLASSIFY['name']],
            'INS': f'''If you just classified the meme content as offensive, output "Conclusion: Offensive." Otherwise, output "Conclusion: Non-offensive."''',
        },
    },
    'output_format': {
        'v0': {"INS": '''''', 'post_process_func': multioff_extract_classification_label},
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
            1: {'template': DECISION, "version": "gpt", "out_format": 'v0', 'batch_size': 1},
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
            0: {'template': CELEB, "version": "pc", "out_format": 'v0'},
            1: {'template': DESCRIBE, "version": "v0", "out_format": 'v0'},
            2: {'template': AUXIN, "version": "trump", "out_format": 'v0'},
            3: {'template': AUXIN, "version": "hillary", "out_format": 'v0', "load_from_prestep": True},
            4: {'template': AUXIN, "version": "obama", "out_format": 'v0', "load_from_prestep": True},
            5: {'template': AUXIN, "version": "bern", "out_format": 'v0', "load_from_prestep": True},
            6: {'template': AUXIN, "version": "gary", "out_format": 'v0', "load_from_prestep": True},
            7: {'template': AUX, "version": "lgbt", "out_format": 'v0', "load_from_prestep": True},
            8: {'template': AUX, "version": "muslim", "out_format": 'v0', "load_from_prestep": True},
            9: {'template': AUX, "version": "racial", "out_format": 'v0', "load_from_prestep": True},
        },
        'multi-turn': False},    
    'llm_1': {
        'prompt': {
            0: {'template': INTEGRATE, "version": "v1", "out_format": 'v0', "load_from_prestep": True, "return_prestep_path": False},
            1: {'template': AUXT, "version": "lgbt_t", "out_format": 'v0', 'max_new_tokens': 256}, 
            2: {'template': AUXT, "version": "racial_t", "out_format": 'v0', 'max_new_tokens': 256, "load_from_prestep": True, "return_prestep_path": True},
            3: {'template': AUXT, "version": "party", "out_format": 'v0', 'max_new_tokens': 256, "load_from_prestep": True, "return_prestep_path": True},   
        },
        'multi-turn': False},
}

M2T_GD = {
    'lmm': {
        'prompt': {
            0: {'template': CELEB, "version": "pc", "out_format": 'v0'},
            1: {'template': DESCRIBE, "version": "v0", "out_format": 'v0'},
            2: {'template': AUXIN, "version": "trump", "out_format": 'v0'},
            3: {'template': AUXIN, "version": "hillary", "out_format": 'v0', "load_from_prestep": True},
            4: {'template': AUXIN, "version": "obama", "out_format": 'v0', "load_from_prestep": True},
            5: {'template': AUXIN, "version": "bern", "out_format": 'v0', "load_from_prestep": True},
            6: {'template': AUXIN, "version": "gary", "out_format": 'v0', "load_from_prestep": True},
            7: {'template': AUX, "version": "lgbt", "out_format": 'v0', "load_from_prestep": True},
            8: {'template': AUX, "version": "muslim", "out_format": 'v0', "load_from_prestep": True},
            9: {'template': AUX, "version": "racial", "out_format": 'v0', "load_from_prestep": True},
        },
        'multi-turn': False},    
    'llm_1': {
        'prompt': {
            0: {'template': INTEGRATE, "version": "v1", "out_format": 'v0', "load_from_prestep": True, "return_prestep_path": False}  
        },
        'multi-turn': False},
}

# ******************************************************************************************* # 
b2 = {
    'llm_2': {
        'multi-turn': True,
        'prompt': {
            0: {'template': REASONING, "version": "CoT", "out_format": 'v0', "load_from_prestep": True, "return_prestep_path": True},
            1: {'template': DECISION, "version": "v0", "out_format": 'v0'}
        }
    }
}

# Ablation: replace high-fidelity meme2text to GPT-generated description
pd = {
    'llm_2': {
        'prompt': {
            0: {'template': AUXT, "version": "lgbt_t_GD", "out_format": 'v0', 'max_new_tokens': 256}, 
            1: {'template': AUXT, "version": "racial_t_GD", "out_format": 'v0', 'max_new_tokens': 256, "load_from_prestep": True, "return_prestep_path": True},
            2: {'template': AUXT, "version": "party_GD", "out_format": 'v0', 'max_new_tokens': 256, "load_from_prestep": True, "return_prestep_path": True},   
        },
        'multi-turn': False},
    'llm_3': {
        'multi-turn': True,
        'prompt': {
            0: {'template': REASONING, "version": "CoT+GD", "out_format": 'v0', "load_from_prestep": True, "return_prestep_path": True},
            1: {'template': DECISION, "version": "v0", "out_format": 'v0'}
        }
    }
}
PD = dict(**M2T_GD, **pd)

p1 = {
    'llm_2': {
        'multi-turn': True,
        'prompt': {
            0: {'template': REASONING, "version": "CoT+", "out_format": 'v0', "load_from_prestep": True, "return_prestep_path": True},
            1: {'template': DECISION, "version": "v0", "out_format": 'v0'}
        }
    },
    # 'llm_3': {
    #     'multi-turn': True,
    #     'prompt': {
    #         21: {'template': REASONING, "version": "CoT+", "out_format": 'v0', "load_from": {'m_type': 'llm_1', 'rid': 3}, "return_load_from_path": True, 'new_conversation': True, "perturbation": "rephrased"},
    #         31: {'template': DECISION, "version": "v0", "out_format": 'v0'},
    #         22: {'template': REASONING, "version": "CoT+", "out_format": 'v0', 'new_conversation': True, "load_from": {'m_type': 'llm_1', 'rid': 3}, "return_load_from_path": True, "perturbation": "shuffled"},
    #         32: {'template': DECISION, "version": "v0", "out_format": 'v0'},
    #         23: {'template': REASONING, "version": "CoT+", "out_format": 'v0', 'new_conversation': True, "load_from": {'m_type': 'llm_1', 'rid': 3}, "return_load_from_path": True, "perturbation": "add_remove"},
    #         33: {'template': DECISION, "version": "v0", "out_format": 'v0'}
    #     }
    # }
}
PP = dict(**M2T, **p1)
B2 = dict(**M2T, **b2)

b2_qw3 = {
    'llm_2': {
        'multi-turn': True,
        'prompt': {
            0: {'template': REASONING, "version": "CoTqw3", "out_format": 'v0', "load_from_prestep": True, "return_prestep_path": True},
            1: {'template': DECISION, "version": "v0", "out_format": 'v0'}
        }
    }
}

p1_qw3 = {
    'llm_2': {
        'multi-turn': True,
        'prompt': {
            0: {'template': REASONING, "version": "CoT+qw3", "out_format": 'v0', "load_from_prestep": True, "return_prestep_path": True},
            1: {'template': DECISION, "version": "v0", "out_format": 'v0'}
        }
    }
}
PPqw3 = dict(**M2T, **p1_qw3)
B2qw3 = dict(**M2T, **b2_qw3)

p_fewshot = {
    'llm_2': {
        'multi-turn': True,
        'prompt': {
            0: {'template': REASONING, "version": "fsCoT", "out_format": 'v0'},
            1: {'template': DECISION, "version": "v0", "out_format": 'v0'}
        }
    }
}
FS = dict(**M2T, **p_fewshot)
# ******************************************************************************************* # 

MultiOFF_PROMPT_SCHEMES = {
    'M2T': M2T,
    'B1': B1,
    'B2': B2,
    'GPT': GPT,
    'PP': PP,
    'B2qw3': B2qw3,
    'PPqw3': PPqw3,
    'GPT_DESCRIBE': GPT_describe,
    'FS': FS,
    'PD': PD
}

def assign_guidelines_(js, args):
    aux_info = js["aux_info"]
    politician_mentions = []
    for _, kwl in celeb_kw.items():
        politician_mentions.extend(kwl)
    def formulate_rules(aux_info, politician_mentions, perturb_surfix=""):
        Rules = [TYPES[f"interpret{perturb_surfix}"], TYPES[f"general{perturb_surfix}"]]
        text_lower =  js["text"].lower()
        text_words = [w.replace("'s", "").replace("’s", "") for w in js["text"].lower().split()]

        # Politicians
        if any([w in text_words for w in politician_mentions]):
            Rules.append(TYPES[f'politicians{perturb_surfix}'])

        # Muslims
        if "muslim" in text_lower:
            Rules.append(TYPES[f'muslim{perturb_surfix}'])

        # political parties
        if any([w in text_lower for w in party_kw]):
            Rules.append(TYPES[f'party{perturb_surfix}'])

        for k, v in aux_info.items():
            if k.endswith("_GD"):
                k = k.replace("_GD", "")
            if (k in cname_map) and (v['flag']):
                if TYPES[f'politicians{perturb_surfix}'] not in Rules:
                    Rules.append(TYPES[f'politicians{perturb_surfix}'])
            if (k in TYPES) and v['flag'] and (TYPES[k+perturb_surfix] not in Rules):
                Rules.append(TYPES[k+perturb_surfix])
            if (k.endswith("_t")) and v['flag']:
                if TYPES[k.split("_")[0]+perturb_surfix] not in Rules:
                    Rules.append(TYPES[k.split("_")[0]+perturb_surfix])
        return Rules
    
    if "perturbation" in args.current_prompt_meta:
        if args.current_prompt_meta["perturbation"] == "rephrased":
            Rules = formulate_rules(aux_info, politician_mentions, perturb_surfix="_gpt_rephrased")
        if args.current_prompt_meta["perturbation"] == "shuffled":
            Rules = formulate_rules(aux_info, politician_mentions, perturb_surfix="_shuffled")
            if len(Rules) > 3:
                Rules_new = Rules[:2]
                Rules_rest = Rules[2:]
                random.shuffle(Rules_rest)
                Rules = Rules_new + Rules_rest
        if args.current_prompt_meta["perturbation"] == "add_remove":
            Rules = formulate_rules(aux_info, politician_mentions, perturb_surfix="")
            Rules = [R1] + Rules[1:]
    else:
        Rules = [TYPES["interpret"], TYPES["general"]]
        text_lower =  js["text"].lower()
        text_words = [w.replace("'s", "").replace("’s", "") for w in js["text"].lower().split()]

        # Politicians
        politician_mentions = []
        for _, kwl in celeb_kw.items():
            politician_mentions.extend(kwl)
        if any([w in text_words for w in politician_mentions]):
            Rules.append(TYPES['politicians'])

        # Muslims
        if "muslim" in text_lower:
            Rules.append(TYPES['muslim'])

        # political parties
        if any([w in text_lower for w in party_kw]):
            Rules.append(TYPES['party'])

        for k, v in aux_info.items():
            if k.endswith("_GD"):
                k = k.replace("_GD", "")
            if (k in cname_map) and (v['flag']):
                if TYPES['politicians'] not in Rules:
                    Rules.append(TYPES['politicians'])
            if (k in TYPES) and v['flag'] and (TYPES[k] not in Rules):
                Rules.append(TYPES[k])
            if (k.endswith("_t")) and v['flag']:
                if TYPES[k.split("_")[0]] not in Rules:
                    Rules.append(TYPES[k.split("_")[0]])
    
    
    GL = " ".join([f"{i+1}. {rule}" for i, rule in enumerate(Rules)]) if len(Rules) > 1 else Rules[0]
    return GL

def fill_placeholder(tmp, js, args):
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
        return tmp.format(assign_guidelines = assign_guidelines_(js, args)), js
    
    if fewshots in tmp:
        N_ = int(args.n_shots / 2)
        fs_examples = []
        # harmful_samples = random.sample(HARMFUL, N_)
        # harmless_samples = random.sample(HARMLESS, N_)
        for label, pool in zip(["Offensive", "Non-offensive"], [HARMFUL, HARMLESS]):
            for one_sample in random.sample(pool, N_):
                fs_examples.append(f"**Description of the image**: {one_sample} **Classification**: {label}. |")
        return tmp.format(fewshots = "Examples for your reference: " + " ".join(fs_examples)), js
    
    if from_gpt_description in tmp:
        dp_pred_key = 'processed_dependency_prediction'
        if dp_pred_key not in js:
            dp_pred_key = "processed_prediction"
        dp_pred = js.pop(dp_pred_key)
        gold_description = js["gpt_description"]
        if "i'm sorry, i can't" in js["gpt_description"].lower():
            gold_description = dp_pred
        return tmp.format(from_gpt_description = gold_description), js
    
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
            item, js = fill_placeholder(item, js, args)
            ins.append(item)
        if ins_output_format:
            ins.append(ins_output_format)
        text_content = " ".join(" ".join(ins).split())
    if isinstance(prompt, str):
        text_content, js = fill_placeholder(prompt, js, args)
        # text_content = " ".join([text_content, ins_output_format]).strip()
        text_content = " ".join(" ".join([text_content, ins_output_format]).split()).strip()
    
    if js is not None:
        if args.current_model_type == 'llm':
            usr_pt = {"role": "user", "content": text_content}
        if args.current_model_type == 'lmm':
            img_path = js["img"]
            if args.use_resized_img:
                resized_img = "img"
                resized_img = "img_512"
                if args.current_model.startswith('qwen2'):
                    resized_img = "img_512_1280"
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

def prompt_multioff(args, model_tag, js):
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