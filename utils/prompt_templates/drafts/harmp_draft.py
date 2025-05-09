from utils.tool import *
from utils.knowledge.harmp import *

from_raw_data = '{from_raw_data}'
from_dependency = '{from_dependency}'
from_previous_turn = '{from_previous_turn}'
# --------------------------- For Multimodal LMMs --------------------#
VLREASONING = {
    'name': "VLReasoning", 'should_evaluate': False, 'take_image': True,
    'gen_depend_on': None,
    'versions': {
        'CoT': {
            "INS": f'''This is an online meme related to U.S. politics. Classify the meme as either harmful or harmless based on widely accepted values, established knowledge, and social norms. **Now, let's analyze step by step**:'''
        },
    },
    'output_format': {
        'v0': {"INS": '''''', 'post_process_func': post_process_to_remove_gibberish},
    },
}

check_dependency = '''{check_dependency}'''
introduce = f'''This is a meme with an overlaid caption: "{from_raw_data}".'''

GPT_DIRECT_CLASSIFY = {
    'name': "Classify",
    'should_evaluate': False,
    'take_image': True,
    'gen_depend_on': None,
    'versions': {
        'v0': {'INS': f'''Classify this meme as either harmful or harmless.'''},
        'v1': {'INS': f'''Classify this meme as either harmful or harmless.'''},
    },
    'output_format': {
        'v0': {"INS": '''''', 'post_process_func': post_process_to_remove_gibberish}
    },
}

check_aux = "{check_aux}"
DESCRIBE = {
    'name': "Describe", 'should_evaluate': False,'take_image': True,'gen_depend_on': None,
    'versions': {
        'v0': {"INS" : '''What is shown in this meme?'''},
        'v1': {"INS" : '''What is going on in this image? Describe the content of the image without interpreting any underlying implications.'''},
        'v2': {"INS" : '''What is going on in this image?'''},
        'v3': {"INS" : f'''{check_aux} Describe: What is shown in this meme?'''},
        'v4': {"INS" : f'''What is shown in this image?'''},
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
        #'bern': {"INS" : f'''Is {cname_map['bern']} portrayed in the image?'''},
        #'gary': {"INS" : f'''Is {cname_map['gary']} portrayed in the image?'''},
        'party': {"INS" : f'''Is any political party explicitly involved in this image?'''},
        # 'party1': {"INS" : f'''Is any political party involved in this image?'''}
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
        'v1': {"INS": f'''If yes, output "Yes, {cname} is portrayed in the image." Otherwise, output "No."''', 'post_process_func': extract_yes_or_no},
    }
}

# --------------------------- For Unimodal LLMs --------------------#

UNIFY_SYS = '''You are a helpful assistant.''' 
from_Integrate = "{from_Integrate}"
from_data_text = "{from_data_text}"
INTEGRATE = {
    'name': "Integrate", 'should_evaluate': False, 'take_image': False, 'gen_depend_on': [AUX['name'], CELEB['name'], DESCRIBE['name']],
    'versions': {
        'v0': {
            "INS": f'''Given the following information provided about an online meme, and disregarding any information about overlaid text or captions, synthesize and rephrase these information into a unified, detailed description of the image content. Information: "{from_dependency}"'''
        },
        'v1': {
            "INS": [
                f'''Given the following information provided about an online meme, synthesize these information into a coherent, unified, and neutral description of the meme's content. Exclude any assumption about the meme's tone or intent. **Information**: {from_dependency}''',
                f'''{from_data_text}'''
            ]
        },
        'v2': {
            "INS": [
                f'''Given the following information provided about an online meme, synthesize these information into a coherent, unified, and neutral description of the meme's content. DO NOT include any assumption about the meme's tone or intent. DO NOT mention any wartermark on the image. **Information**: {from_dependency}''',
                f'''{from_data_text}'''
            ]
        }
    },
    'output_format': {
        'v0': {"INS": '''''', 'post_process_func': post_process_description},
    }
}


