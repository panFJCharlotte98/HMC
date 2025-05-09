from utils.knowledge.fhm import *
from utils.tool import *
from_raw_data = '{from_raw_data}'
from_dependency = '{from_dependency}'
from_previous_turn = '{from_previous_turn}'
# --------------------------- For Multimodal LMMs --------------------#
introduce = f'''This is a meme with an overlaid caption: "{from_raw_data}".'''

VLREASONING = {
    'name': "VLReasoning", 'should_evaluate': False, 'take_image': True, 'gen_depend_on': None,
    'versions': {
        'CoT': {
            'INS': [
                f'''This is an image with an overlaid caption that reads: "{from_raw_data}".''',
                '''Classify the image as either hateful or non-hateful based on widely accepted social norms, cultural context, and established understanding of harmful stereotypes, biases, and discriminatory narratives.''',
                '''**Now, let's analyze step by step**:'''
            ]
        }
    },
    'output_format': {
        'v0': {"INS": '''''', 'post_process_func': post_process_to_remove_gibberish},
    }
}

DESCRIBE = {
    'name': "Describe",
    'should_evaluate': False,
    'take_image': True,
    'gen_depend_on': None,
    'versions': {
        'v0': {"INS" : f'''What is shown in the image? Describe within three sentences, ignoring any overlaid text or caption.'''},
        'v1': {"INS" : f'''What is shown in the image? Describe within two sentences, ignoring any overlaid text or caption.'''},### best with
    },
    'output_format': {
        'v0': {"INS": "", 'post_process_func': post_process_visual_describe},
        'v1': {"INS": "", 'post_process_func': post_process_description},
    }
}

Ignore = '''Ignore any overlaid text or caption.'''
check_dependency = "{check_dependency}"
check_human_dependency = '''{check_human_dependency}'''
HUMAN = {
    'name': "Human", 'should_evaluate': False, 'take_image': True, 'gen_depend_on': None,
    'versions': {
        'v0': {"INS" : f'''Is there any human subject in the given image? {Ignore}'''},
    },
    'output_format': {
        'v0': {"INS": '''Start your response with "Yes," or "No," before giving any further explanation.''', 'post_process_func': extract_yes_or_no},
    }
}

NUM = {
    'name': "Num", 'should_evaluate': False, 'take_image': True, 'gen_depend_on': [HUMAN['name']],
    'versions': {
        'v0': {"INS" : f'''{check_human_dependency}Does the image include more than one human subject? {Ignore}'''},
    },
    'output_format': {
        'v0': {"INS": '''Start your response with "Yes," or "No," before giving the explanation.''', 'post_process_func': extract_yes_or_no},
    }
}

CELEB = {
    'name': "Celeb", 'should_evaluate': False, 'take_image': True, 'gen_depend_on': [NUM['name']],
    'versions': {
        'v0': {"INS" : '''{Celeb-0_check_human_num_dependency}'''},
        'v1': {"INS" : f'''Is any celebrity or historical figure portrayed in the image? If yes, who are they? If no, just output "No.".'''},
        # 'hit': {"INS" : f'''Is Adolf Hitler portrayed in the image?'''},
        'hit': {"INS" : f'''Does the image portray Adolf Hitler?'''},
        'anne': {"INS" : f'''Does the image portray Anne Frank, the Jewish girl who hid from the Nazis during World War II?'''},
    },
    'output_format': {
        'v0': {"INS": '''If there is no clear clues indicating the identity of the human subject(s) in the image, output "I can't tell."''', 'post_process_func': extract_celeb},
        'v1': {"INS": '''Start your response with "Yes," or "No," before giving the explanation.''', 'post_process_func': extract_yes_or_no},
        'anne': {"INS": '''If yes, output "Yes, Anne Frank is portrayed in the image." Otherwise, if you are not sure about the identity of human subject, just output "No, I can't tell."''', 'post_process_func': extract_celeb},
        'hit': {"INS": '''If yes, output "Yes, Adolf Hitler is portrayed in the image." Otherwise, if you are not sure about the identity of human subject, just output "No, I can't tell."''', 'post_process_func': extract_celeb},
    }
}

