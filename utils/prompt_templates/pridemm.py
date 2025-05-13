from utils.knowledge.pridemm import *
from utils.tool import *
from_raw_data = '{from_raw_data}'
from_dependency = '{from_dependency}'
from_previous_turn = '{from_previous_turn}'
# --------------------------- For Multimodal LMMs --------------------#
Introduce = '''This is an online meme related to LGBTQ+ pride movements.'''
VLREASONING = {
    'name': "VLReasoning", 'should_evaluate': False, 'take_image': True,
    'gen_depend_on': None,
    'versions': {
        'CoT': {
            "INS": f'''{Introduce} Classify the meme as either harmful or harmless to: (1) the LGBTQ+ community and its supporters, or (2) the specific individual(s) or organization(s) involved, based on widely accepted values, established knowledge, cultural understanding, and social norms. Now, let's analyze step by step:'''
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
        'v0': {
            "INS" : '''This is an online meme related to LGBTQ+ pride movement. What is this meme about? Note: DO NOT ASSUME the nature of the meme's tone and intent as humorous or lighthearted. Describe in a neutral tone.''',
        },
    },
    'output_format': {
        'v0': {"INS": "", 'post_process_func': post_process_visual_describe},
    }
}

Ignore = '''Ignore any overlaid text or caption.'''
check_dependency = '''{check_dependency}'''
HUMAN = {
    'name': "Human", 'should_evaluate': False, 'take_image': True, 'gen_depend_on': None,
    'versions': {
        'v0': {"INS" : f'''Is there any human subject in the image? {Ignore}'''},
    },
    'output_format': {
        'v0': {"INS": '''Start your response with "Yes," or "No," before giving any further explanation.''', 'post_process_func': extract_yes_or_no}
    }
}

RACE = {
    'name': "Race", 'should_evaluate': False, 'take_image': True, 'gen_depend_on': [HUMAN['name']],
    'versions': {
        'v0': {"INS" : f'''{check_dependency}What is/are the perceived race(s) of the human subject(s) in the image? {Ignore}'''},
    },
    'output_format': {
        'v0': {"INS": '''''', 'post_process_func': False}
    }
}

GENDER = {
    'name': "Gender", 'should_evaluate': False, 'take_image': True, 'gen_depend_on': [HUMAN['name']],
    'versions': {
        'v0': {"INS" : f'''{check_dependency}What is/are the gender(s) of the human subject(s) in the image? {Ignore}'''},
    },
    'output_format': {
        'v0': {"INS": '''''', 'post_process_func': False},
    }
}

APPEARANCE = {
    'name': "Appearance", 'should_evaluate': False, 'take_image': True, 'gen_depend_on': [HUMAN['name']],
    'versions': {
        'v0': {"INS" : f'''{check_dependency}What are the distinctive physical appearance characteristics of the human subject(s) in the image? {Ignore} Describe within three sentences.'''},
        'v1': {"INS" : f'''{check_dependency}What are the distinctive physical appearance characteristics of the human subject(s) in the image? {Ignore}'''},
    },
    'output_format': {
        'v0': {"INS": '''''', 'post_process_func': False},
    }
}
# --------------------------- For Unimodal LLMs --------------------#

UNIFY_SYS = '''You are a helpful assistant.''' #'''You are an expert in meme content comprehension and hatefulness detection.'''
from_data_text = '''{from_data_text}'''
from_Integrate = "{from_Integrate}"
INTEGRATE = {
    'name': "Integrate", 'should_evaluate': False, 'take_image': False, 
    'gen_depend_on': [HUMAN['name'], RACE['name'], GENDER['name'], APPEARANCE['name'], DESCRIBE['name']],
    'versions': {
        'v0':{
            "INS": [
                f'''Given the following information provided about an online meme, synthesize and rephrase these information into a unified, coherent, and neutral description of the meme content. DO NOT mention the meme's tone and intent as humorous or light-hearted in the description. **Information**: {from_dependency}''',
                f'''{from_data_text}''',
                # f'''The overlaid caption or text recognized in the meme reads: "{from_raw_data}".''',
            ]
        }    
    },
    'output_format': {
        'v0': {"INS": '''''', 'post_process_func': post_process_to_remove_gibberish},
    }
}

check_if_has_individual = '''{check_if_has_individual}'''
check_if_is_lgbt_individual = '''{check_if_is_lgbt_individual}'''
AUX = {
    'name': "Aux", 'should_evaluate': False, 'take_image': False,
    'versions': {
        'subgroup': {
            'gen_depend_on': None,
            "INS": [
                '''If you just concluded that the meme content particularly mentions, references or implicitly implies specific LGBTQ+ subgroup(s), output: "Conclusion: Your choice of the most directly referenced subgroup from the option list. Otherwise, output "Conclusion: No specific subgroup referenced or implied." ''',
                '''**Option list**:'''
                '''1. Gay; 2. Trans women; 3. Trans men; 4. (Semi-) Bisexual individuals; 5. Non-binary individuals; 6. Other subgroup not listed.''',
            ]
        },
        'hateTarget': {
            'gen_depend_on': None,
            "INS": f'''Output "Conclusion: your_choice_from_the_option_list". **Option list**: {TG_LABEL}''',
        },
        'individual': {
            'gen_depend_on': None,
            "INS": '''If you just concluded that the meme does involve a specific individual, output "Yes." Otherwise, just output "No.".''',
        },
        'LGBTQindividual': {
            'gen_depend_on': None,
            "INS": f'''{check_if_has_individual}''',
        },
        'organization': {
            'gen_depend_on': None,
            "INS": '''If you just concluded that the meme addresses or discusses organizational involvement in LGBTQ+ issues, output "Yes." Otherwise, just output "No.".''',
        },
        'country': {
            'gen_depend_on': [INTEGRATE['name']],
            "INS": [
                f'''Given the following description of an online meme related to LGBTQ+ movements,''',
                '''does the meme explicitly reference any country or region where LGBTQ+ identities or advocacy are discouraged?''',
                f'''**Description of the meme content**: {from_dependency}''',
            ],
        },
        'politic': {
            'gen_depend_on': [INTEGRATE['name']],
            "INS": [
                f'''Given the following description of an online meme related to LGBTQ+ movements,''',
                '''does the meme explicitly involve or mention politicians, political figures, political parties, ideologies, or groups?''',
                f'''**Description of the meme content**: {from_dependency}''',
            ],
        },
        'company1': {
            'gen_depend_on': [INTEGRATE['name']],
            "INS": [
                f'''Given the following description of an online meme related to LGBTQ+ movements,''',
                '''does the meme explicitly touch on topics about corporate involvement in LGBTQ+ movements?''',
                f'''**Description of the meme content**: {from_dependency}''',
            ],
        },
        'company2': {
            'gen_depend_on': [INTEGRATE['name']],
            "INS": [
                f'''Given the following description of an online meme related to LGBTQ+ movements,''',
                '''does the meme make any general reference to companies, corporations, or brands?''',
                f'''**Description of the meme content**: {from_dependency}''',
            ],
        },
        'company3': {
            'gen_depend_on': [INTEGRATE['name']],
            "INS": [
                f'''Given the following description of an online meme related to LGBTQ+ movements,''',
                '''does the meme explicitly involve or mention any companies, corporations, or brands?''',
                f'''**Description of the meme content**: {from_dependency}''',
            ],
        },
        'self': {
            'gen_depend_on': [INTEGRATE['name']],
            "INS": [
                f'''Given the following description of an online meme related to LGBTQ+ movements,''',
                '''is this meme a self-reflection on the introspective experiences, struggles, or identity exploration of LGBTQ+ individuals from their own perspective?''',
                f'''**Description of the meme content**: {from_dependency}''',
            ],
        },
        'media': {
            'gen_depend_on': [INTEGRATE['name']],
            "INS": [
                f'''Given the following description of an online meme related to LGBTQ+ movements,''',
                '''does the meme explicitly reference any streaming media platforms?''',
                f'''**Description of the meme content**: {from_dependency}''',
            ],
        },
        'religion': {
            'gen_depend_on': [INTEGRATE['name']],
            "INS": [
                f'''Given the following description of an online meme related to LGBTQ+ movements,''',
                '''does the meme explicitly involve any religion or religious beliefs?''',
                f'''**Description of the meme content**: {from_dependency}''',
            ],
        },
        'children': {
            'gen_depend_on': [INTEGRATE['name']],
            "INS": [
                f'''Given the following description of an online meme related to LGBTQ+ movements,''',
                '''does the meme explicitly involve topics related to children, youth, or education?''',
                f'''**Description of the meme content**: {from_dependency}''',
            ],
        },
    },
    'output_format': {
        'subgroup': {"INS": '''''', 'post_process_func': pridemm_extract_subgroup},
        "hateTarget": {"INS": '''''', 'post_process_func': pridemm_extract_target},
        'y&n': {"INS": '''Start your response with "Yes," or "No," before giving any further explanation.''', 'post_process_func': extract_yes_or_no},
        'YN': {"INS": '''''', 'post_process_func': extract_yes_or_no}
    }
}

assign_prompt_by_target = '''{assign_prompt_by_target}'''
make_guidelines = '''{make_guidelines}'''
PP_CoT_INS = '''Now, let's analyze by applying the guidelines one by one:'''
cot_ins = '''Now, let's analyze step by step:'''
meme2text = f'''**Meme content you need to classify**: {from_dependency}'''
BASELINE_CLASSIFY_INS = f'''Given the following description of an online meme related to LGBTQ+ pride movements, classify the content as either harmful or harmless to: (1) the LGBTQ+ community and its supporters, or (2) the specific individual(s) or organization(s) involved, based on widely accepted social norms, values and cultural understanding.'''
REASONING = {
    'name': "Reasoning", 'should_evaluate': False, 'take_image': False,
    'versions': {
        'CoTxTarget': {
            'gen_depend_on': [INTEGRATE['name']],
            'INS': [
                f'''Given the following description of an online meme related to LGBTQ+ pride movements,''',
                f'''{assign_prompt_by_target}''',
                meme2text,
                PP_CoT_INS
            ]
        },
        'subgroup':{
            'gen_depend_on': [INTEGRATE['name']],
            "INS": [
                f'''Given the following description of an online meme related to LGBTQ+ pride movements,''',
                '''analyze: what specific subgroup(s) within the LGBTQ+ community is/are particularly mentioned, referenced or implicitly implied in the meme content?''',
                '''**Guidelines**:''',
                '''A. If the content does not appear to imply, mention or reference any specific LGBTQ+ subgroups but instead refers to the LGBTQ+ community as a whole, just output "No specific subgroup referenced."''',
                '''B. Otherwise, choose the mentioned, referenced or implied subgroup(s) from the provided list (you may choose multiple options if there are more than one subgroup being referenced):''',
                '''1. Gay; 2. Trans women; 3. Trans men; 4. (Semi-) Bisexual individuals; 5. Non-binary individuals; 6. Other subgroup not listed.''',
                f'''**Meme content you need to analyze**: {from_dependency}''',
                '''**Now, let's analyze step by step**:'''
            ]
        },
        'individual': {
            'gen_depend_on': [INTEGRATE['name']],
            "INS": [
                f'''Given the following description of an online meme related to LGBTQ+ movements, analyze: Does the meme content involve any specific individual? **Guidelines**: {Individual_GL}''',
                f'''**Description of the meme content**: {from_dependency}''',
                '''**Now, let's analyze step by step**:'''
            ]
        },
        'organization': {
            'gen_depend_on': [INTEGRATE['name']],
            "INS": [
                f'''Given the following description of an online meme related to LGBTQ+ movements, analyze: Does the meme content address or discuss organizational involvement related to LGBTQ+ issues? **Guidelines**: {Organization_GL}''',
                f'''**Description of the meme content**: {from_dependency}''',
                '''**Now, let's analyze step by step**:'''
            ]
        },
        'hateTarget': {
            'gen_depend_on': [INTEGRATE['name']],
            "INS": [
                f'''Given the following description of an online meme related to LGBTQ+ movements, analyze: What is the meme's target subject? Select the most appropriate category from these options: 1. Undirected; 2. LGBTQ+ Community; 3. Specific Individual; 4. Organization. **Target Classification Guidelines**: {TG_GL}''',
                f'''**Description of the meme content**: {from_dependency}''',
                cot_ins
            ]
        },
        'hateTarget*': {
            'gen_depend_on': [INTEGRATE['name']],
            "INS": [
                f'''Given the following description of an online meme related to LGBTQ+ movements, analyze: What is the meme's target subject? Select the most appropriate category from these options: {TG_LABEL} **Guidelines**: {TG_GL}''',
                f'''**Description of the meme content**: {from_dependency}''',
                cot_ins
            ]
        },
        'CoT': {
            'gen_depend_on': [INTEGRATE['name']],
            'INS': [
                BASELINE_CLASSIFY_INS,
                meme2text,
                cot_ins
            ]
        },
        'CoT*': {
            'gen_depend_on': [INTEGRATE['name']],
            'INS': [
                f'''Given the following description of an online meme related to LGBTQ+ pride movements, classify the content as either harmful or harmless to: (1) the LGBTQ+ community and its supporters, or (2) the specific individual(s) or organization(s) involved, based on widely accepted social norms, values, cultural understanding and the provided guidelines.''',
                f'''**Guidelines**: {make_guidelines}''',
                meme2text,
                PP_CoT_INS
            ]
        },
        'CoTqw3': {
            'gen_depend_on': [INTEGRATE['name']],
            'INS': [
                BASELINE_CLASSIFY_INS,
                meme2text
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
        'v0': {'INS': f'''{Introduce} Classify the meme as either harmful or harmless to: (1) the LGBTQ+ community and its supporters, or (2) the specific individual or organization involved.'''},
    },
    'output_format': {
        'v0': {"INS": '''''', 'post_process_func': post_process_to_remove_gibberish}
    },
}

GPT_DESCRIBE = {
    'name': "Describe", 'should_evaluate': False, 'take_image': True, 'gen_depend_on': None,
    'versions': {
        'v0': {'INS': f'''{Introduce} Describe the visual content of the meme without interpretation. If there is any overlaid caption, transcribe it exactly as shown without paraphrasing.'''},
    },
    'output_format': {
        'v0': {"INS": '''''', 'post_process_func': post_process_to_remove_gibberish}
    },
}

assign_decision_prompt_by_target = '''{assign_decision_prompt_by_target}'''
DECISION = {
    'name': "Decision", 'should_evaluate': True, 'take_image': False,
    'versions': {
        'v0': {
            'gen_depend_on': None,
            'INS': f'''If you just classified the meme content as harmful (either explicitly or implicitly), output "Conclusion: Harmful." Otherwise, output "Conclusion: Harmless."''',
        },
        'tg': {
            'gen_depend_on': None,
            'INS': f'''{assign_decision_prompt_by_target}''',
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
        'v0': {"INS": '''''', 'post_process_func': extract_classification_label},
    }
}

def assign_decision_extract_by_target(js):
    assert "aux_info" in js
    aux_info = js["aux_info"]
    assert "individual" in aux_info
    if aux_info["individual"]["flag"] == 1:
        #assert aux_info["individual"]["flag"] == 1
        if aux_info["hateTarget"] == "individual":
            if aux_info["LGBTQindividual"]['flag'] == 0:
                # Non-LGBTQ+ individual
                plh = "individual"
                return f'''If you just classified the meme content as harmful (either explicitly or implicitly) to the public image of the specific {plh}, output "Conclusion: Harmful." Otherwise, output "Conclusion: Harmless."'''
            else:
                plh = "LGBTQ+ individual"
                return f'''If you just classified the meme content as hurtful (either explicitly or implicitly) to the {plh}, output "Conclusion: Hurtful." Otherwise, output "Conclusion: Non-hurtful."'''
            # return f'''If you just classified the meme content as hurtful (either explicitly or implicitly) to the {plh}, output "Conclusion: Hurtful." Otherwise, output "Conclusion: Non-hurtful."'''
    else:
        #if aux_info["organization"] is not None:
        if (aux_info["hateTarget"] in ["organization"]):# and (aux_info["organization"]["flag"] == 1)
            return f'''If you just classified the meme content as harmful (either explicitly or implicitly) to the public image of the organization, output "Conclusion: Harmful." Otherwise, output "Conclusion: Harmless."'''
    return f'''If you just classified the meme content as harmful (either explicitly or implicitly), output "Conclusion: Harmful." Otherwise, output "Conclusion: Harmless."'''


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
            1: {'template': RACE, "version": "v0", "out_format": 'v0'},
            2: {'template': GENDER, "version": "v0", "out_format": 'v0'},
            3: {'template': APPEARANCE, "version": "v0", "out_format": 'v0'},
            4: {'template': APPEARANCE, "version": "v1", "out_format": 'v0'},
            5: {'template': DESCRIBE, "version": "v0", "out_format": 'v0'},
        },
        'multi-turn': False
    },
    'llm_1': {
        'prompt': {
            0: {'template': INTEGRATE, "version": "v0", "out_format": 'v0'},    
        },
        'multi-turn': False
    },
}

# ******************************************************************************************* # 
# Unimodal baseline: Inference with LLM
b2 = {
    'llm_2': {
        'multi-turn': True,
        'prompt': {
            0: {'template': REASONING, "version": "CoT", "out_format": 'v0'},
            1: {'template': DECISION, "version": "v0", "out_format": 'v0'},
        }
    }
}

b2_qw3 = {
    'llm_2': {
        'multi-turn': True,
        'prompt': {
            0: {'template': REASONING, "version": "CoTqw3", "out_format": 'v0'},
            1: {'template': DECISION, "version": "v0", "out_format": 'v0'},
        }
    }
}

p1 = {
    'llm_2': {
        'multi-turn': False,
        'prompt': {
            0: {'template': AUX, "version": "country", "out_format": 'y&n'},
            1: {'template': AUX, "version": "politic", "out_format": 'y&n', "load_from_prestep": True, "return_prestep_path": True},
            2: {'template': AUX, "version": "company1", "out_format": 'y&n', "load_from_prestep": True, "return_prestep_path": True},
            3: {'template': AUX, "version": "company2", "out_format": 'y&n', "load_from_prestep": True, "return_prestep_path": True},
            4: {'template': AUX, "version": "company3", "out_format": 'y&n', "load_from_prestep": True, "return_prestep_path": True},
            5: {'template': AUX, "version": "self", "out_format": 'y&n', "load_from_prestep": True, "return_prestep_path": True},
            # 0: {'template': AUX, "version": "children", "out_format": 'y&n'},
            # 1: {'template': AUX, "version": "religion", "out_format": 'y&n', "load_from_prestep": True, "return_prestep_path": True},
            # 2: {'template': AUX, "version": "media", "out_format": 'y&n', "load_from_prestep": True, "return_prestep_path": True},
        }
    },
    'llm_3': {
        'multi-turn': True,
        'prompt': {
            0: {'template': REASONING, "version": "subgroup", "out_format": 'v0', "load_from_prestep": True, "return_prestep_path": True},
            1: {'template': AUX, "version": "subgroup", "out_format": 'subgroup'},
        }
    },
    'llm_4': {
        'multi-turn': True,
        'prompt': {
            0: {'template': REASONING, "version": "individual", "out_format": 'v0', "load_from_prestep": True, "return_prestep_path": True},
            2: {'template': AUX, "version": "individual", "out_format": 'YN'},
            3: {'template': AUX, "version": "LGBTQindividual", "out_format": 'YN'},
        }
    },
    'llm_5': {
        'multi-turn': True,
        'prompt': {
            0: {'template': REASONING, "version": "organization", "out_format": 'v0', "load_from_prestep": True, "return_prestep_path": True},
            4: {'template': AUX, "version": "organization", "out_format": 'YN'},
        }
    },
    'llm_6': {
        'multi-turn': True,
        'prompt': {
            0: {'template': REASONING, "version": "hateTarget*", "out_format": 'v0', "load_from_prestep": True, "return_prestep_path": True},
            5: {'template': AUX, "version": "hateTarget", "out_format": 'hateTarget'},
            6: {'template': REASONING, "version": "CoTxTarget", "out_format": 'v0', 'new_conversation': True, 'depend_on_prestep': True, 'max_new_tokens': 1536},
            7: {'template': DECISION, "version": "tg", "out_format": 'v0'}
        }
    },
    # 'llm_7': {
    #     'multi-turn': True,
    #     'prompt': {
    #         6: {'template': REASONING, "version": "CoTxTarget", "out_format": 'v0', 'new_conversation': True, 'depend_on_prestep': True, 'max_new_tokens': 1536, 'batch_size': 14},
    #         7: {'template': DECISION, "version": "tg", "out_format": 'v0', 'batch_size': 12}
    #     }
    # },
}

PP = dict(**M2T, **p1)
B2 = dict(**M2T, **b2)
B2qw3 = dict(**M2T, **b2_qw3)
# ******************************************************************************************* # 

PrideMM_PROMPT_SCHEMES = {
    'M2T': M2T,
    'B1': B1,
    'B2': B2,
    'GPT': GPT,
    'PP': PP,
    'B2qw3': B2qw3,
    'GPT_DESCRIBE': GPT_describe
}

def assign_unified_guidelines(js):
    assert "aux_info" in js
    aux_info = js["aux_info"]
    Rules = GL_INONE
    if aux_info["self"]["flag"]:
        Rules.append(TYPES["self"])
    GL = f"\n".join([f"{rid+1}. {rule}" for rid, rule in enumerate(Rules)])
    return GL

def assign_guidelines(js):
    assert "aux_info" in js
    aux_info = js["aux_info"]
    Rules = [R_interpret, R_stance, R_explicit, R_implicit_new]
    R_harmful_new_ = R_harmful_new
    
    # # Subgroup
    aux_subg = aux_info["subgroup"]
    r_subgroup = ""
    if aux_subg:
        if (len(aux_subg) == 1):
            one_sg = aux_subg[0]
            examples = ""
            if "subgroups" in one_sg.lower():
                examples = TYPES["LGBTQ+ subgroups"]
            if any([w in one_sg.lower() for w in ["bisexual", "bi-sexual"]]):
                examples = TYPES["(Semi-) Bisexual individuals"]
            r_subgroup = f'''{examples}'''
    
    if r_subgroup:
        R_harmful_new_ = f"{R_harmful_new_} {r_subgroup}"
    
    # Specific aspects: country, politic, company
    issues = []
    for k, item in aux_info.items():
        if k in ['country', 'politic']:
            if isinstance(item, dict) and item["flag"]:
                topic = TYPES[k]['topic']
                examples = TYPES[k]['examples']
                issues.append(f"{examples}")
    if any([item["flag"] for k, item in aux_info.items() if k.startswith("company")]):
        topic = TYPES["company"]['topic']
        examples = TYPES["company"]['examples']
        issues.append(f"{examples}")
    if issues:
        R_harmful_new_ = " ".join([R_harmful_new_, f" ".join(issues)])
    
    Rules.append(R_harmful_new_)

    # # Harmless
    if aux_info["self"]["flag"]:
        Rules.append(TYPES["self"])
    
    Rules.append(R_harmless_ori)
    ######################2025-05-13######################
    Rules.append(R_news)
    ######################2025-05-13######################

    GL = f"\n".join([f"{rid+1}. {rule}" for rid, rule in enumerate(Rules)])
    return GL

surfix = '''according to widely accepted social norms, values, cultural understanding, and the provided guidelines.'''
def assign_prompt_INS_by_target(js):
    assert "aux_info" in js
    aux_info = js["aux_info"]
    use_default = False
    assert "individual" in aux_info
    if aux_info["individual"]["flag"] == 1:
        if aux_info["hateTarget"] == "individual":
            if aux_info["LGBTQindividual"]['flag'] == 0:
                # Non-LGBTQ+ individual
                plh = "individual"
                Rules = [Individual_GL, R_interpret, R_stance_individual, R_explicit_individual, R_implicit_individual, R_harmless_ori]
                Rules = [Individual_GL, R_interpret, R_stance_individual, R_explicit_individual, R_implicit_individual_harmful, R_harmless_ori]
                classify_ins = f'''classify the content as either harmful or harmless to the public image of the specific {plh} involved, {surfix}'''
            else:
                plh = "LGBTQ+ individual"
                Rules = [R_interpret, R_stance_lgbt_individual, R_explicit_individual, R_implicit_lgbt_individual, R_harmful_lgbt_individual, R_harmless_ori]

                Rules = [R_interpret, R_stance_lgbt_individual, R_explicit_individual, R_implicit_lgbt_individual, R_harmful_lgbt_individual, R_harmless_ori, R_news]
                classify_ins = f'''classify the content as either hurtful or non-hurtful to the specific {plh} involved, {surfix}'''
            # classify_ins = f'''classify the content as either hurtful or non-hurtful to the specific {plh} involved, {surfix}'''
        else:
            use_default = True
    else:
        if (aux_info["hateTarget"] in ["organization"]):# and (aux_info["organization"]["flag"] == 1)
            Rules = [R_organization, R_interpret, R_explicit_organization, R_implicit_organization, R_harmful_organization, R_harmless_ori]
            classify_ins = f'''classify the content as either harmful or harmless to the public image of the organization(s) involved, {surfix}'''
        else:
            use_default = True
    if use_default:
        Rules = assign_guidelines(js)
        classify_ins = '''classify the content as either harmful or harmless to LGBTQ+ community and supporters, based on widely accepted social norms, values, cultural understanding, and the provided guidelines.'''
    
    if isinstance(Rules, list):
        GL = f" ".join([f"{rid+1}. {rule}" for rid, rule in enumerate(Rules)])
    else:
        GL = Rules
    prompt = " ".join([classify_ins, f"Guidelines: {GL}"])
    return prompt


plh = "{plh}"
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
            prompt = f'''The overlaid caption or text recognized in the meme reads: "{js['text']}".'''
        else:
            prompt = ""
        return tmp.format(from_data_text = prompt), js

    if make_guidelines in tmp:
        return tmp.format(make_guidelines = assign_unified_guidelines(js)), js
    if assign_prompt_by_target in tmp:
        return assign_prompt_INS_by_target(js), js
    if assign_decision_prompt_by_target in tmp:
        return assign_decision_extract_by_target(js), js
     
    if check_if_has_individual in tmp:
        assert "aux_info" in js
        aux_info = js["aux_info"]
        #print(list(aux_info.keys()))
        a = f'''Output "No.".'''
        if aux_info["individual"]["flag"] == 1:
            a = f'''Is this specific individual an LGBTQ+ individual? Start your response with "Yes," or "No," before giving any further explanation.'''
        # if "individual" in list(aux_info.keys()):
        #     if aux_info["individual"] is not None:
        #         assert aux_info["individual"]["flag"] == 1
        #         a = f'''Is this specific individual an LGBTQ+ individual? Start your response with "Yes," or "No," before giving any further explanation.'''           
        return a, js
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
    text_content = " ".join(text_content.split())

    if js is not None:
        if args.current_model_type == 'llm':
            usr_pt = {"role": "user", "content": text_content}
        if args.current_model_type == 'lmm':
            img_path = js["img"]
            if args.use_resized_img:
                resized_img = "img"
                #resized_img = "img_512"
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
            if args.current_prompt_meta['version'] == "LGBTQindividual":
                dialog = js['chat_history'][:-1] + [usr_pt]  

        
        js['chat_history'] = dialog
        js['task'] = args.task
        js['img_history'] = img_history
    return js

def prompt_pridemm(args, model_tag, js):
    """
    input:
        js is one data sample in the format of dictionary
        js['text'] is a string
    """
    if model_tag.startswith('t5'):
        text = js['text'].lower()    
    else:
        js = format_chat(args, js)
    return js