auxt_ins = f'''Given the following description of an image related to U.S. politics, answer the question:'''
AUXT = {
    'name': "Auxt", 'should_evaluate': False, 'take_image': False, 'gen_depend_on': [INTEGRATE['name']],
    'versions': {
        'party': {
            "INS" : [
                auxt_ins,
                f'''Does the image content explicitly target at any political party or political supporters/opponents as a group? **Description of the image**: {from_dependency}''',
            ]
        },
        'lgbt_t': {
            "INS" : [
                auxt_ins,
                f'''Is LGBTQ+ community or LGBTQ+ issue involved in this image content? **Description of the image**: {from_dependency}''',
            ]
        },
        'racial_t': {
            "INS" : [
                auxt_ins,
                f'''Is any reference to individuals of protected groups (e.g., African Americans, Muslims, immigrants, etc.) involved in this image content? **Description of the image**: {from_dependency}''',
            ]
        },
    },
    'output_format': {
        'v0': {"INS": '''Start your response with "Yes," or "No," before giving the explanation.''', 'post_process_func': extract_yes_or_no},
    }
}


EXTRACT = {
    'name': "Extract", 'should_evaluate': False,'take_image': False, 'gen_depend_on': None,
    'versions': {
        'TargetGroup': {
            "INS": [
                '''If you concluded that the content does not involve any specific vulnerable groups, output "Conclusion: No specific protected group being targeted."''',
                '''Otherwise, output "Conclusion: your_choice_from_the_provided_option_list".''',
                '''(Option list:'''
                '''1. Women (Female); 2. LGBTQ Community; 3. People with Disabilities; 4. Muslims and Islamic Culture; 5. Individuals of Middle Eastern Descent; 6. Jewish Individuals; 7. Individuals of African Descent, including African Americans; 8. Other Colored People; 9. People of Asian Descent; 10. Other protected groups not listed.)''',
            ]
        },
    },
    'output_format': {
        'v0': {"INS": '''''', 'post_process_func': fhm_extract_target_group},
    },
}

check_tg = "{check_tg}"
GENERATE_TG_CONTEXT = {
    'name': "GenTGContext", 'should_evaluate': False,'take_image': False,
    'versions': {
        'v0': {'gen_depend_on': [EXTRACT["name"]], "INS": f'''{check_tg}'''}
    },
    'output_format': {
        'v0': {"INS": '''''', 'post_process_func': post_process_to_remove_gibberish},
    },
}

integrate_tg_context = "{integrate_tg_context}"
from_IntegrateTGContext = "{from_IntegrateTGContext}"
INTEGRATE_TG_CONTEXT = {
    'name': "IntegrateTGContext", 'should_evaluate': False,'take_image': False,
    'versions': {
        'v0': {'gen_depend_on': [GENERATE_TG_CONTEXT['name']], "INS": f'''{integrate_tg_context}'''},
    },
    'output_format': {
        'v0': {"INS": '''''', 'post_process_func': post_process_to_remove_gibberish},
    },
}