RACE = {
    'name': "Race", 'should_evaluate': False, 'take_image': True, 'gen_depend_on': [NUM['name']],
    'versions': {
        'v0': {"INS" : '''{Race_check_human_num_dependency}'''},
    },
    'output_format': {
        'v0': {"INS": '''''', 'post_process_func': False}
    }
}

GENDER = {
    'name': "Gender", 'should_evaluate': False, 'take_image': True, 'gen_depend_on': [NUM['name']],
    'versions': {
        'v0': {"INS" : '''{Gender_check_human_num_dependency}'''},
    },
    'output_format': {
        'v0': {"INS": '''''', 'post_process_func': False},
    }
}

APPEARANCE = {
    'name': "Appearance", 'should_evaluate': False, 'take_image': True, 'gen_depend_on': [NUM['name']],
    'versions': {
        'v0': {"INS" : '''{Appearance_check_human_num_dependency}'''},
        'v1': {"INS" : f'''What are the distinctive physical appearance characteristics of the human subject(s) in the image? {Ignore}'''},
    },
    'output_format': {
        'v0': {"INS": '''''', 'post_process_func': False},
    }
}

DISABLE = {
    'name': "Disability", 'should_evaluate': False, 'take_image': True, 'gen_depend_on': [NUM['name']],
    'versions': {
        'v0': {"INS" : '''{Disability_check_human_num_dependency}'''},
        'v1': {"INS" : '''{Disability_check_human_num_dependency}'''}
    },
    'output_format': {
        'v0': {"INS": '''''', 'post_process_func': extract_disable},
        'v1': {"INS": '''Start your response with "Yes," or "No," before giving the explanation.''', 'post_process_func': extract_yes_or_no},
    }#
}

DISABLE_HOW = {
    'name': "Dishow", 'should_evaluate': False, 'take_image': False, 'gen_depend_on': [DISABLE['name']],
    'versions': {
        'v0': {"INS" : f'''{check_dependency}So, what kind of disability?'''},
        'v1': {"INS" : f'''{check_dependency}So, what kind of disability does/do the human subject(s) in the image have?'''},
    },
    'output_format': {
        'v0': {"INS": '''''', 'post_process_func': False},
    }
}

VISUAL_PROMPTS = {
    RACE['name']: {
        's': f'''What is the perceived race of the human subject in the image? {Ignore}''',
        'p': f'''What are the perceived races of the human subjects in the image? {Ignore}'''
    },
    GENDER['name']: {
        's': f'''What is the gender of the human subject in the image? {Ignore}''',
        'p': f'''What are the genders of the human subjects in the image? {Ignore}''',
    },
    APPEARANCE['name']: {
        's': f'''What are the distinctive physical appearance characteristics of the human subject in the image? {Ignore}''',
        'p': f'''What are the distinctive physical appearance characteristics of the human subjects in the image? {Ignore}''',
    },
    DISABLE['name']: {
        's': f'''Does the human subject in the image have any disability?''',#appear to 
        'p': f'''Does any of the human subjects in the image have any disability?''',# appear to
    },
    f"{CELEB['name']}-0": {
        's': f'''Who is the human subject in the image?''',
        'p': f'''Who are the human subjects in the image?''',
    }
}

# --------------------------- For Unimodal LLMs --------------------#
UNIFY_SYS = '''You are a helpful assistant.'''
from_Integrate = "{from_Integrate}"
from_data_text = "{from_data_text}"
INTEGRATE = {
    'name': "Integrate", 'should_evaluate': False, 'take_image': False, 
    'versions': {
        'v0': {
            'gen_depend_on': [HUMAN['name'], NUM['name'], RACE['name'], GENDER['name'], APPEARANCE['name'], CELEB['name'], DISABLE['name'], DESCRIBE['name']],
            "INS" : f'''Given the following information provided about an image, and disregarding any information about overlaid text or captions, synthesize and rephrase these information into a coherent and unified description of the image's content. **Information**: "{from_dependency}"'''
        },
        'v1': {# No index id in gathering information
            'gen_depend_on': [HUMAN['name'], RACE['name'], GENDER['name'],DISABLE['name'], APPEARANCE['name'], CELEB['name'], DESCRIBE['name']],
            "INS" : f'''Given the following information provided about an image, and disregarding any information about overlaid text or captions, synthesize and rephrase these information into a coherent and unified description of the image's content. **Information**: {from_dependency}'''
        },
    },
    'output_format': {
        'v0': {"INS": '''''', 'post_process_func': post_process_to_remove_gibberish},
    }
}

EXTRACT = {
    'name': "Extract", 'should_evaluate': False,'take_image': False, 'gen_depend_on': None,
    'versions': {
        'TargetGroup': {
            "INS": f'''If you just concluded that the content does not involve any specific protected groups, output "Conclusion: No specific protected group involved." Otherwise, output "Conclusion: your_choice_from_the_provided_option_list". (**Option list**:{TG_LIST})''',
        },
    },
    'output_format': {
        'v0': {"INS": '''''', 'post_process_func': fhm_extract_target_group},
    },
}

check_tg = "{check_tg}"
integrate_tg_context = "{integrate_tg_context}"
integrate_tg_context_v1 = "{integrate_tg_context_v1}"
from_IntegrateTGContext = "{from_IntegrateTGContext}"
GENERATE_TG_CONTEXT = {
    'name': "GenTGContext", 'should_evaluate': False, 'take_image': False,
    'versions': {
        'v0': {'gen_depend_on': [EXTRACT["name"]], "INS": f'''{check_tg}'''}
    },
    'output_format': {
        'v0': {"INS": '''''', 'post_process_func': post_process_to_remove_gibberish},
    },
}
INTEGRATE_TG_CONTEXT = {
    'name': "IntegrateTGContext", 'should_evaluate': False,'take_image': False,
    'versions': {
        'v0': {
            'gen_depend_on': [GENERATE_TG_CONTEXT['name']], 
            "INS": f'''{integrate_tg_context}'''
        },
        'v1': {
            'gen_depend_on': [GENERATE_TG_CONTEXT['name']], 
            "INS": f'''{integrate_tg_context_v1}'''
        },
    },
    'output_format': {
        'v0': {"INS": '''''', 'post_process_func': post_process_to_remove_gibberish},
    },
}