check_label = "{check_label}"
assign_guidelines = "{assign_guidelines}"
REASONING = {
    'name': "Reasoning", 'should_evaluate': False, 'take_image': False,
    'versions': {
        'ClassifyPerceived': {
            'gen_depend_on': [INTEGRATE['name']],
            'INS': [
                f'''Given the following description of an image-caption pair which may or may not be an online meme,''',
                '''classify the content as 1. "perceived to be hateful by the general public", 2. "perceived to be hateful by specific individuals or groups", or 3. "perceived to be non-hateful by the general public"''',
                '''based on common values, knowledge and social norms.'''
                f'''Image-caption pair: {from_dependency}''',
                f'''The caption overlaid on the image reads "{from_raw_data}".'''
            ]
        },
        'ClassifyWDef': {
            'gen_depend_on': [INTEGRATE['name']],
            'INS': [
                f'''Based on the following definitions: 1. "hateful":. 2. "non-hateful": , classify the following meme content as either hateful or non-hateful.''',
                f'''Meme content: {from_dependency}''',
                f'''The caption overlaid on the image reads "{from_raw_data}".'''
            ]
        },
        'ClassifyWODef': {
            'gen_depend_on': [INTEGRATE['name']],
            'INS': [
                f'''Classify the following meme content as either hateful or non-hateful based on common values, knowledge and social norms.''',
                f'''Meme content: {from_dependency}''',
                f'''The caption overlaid on the image reads "{from_raw_data}".'''
            ]
        },
        'CoT': {
            'gen_depend_on': [INTEGRATE['name']],
            'INS': [
                f'''Given the following description of an image related to U.S. politics,''',
                '''classify the image content as either harmful or harmless based on common values, knowledge, social norms and the provided guidelines.''',
                f'''**Guidelines**: {assign_guidelines}''',
                f'''**Description of the image**: {from_dependency}''',
                # f'''The caption overlaid on the image reads "{from_raw_data}".''',
                '''Now, let's analyze by applying the guidelines one by one:'''
            ]
        },
        'CoT2': {
            'gen_depend_on': [INTEGRATE['name']],
            'INS': [
                f'''Given the following description of an image related to U.S. politics,''',
                '''classify the image content as harmful, mildly harmful or harmless based on common values, knowledge, social norms and the provided guidelines.''',
                f'''**Guidelines**: {assign_guidelines}''',
                f'''**Description of the image**: {from_dependency}''',
                '''Now, let's analyze by applying the guidelines one by one:'''
            ]
        },
        'CoTwhy': {
            'gen_depend_on': [INTEGRATE['name']],
            'INS': f'''{check_label}'''
        },
        # 'CoTwContext': {
        #     'gen_depend_on': [INTEGRATE['name']],
        #     'INS': [
        #         f'''Given the following description of an online meme about US politics,''',
        #         '''classify the meme as either harmful or non-harmful based on common values, knowledge and social norms.''',
        #         f'''Here are some guidelines for your reference: {KNOWLEDGE}''',#some tips
        #         f'''Meme content you need to classify: {from_dependency}''',
        #         f'''The caption overlaid on the meme reads "{from_raw_data}".''',
        #         '''Now, let's think step by step:'''
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
            'INS': f'''If you just classified the image as harmful, output "Conclusion: Harmful." Otherwise, output "Conclusion: Harmless."''',
        },
        'gpt': {
            'gen_depend_on': [GPT_DIRECT_CLASSIFY['name']],
            'INS': f'''If you just classified the meme as harmful, output "Conclusion: Harmful." Otherwise, output "Conclusion: Harmless."''',
        },
        'v1': {
            'gen_depend_on': None,
            'INS': f'''If you just concluded that the meme is likely to be perceived as potentially harmful, output "Conclusion: Harmful." Otherwise, output "Conclusion: Harmless."''',
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
    # old
    # 'lmm_1': {'prompt': {
    #             # 0: {'template': CELEB, "version": "trump", "out_format": 'v0'},

    #             # 0: {'template': CELEB, "version": "USpolitician", "out_format": 'v0'},
    #             # 1: {'template': CELEB, "version": "leaders", "out_format": 'v0'},
    #             # 2: {'template': DESCRIBE, "version": "v0", "out_format": 'v0'},
                
    #             # 0: {'template': CELEB, "version": "trump", "out_format": 'v1'},
    #             # 1: {'template': CELEB, "version": "biden", "out_format": 'v1'},
    #             # 2: {'template': CELEB, "version": "obama", "out_format": 'v1'},
    #             # 3: {'template': CELEB, "version": "hillary", "out_format": 'v1'},
    #             0: {'template': CELEB, "version": "celeb", "out_format": 'v0'},
    #             1: {'template': CELEB, "version": "leaders", "out_format": 'v0'},
    #             2: {'template': DESCRIBE, "version": "v0", "out_format": 'v0'},
    #             3: {'template': AUX, "version": "trump", "out_format": 'v0'},
    #             4: {'template': AUX, "version": "biden", "out_format": 'v0', "load_from_prestep": True},
    #             5: {'template': AUX, "version": "obama", "out_format": 'v0', "load_from_prestep": True},
    #             6: {'template': AUX, "version": "hillary", "out_format": 'v0', "load_from_prestep": True},
    #             7: {'template': AUX, "version": "b&o", "out_format": 'v0', "load_from_prestep": True},
    #             # 8: {'template': AUX, "version": "party1", "out_format": 'v0', "load_from_prestep": True},
    #             8: {'template': AUX, "version": "bern", "out_format": 'v0', "load_from_prestep": True},
    #             9: {'template': AUX, "version": "gary", "out_format": 'v0', "load_from_prestep": True},
    #         },
    #         'multi-turn': False},

    # 'lmm_2': {'prompt': {
    #             0: {'template': AUX, "version": "trump", "out_format": 'v0'},
    #             1: {'template': AUX, "version": "biden", "out_format": 'v0', "load_from_prestep": True},
    #             2: {'template': AUX, "version": "obama", "out_format": 'v0', "load_from_prestep": True},
    #             3: {'template': AUX, "version": "hillary", "out_format": 'v0', "load_from_prestep": True},
    #             4: {'template': AUX, "version": "b&o", "out_format": 'v0', "load_from_prestep": True},
    #             5: {'template': AUX, "version": "party1", "out_format": 'v0', "load_from_prestep": True},
    #         },
    #         'multi-turn': False},
    'llm_1': {
        'prompt': {
            0: {'template': INTEGRATE, "version": "v1", "out_format": 'v0', "load_from_prestep": True, "return_prestep_path": False},    
            # 1: {'template': AUXT, "version": "party", "out_format": 'v0',
            # 'max_new_tokens': 256}, 
        },
        'multi-turn': False
    },
}

# ******************************************************************************************* # 
d0 = {
    'llm_2': {
        'multi-turn': True,
        'prompt': {
            0: {'template': REASONING, "version": "ClassifyPerceived", "out_format": 'v0'},
            1: {'template': DECISION, "version": "v0", "out_format": 'v0'},
        }
    }
}

d1 = {
    'llm_2': {
        'multi-turn': True,
        'prompt': {
            0: {'template': REASONING, "version": "ClassifyWDef", "out_format": 'v0'},
            1: {'template': DECISION, "version": "v1", "out_format": 'v0'},
        }
    }
}

d2 = {
    'llm_2': {
        'multi-turn': True,
        'prompt': {
            0: {'template': REASONING, "version": "ClassifyWODef", "out_format": 'v0'},
            1: {'template': DECISION, "version": "v2", "out_format": 'v0'},
        }
    }
}

d3 = {
    'llm_2': {
        'multi-turn': True,
        'prompt': {
            0: {'template': REASONING, "version": "CoT", "out_format": 'v0'},
            1: {'template': DECISION, "version": "v3", "out_format": 'v0'},
        }
    }
}


GPT = {
    'lmm': {'prompt': {
                0: {'template': GPT_DIRECT_CLASSIFY, "version": "v0", "out_format": 'v0'},
            },
            'multi-turn': False},
    'llm': {
        'multi-turn': True,
        'prompt': {
            1: {'template': DECISION, "version": "gpt", "out_format": 'v0'},
        }
    }
}

d6 = {
    'llm_2': {
        'multi-turn': True,
        'prompt': {
            # 0: {'template': REASONING, "version": "CoTwContext", "out_format": 'v0'},
            0: {'template': REASONING, "version": "CoT", "out_format": 'v0', 'max_new_tokens': 1536},# "load_from_prestep": True, "return_prestep_path": True
            1: {'template': DECISION, "version": "v0", "out_format": 'v0'},
        }
    }
}

d6m = {
    'llm_2': {
        'multi-turn': True,
        'prompt': {
            # 0: {'template': REASONING, "version": "CoTwContext10", "out_format": 'v0'},
            # 1: {'template': DECISION, "version": "v3", "out_format": 'v0'},
            0: {'template': REASONING, "version": "TargetG2", "out_format": 'v0'},
            1: {'template': EXTRACT, "version": "TargetGroup", "out_format": 'v0'},
        }
    },
    'llm_3': {
        'multi-turn': True,
        'prompt': {
            2: {'template': GENERATE_TG_CONTEXT, "version": "v0", "out_format": 'v0'},
        }
    },
    'llm_4': {
        'multi-turn': True,
        'prompt': {
            3: {'template': INTEGRATE_TG_CONTEXT, "version": "v0", "out_format": 'v0', 'new_conversation': True},
            4: {'template': REASONING, "version": "CoTwTGContext", "out_format": 'v0', 'new_conversation': True},
            5: {'template': DECISION, "version": "v3", "out_format": 'v0'},
        }
    }
}


D5 = {
    'lmm': {
        'prompt': {
            0: {'template': VLREASONING, "version": "CoT", "out_format": 'v0'},
            1: {'template': DECISION, "version": "v4", "out_format": 'v0'}
        },
        'multi-turn': True
    }
}

WhyHarm = {
    'llm_2': {
        'multi-turn': False,
        'prompt': {
            0: {'template': REASONING, "version": "CoTwhy", "out_format": 'v0'},
        }
    }
}
D0 = dict(**M2T, **d0)
D1 = dict(**M2T, **d1)
D2 = dict(**M2T, **d2)
D3 = dict(**M2T, **d3)
D6 = dict(**M2T, **d6)
D6m = dict(**M2T, **d6m)
why = dict(**M2T, **WhyHarm)

# ******************************************************************************************* # 

HARMP_PROMPT_SCHEMES = {
    'B1': B1,
    'GPT': GPT,
    'M2T': M2T,
    'D0': D0,
    'D1': D1,
    'D2': D2,
    'D3': D3,
    'D5': D5,
    'D6': D6,
    'D6m': D6m,
    'why': why
}

def assign_guidelines_(js):
    aux_info = js["aux_info"]
    # TYPES['interpret'],
    basic = [TYPES["general"]]
    
    assert "processed_prediction" in js
    text_lower = js["processed_prediction"].lower()
    text_words = [w.replace("'s", "").replace("’s", "") for w in text_lower.split()]
    # text_lower =  js["text"].lower()
    # text_words = [w.replace("'s", "").replace("’s", "") for w in js["text"].lower().split()]
    # # Politicians
    politician_mentions = []
    for _, kwl in celeb_kw.items():
        politician_mentions.extend(kwl)
    if any([w in text_words for w in politician_mentions]):
        basic.append(TYPES['politicians'])
    
    # political parties
    # if any([w in text_lower for w in party_kw]):
    #     basic.append(TYPES['party'])

    for k, v in aux_info.items():
        if (k in cname_map) and (v['flag']):
            if TYPES['politicians'] not in basic:
                basic.append(TYPES['politicians'])
            if (k in ['biden', 'b&o']) and (TYPES[cname_map['biden']] not in basic):
                basic.append(TYPES[cname_map['biden']]) 
        if (k =='party') and v['flag'] and (TYPES[k] not in basic):
            basic.append(TYPES[k])
    #basic.reverse()
    gl = " ".join([f"{i+1}. {rule}" for i, rule in enumerate(basic)]) if len(basic) > 1 else basic[0]
    return gl

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
    if check_aux in tmp:
        assert "aux_info" in js
        politicians = []
        for k, v in js["aux_info"].items():
            if (k in cname_map) and v['flag']:
                if k == "b&o":
                    politicians.extend(['biden', 'obama'])
                else:
                    politicians.append(k)
        politicians = list(set(politicians))
        poli_template = '''This is a meme featuring {pt}.'''
        if len(politicians) == 0:
            return tmp.format(check_aux = "").strip(), js
        if len(politicians) == 1:
            poli_text = cname_map[politicians[0]]
        if len(politicians) == 2:
            poli_text = f"{cname_map[politicians[0]]} and {cname_map[politicians[1]]}"
        if len(politicians) > 2:
            poli_text = ", ".join([cname_map[p] for p in politicians[:-1]]) + f" and {cname_map[politicians[-1]]}"
            poli_text = " ".join(poli_text.split())
        poli_info = poli_template.format(pt = poli_text)
        return tmp.format(check_aux = poli_info), js

    if from_data_text in tmp:
        if js['text']:
            prompt = f'''Also, some overlaid text in the image is recognized as: "{js['text']}"'''
        else:
            prompt = ""
        return tmp.format(from_data_text = prompt), js
    if check_label in tmp:
        if js['label']:
            dp_pred_key = 'processed_dependency_prediction'
            if dp_pred_key not in js:
                dp_pred_key = "processed_prediction"
            dp_pred = js.pop(dp_pred_key)
            assert isinstance(dp_pred, str)
            tmp = f'''Given the following description of an image, analyze why this image is considered "harmful" based on common values, knowledge and social norms. **Description**: {dp_pred} **Now, let's analyze step by step**:'''
            return tmp, js
        else:
            return "", None
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
        text_content = " ".join([text_content, ins_output_format]).strip()
    
    if js is not None:
        if args.current_model_type == 'llm':
            usr_pt = {"role": "user", "content": text_content}
        if args.current_model_type == 'lmm':
            #img_path = js['img_mask'] if args.use_mask_img else js['img']
            img_path = js["img"]
            if args.use_resized_img:
                img_path = js["img_768"] if (("img_768" in js) and js["img_768"]) else js["img"]
                if args.current_model.startswith('qwen2'):
                    img_path = js["img_768_896"] if (("img_768_896" in js) and js["img_768_896"]) else js["img"]
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
        js['seq_in'] = T5_PROMPTS[0].format(segment=text, definitions=fal_def_str.lower())
        #js['seq_in'] = T5_PROMPTS[0].format(segment=text, definitions=fal_def_str.lower(), fallacies=fal_name_str.lower())
    else:
        js = format_chat(args, js)
    return js