make_guidelines = "{make_guidelines}"
make_guidelines_w_IntegrateTGContext = "{make_guidelines_w_IntegrateTGContext}"
make_guidelines_w_GenTGContext = "{make_guidelines_w_GenTGContext}"
CLASSIFY_INS = '''Given the following image-caption content, which may or may not be an online meme, classify the content as either hateful or non-hateful based on common values, knowledge and social norms.'''
CLASSIFY_INS_V1 = '''Given the following image-caption content, which may or may not be an online meme, classify the content as either hateful or non-hateful based on widely accepted values, established knowledge, social norms and the provided guidelines.'''
REASONING = {
    'name': "Reasoning", 'should_evaluate': False, 'take_image': False,
    'versions': {
        'TG': {
            'gen_depend_on': [INTEGRATE['name']],
            'INS': [
                f'''Given the following image-caption content which may or may not be an online meme,''',
                '''analyze: what vulnerable protected group(s) might be involved in the content?''',
                '''Here are some guidelines for your reference:''',
                '''A. If the content does not appear to involve any specific protected group, just output "No specific protected group involved."''',
                '''B. If the image content does involve specific protected group(s), choose your answer(s) from the specified list (you may choose multiple options if there are more than one protected groups involved):''',
                f'''{TG_LIST}''',
                f'''Here is the image-caption content you need to analyze: {from_dependency}''',
                f'''The caption overlaid on the image reads "{from_raw_data}".''',
                '''Now, let's think step by step:'''
            ]
        },
        'CoT+': {
            'gen_depend_on': [INTEGRATE['name'], INTEGRATE_TG_CONTEXT['name']],
            'INS': [
                #CLASSIFY_INS,
                CLASSIFY_INS_V1,
                f'''**Guidelines**: {make_guidelines_w_IntegrateTGContext}''',
                f'''**Image-caption content you need to classify**: {from_Integrate}''',
                f'''The caption overlaid on the image reads "{from_raw_data}".''',
                '''Now, let's think step by step:'''
            ]
        },
        # 'CoT+': {
        #     'gen_depend_on': [INTEGRATE['name'], INTEGRATE_TG_CONTEXT['name']],
        #     'INS': [
        #         #CLASSIFY_INS,
        #         CLASSIFY_INS_V1,
        #         f'''Here are some guidelines for your reference: {make_guidelines_w_IntegrateTGContext}''',
        #         f'''**Image-caption content you need to classify**: {from_Integrate}''',
        #         f'''The caption overlaid on the image reads "{from_raw_data}".''',
        #         '''Now, let's think step by step:'''
        #     ]
        # },
        'CoT++': {
            'gen_depend_on': [INTEGRATE['name'], GENERATE_TG_CONTEXT['name']],
            'INS': [
                CLASSIFY_INS,
                f'''Here are some guidelines for your reference: {make_guidelines_w_GenTGContext}''',
                f'''**Image-caption content you need to classify**: {from_dependency}''',
                f'''The caption overlaid on the image reads "{from_raw_data}".''',
                '''Now, let's analyze step by step:'''
            ]
        },
        'CoT*': {
            'gen_depend_on': [INTEGRATE['name'], INTEGRATE_TG_CONTEXT['name']],
            'INS': [
                CLASSIFY_INS,
                f'''Here are some **guidelines** for your reference: {make_guidelines}''',
                f'''**Image-caption content you need to classify**: {from_Integrate}''',
                f'''The caption overlaid on the image reads "{from_raw_data}".''',
                '''Now, let's think step by step:'''
            ]
        },
        'CoT': {
            'gen_depend_on': [INTEGRATE['name']],
            'INS': [
                f'''Given the following image-caption content, which may or may not be an online meme, classify the content as either hateful or non-hateful based on widely accepted values, established knowledge and social norms.''',
                f'''**Image-caption content you need to classify**: {from_dependency}''',
                f'''The caption overlaid on the image reads "{from_raw_data}".''',
                '''**Now, let's think step by step**:'''
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
        'v1': {'INS': f'''Is this meme disrespectful, offensive, harmful or hateful?'''},
        'v0': {'INS': f'''Classify this image as either hateful or non-hateful based on widely accepted social norms, cultural context, and established understanding of harmful stereotypes, biases, and discriminatory narratives.'''},
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
            'INS': f'''If you just classified the image-caption content as hateful, output "Conclusion: Hateful." Otherwise, output "Conclusion: Non-hateful."''',
        },
        'v1': {
            'gen_depend_on': None,
            'INS': f'''If you just classified the image-caption content as hateful (either explicitly or implicitly), output "Conclusion: Hateful." Otherwise, output "Conclusion: Non-hateful."''',
        },
        'vl': {
            'gen_depend_on': None,
            'INS': f'''If you just classified the image as hateful, output "Conclusion: Hateful." Otherwise, output "Conclusion: Non-hateful."''',
        },
        'gpt': {
            'gen_depend_on': [GPT_DIRECT_CLASSIFY['name']],
            # 'INS': f'''If you just classified the image content as hateful, output "Conclusion: Hateful." Otherwise, output "Conclusion: Non-hateful."''',
            'INS': f'''If you just concluded that the meme is potentially disrespectful, offensive, harmful or hateful, output "Conclusion: Yes." Otherwise, output "Conclusion: No."''',
        },
    },
    'output_format': {
        'v0': {"INS": '''''', 'post_process_func': extract_classification_label},
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
        'multi-turn': False},
    'llm': {
        'multi-turn': True,
        'prompt': {
            1: {'template': DECISION, "version": "gpt", "out_format": 'v0'},
        }
    }
}

# # What modifications I made:
# 1. Add Celeb-anne to M2T
# 2. Add Celeb output formats
M2T = {
    'lmm_1': {
        'prompt': {
            0: {'template': HUMAN, "version": "v0", "out_format": 'v0'}, 
            1: {'template': NUM, "version": "v0", "out_format": 'v0'},
            2: {'template': RACE, "version": "v0", "out_format": 'v0'},
            3: {'template': GENDER, "version": "v0", "out_format": 'v0'},
            #4: {'template': APPEARANCE, "version": "v0", "out_format": 'v0'},
            4: {'template': APPEARANCE, "version": "v1", "out_format": 'v0'},
            5: {'template': CELEB, "version": "v0", "out_format": 'v0'},
            6: {'template': CELEB, "version": "v1", "out_format": 'v1'},
            7: {'template': CELEB, "version": "hit", "out_format": 'hit'},
            8: {'template': CELEB, "version": "anne", "out_format": 'anne'},####
            # 9: {'template': DESCRIBE, "version": "v0", "out_format": 'v0'},
            9: {'template': DESCRIBE, "version": "v1", "out_format": 'v1'},### best with
        },
        'multi-turn': False},
    'lmm_2': {
        'prompt': {
            0: {'template': DISABLE, "version": "v0", "out_format": 'v0'}, 
            # 1: {'template': DISABLE_HOW, "version": "v0", "out_format": 'v0'}, 
        },
        'multi-turn': False},
    'llm_1': {
        'prompt': {    
            0: {'template': INTEGRATE, "version": "v1", "out_format": 'v0'}, 
        },
        'multi-turn': False
    },
}

# ******************************************************************************************* # 

b2 = {
    'llm_2': {
        'multi-turn': True,
        'prompt': {
            0: {'template': REASONING, "version": "CoT", "out_format": 'v0'},
            1: {'template': DECISION, "version": "v0", "out_format": 'v0'}
        }
    }
}

p2 = {
    'llm_2': {
        'multi-turn': True,
        'prompt': {
            0: {'template': REASONING, "version": "CoT*", "out_format": 'v0'},
            1: {'template': DECISION, "version": "v0", "out_format": 'v0'}
        }
    }
}

p1 = {
    'llm_2': {
        'multi-turn': True,
        'prompt': {
            0: {'template': REASONING, "version": "TG", "out_format": 'v0'},
            1: {'template': EXTRACT, "version": "TargetGroup", "out_format": 'v0'},
            2: {'template': GENERATE_TG_CONTEXT, "version": "v0", "out_format": 'v0'},
            3: {'template': INTEGRATE_TG_CONTEXT, "version": "v0", "out_format": 'v0', 'new_conversation': True},
            # 3: {'template': INTEGRATE_TG_CONTEXT, "version": "v1", "out_format": 'v0', 'new_conversation': True},
            4: {'template': REASONING, "version": "CoT+", "out_format": 'v0', 'new_conversation': True},
            5: {'template': DECISION, "version": "v1", "out_format": 'v0'},
        }
    },
}

# p1 = {
#     'llm_2': {
#         'multi-turn': True,
#         'prompt': {
#             0: {'template': REASONING, "version": "TG", "out_format": 'v0'},
#             1: {'template': EXTRACT, "version": "TargetGroup", "out_format": 'v0'},
#             2: {'template': GENERATE_TG_CONTEXT, "version": "v0", "out_format": 'v0'},
#             3: {'template': REASONING, "version": "CoT++", "out_format": 'v0', 'new_conversation': True, 'batch_size': 14},
#             4: {'template': DECISION, "version": "v1", "out_format": 'v0'},
#         }
#     },
# }

PP = dict(**M2T, **p1)
P2 = dict(**M2T, **p2)
B2 = dict(**M2T, **b2)
# ******************************************************************************************* # 

FHM_PROMPT_SCHEMES = {
    'M2T': M2T,
    'B1': B1,
    'B2': B2,
    'GPT': GPT,
    'PP': PP,
    'P2': P2,
}

def get_tg_str(tg_ls):
    tg_label_ls = [FHM_TG_KNOWLEDGE[tg]["label"] for tg in tg_ls]
    if (len(tg_ls) == 1):
        # if (tg_ls[0] == "others"):
        #     tg_str = "various vulnerable protected groups"
        # else:
        #     tg_str = tg_label_ls[0]
        tg_str = tg_label_ls[0]
    elif len(tg_ls) > 1:
        tg_label_ls = [FHM_TG_KNOWLEDGE[tg]["label"] for tg in tg_ls if tg != "others"]
        if "others" in tg_ls:
            tg_label_ls = tg_label_ls + [FHM_TG_KNOWLEDGE["others"]["label"]]
        tg_str = ", ".join(tg_label_ls[:-1]) + f" and {tg_label_ls[-1]}"
        tg_str = " ".join(tg_str.strip().split())
    return tg_str

def incorporate_gen_context(tg_ls, dp_pred, include_gen_context=True, include_tg_label=False):
    if len(dp_pred) == 1:
        examples = []
        # for tg_id, tg in enumerate(tg_ls):
        #     if tg != "others":
        #         examples.append(FHM_TG_KNOWLEDGE[tg]["examples"])
        # if examples:
        #     if include_gen_context:
        #         examples = examples + dp_pred
        # else:
        #     examples = dp_pred
        
        if include_gen_context:
            examples = dp_pred
        for tg_id, tg in enumerate(tg_ls):
            if tg != "others":
                examples.append(FHM_TG_KNOWLEDGE[tg]["examples"])
    else:
        # examples = []
        # assert len(tg_ls) > 1
        # if "others" in tg_ls:
        #     tg_ls.remove("others")
        # for tg_id, tg in enumerate(tg_ls):
        #     if tg != "others":
        #         combine = [FHM_TG_KNOWLEDGE[tg]["examples"]]
        #         if include_gen_context:
        #             try:
        #                 combine = combine + [dp_pred[tg_id]]
        #             except:
        #                 combine = combine
        #         if include_tg_label:
        #             tg_label = FHM_TG_KNOWLEDGE[tg]["label"]
        #             combine = [f"Against {tg_label}:"] + combine
        #         examples.extend(combine)        
        # if include_gen_context:
        #     for p in dp_pred:
        #         if p not in examples:
        #             examples.append(p)
        examples = []
        assert len(tg_ls) > 1
        if "others" in tg_ls:
            tg_ls.remove("others")
        tg_labels = [FHM_TG_KNOWLEDGE[tg]["label"] for tg in tg_ls]
        my_exps = [FHM_TG_KNOWLEDGE[tg]["examples"] for tg in tg_ls]
        for tg_label, my_exp, gen_exp in zip(tg_labels, my_exps, dp_pred[:len(tg_ls)]):
            combine = []
            if include_gen_context:
                combine.append(gen_exp)
            combine.append(my_exp)
            if include_tg_label:
                examples.extend([f"Against {tg_label}:"] + combine)    
        if include_gen_context:
            for p in dp_pred:
                if p not in examples:
                    examples.append(p)
    return examples

def assign_guidelines(js, add_tg_context=False, summarize=False):
    assert "TargetGroup" in js
    Rules = [R1, R2, R3, R4, R5, R6, R7, R8]
    Rules = [R_combine, R_neutral, R2, R3, R5, R6, R7, R8]#best with
    Rules = [R_neutral, R2, R3, R5, R6, R7, R8]
    Rules = [R_neutral, R2, R3_new, R5, R6, R7, R8]
    #Rules = [R_combine, R_neutral, R2, R3]#best with
    # Rules = [R1, R2, R3, R5, R6, R7, R8]#best with
    #Rules = [R1, R2, R3_new, R4_new, R5, R6, R7, R8]
    #Rules = [R_combine, R_neutral, R2, R3, R_explicit, R5, R6, R7, R8]
    if add_tg_context:
        tg_ls = js["TargetGroup"]
        if tg_ls:
            tg_str = get_tg_str(tg_ls)
            if summarize:
                dp_pred = js.pop(INTEGRATE_TG_CONTEXT['name'])
                #dp_pred = extract_target_group_context(dp_pred)#best with
                prefix = ""
                if dp_pred:
                    assert tg_ls
                    prefix = "If the image-caption content conveys any of the following implications, it should be classified as hateful:"
                    dp_pred = " ".join([prefix, dp_pred])#best without
                    dp_pred = " ".join(dp_pred.split()).strip()
                    Rules.append(R4)
                    Rules.append(dp_pred)
            else:
                dp_pred = js.pop("gen_tg_context") # is a list
                if dp_pred:
                    assert tg_ls
                    # examples = incorporate_gen_context(tg_ls, dp_pred, include_tg_label=False)##best with
                    #examples = incorporate_gen_context(tg_ls, dp_pred, include_tg_label=True)
                    examples = incorporate_gen_context(tg_ls, dp_pred, include_tg_label=True)
                    Rule_forms = " ".join(" ".join(examples).split())
                    prefix = "Commonly found hateful content:"
                    #prefix = "Commonly found harmful stereotypes and forms of offensive or hateful content:"
                    Rule_forms = " ".join([prefix, Rule_forms])#best without
                    Rules.append(R4)
                    Rules.append(Rule_forms)
        # else:
        #     Rules = [R_combine, R_neutral, R2, R_explicit, R3_new, R4_new, R5, R6, R7, R8]
    
    GL = f" ".join([f"{rid+1}. {rule}" for rid, rule in enumerate(Rules)])
    return GL

def fill_placeholder(tmp, js):
    if from_raw_data in tmp:
        return tmp.format(from_raw_data = js['text'].strip('" ')), js
    if "_dependency}" in tmp:
        dp_pred_key = 'processed_dependency_prediction'
        if dp_pred_key not in js:
            dp_pred_key = "processed_prediction"
        dp_pred = js.pop(dp_pred_key)
        if from_dependency in tmp:
            assert isinstance(dp_pred, str)
            return tmp.format(from_dependency = dp_pred), js
        if check_dependency in tmp:
            if isinstance(dp_pred, dict):
                if dp_pred['flag'] == 1:
                    return tmp.replace(check_dependency, ""), js
                else:
                    return "", None
        if check_human_dependency in tmp:
            assert isinstance(dp_pred, dict)
            if dp_pred['flag'] == 1:
                return tmp.replace(check_human_dependency, ""), js
            else:
                return "", None
        if "check_human_num_dependency}" in tmp:
            assert isinstance(dp_pred, dict)
            visual_p = VISUAL_PROMPTS[tmp.strip("{}").split("_")[0]]
            if dp_pred['flag'] == 1: # more than one humans
                return visual_p['p'], js
            else:
                return visual_p['s'], js
    if make_guidelines in tmp:
        return tmp.format(make_guidelines = assign_guidelines(js)), js
    
    if make_guidelines_w_IntegrateTGContext in tmp:
        return tmp.format(make_guidelines_w_IntegrateTGContext = assign_guidelines(js, add_tg_context=True, summarize=True)), js
    
    if make_guidelines_w_GenTGContext in tmp:
        return tmp.format(make_guidelines_w_GenTGContext = assign_guidelines(js, add_tg_context=True, summarize=False)), js
    
    if check_tg in tmp:
        # Generate Target Context
        dp_pred = js["TargetGroup"]
        assert isinstance(dp_pred, list)
        if dp_pred:
            prompts = []
            for tg_abbr in dp_pred:
                prompts.append(FHM_TG_KNOWLEDGE[tg_abbr]["gen_more"])
                #prompts.append(FHM_TG_KNOWLEDGE[tg_abbr]["gen_more_new"])
            if len(prompts) > 1:
                tmp = " ".join([f"{i+1}. {q}" for i, q in enumerate(prompts)])
                #tmp = " ".join([f"### {q}" for i, q in enumerate(prompts)])
                #tmp = " ".join([f"### 1. {q}" for i, q in enumerate(prompts)])
            else:
                tmp = prompts[0]
            return tmp, js
        else:
            return "", None
    
    if '''{integrate_tg_context''' in tmp:
        tg_ls = js["TargetGroup"]
        assert tg_ls
        if integrate_tg_context in tmp:
            # tg_label_ls = [FHM_TG_KNOWLEDGE[tg]['label'] for tg in tg_ls]
            # if len(tg_ls) > 1:
            #     tg_str = ", ".join(tg_label_ls[:-1]) + f" and {tg_label_ls[-1]}"
            # else:
            #     tg_str = tg_label_ls[0]
            # tg_str = " ".join(tg_str.strip().split())
            tg_str = get_tg_str(tg_ls)
            dp_pred = js.pop("processed_prediction")
            #dp_pred = post_process_gen_target_group_context(dp_pred)
            exist_examples = []
            for tg in tg_ls:
                if tg != "others":
                    card = FHM_TG_KNOWLEDGE[tg]
                    this_label = card["label"]
                    this_example = card["examples"]
                    exist_examples.append(f"### Commonly found hateful content targeting {this_label}: {this_example}")### best with  
            #dp_pred = "### " + dp_pred
            tg_examples = f" ".join(exist_examples + [dp_pred])
            # tmp = f'''Given the following examples of commonly found hateful contents in online memes against {tg_str}, integrate the information into one comprehensive and coherent list. Examples: {tg_examples}'''
            tmp = f'''Summarize the following examples of commonly found hateful contents in online memes against {tg_str}. **Examples to summarize**: {tg_examples} **Summarization**:'''
            tmp = f'''Summarize the following examples of commonly found harmful stereotypes and hateful content in online memes targeting {tg_str}. **Examples to summarize**: {tg_examples} **Summarization**:'''
        elif integrate_tg_context_v1 in tmp:
            tg_str = get_tg_str(tg_ls)
            dp_pred = js.pop("processed_prediction") # a list
            examples = incorporate_gen_context(tg_ls, dp_pred, include_tg_label=True)
            tg_examples = " ".join(" ".join(examples).split())
            # tmp = f'''Summarize the following examples of commonly found hateful contents in online memes against {tg_str}. **Examples to summarize**: {tg_examples} **Summarization**:'''
            tmp = f'''Summarize the following examples of commonly found harmful stereotypes and offensive or hateful content in online memes targeting {tg_str}. **Examples to summarize**: {tg_examples} **Summarization**:'''
            # tmp = f'''Summarize the following examples of commonly found harmful stereotypes, disrespectul, offensive or hateful contents against {tg_str}. **Examples to summarize**: {tg_examples} **Summarization**:'''
        return tmp, js
    
    if from_Integrate in tmp:
        dp_pred = js.pop(INTEGRATE['name'])
        return tmp.format(from_Integrate = dp_pred), js
    # if from_IntegrateTGContext in tmp:
    #     dp_pred = js.pop(INTEGRATE_TG_CONTEXT['name'])
    #     dp_pred = extract_target_group_context(dp_pred)
    #     tg_ls = js["TargetGroup"]
    #     tg_label_ls = [FHM_TG_KNOWLEDGE[tg]["label"] for tg in tg_ls]
    #     prefix = ""
    #     if (len(tg_ls) == 1) and (tg_ls[0] == "others"):
    #         prefix = "9. Commonly found hateful contents targeting various vulnerable protected groups include:"
    #     elif len(tg_ls) > 1:
    #         tg_str = ", ".join(tg_label_ls[:-1]) + f" and {tg_label_ls[-1]}"
    #         tg_str = " ".join(tg_str.strip().split())
    #         prefix = f"9. Commonly found hateful contents targeting protected groups e.g., {tg_str} include:"
    #     if dp_pred:
    #         dp_pred = " ".join([prefix, dp_pred])
    #     dp_pred = " ".join(dp_pred.split())
    #     return tmp.format(from_IntegrateTGContext = dp_pred), js
    if from_data_text in tmp:
        if js['text']:
            prompt = f'''The overlaid caption on the image reads: "{js['text']}"'''
        else:
            prompt = ""
        return tmp.format(from_data_text = prompt), js
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
        
        js['chat_history'] = dialog
        js['task'] = args.task
        js['img_history'] = img_history
    return js

def prompt_fhm(args, model_tag, js):
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