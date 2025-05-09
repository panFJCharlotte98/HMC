from utils.knowledge.fhm import *
from utils.tool import *
from_raw_data = '{from_raw_data}'
from_dependency = '{from_dependency}'
from_previous_turn = '{from_previous_turn}'
# --------------------------- For Multimodal LMMs --------------------#
DESCRIBE = {
    'name': "Describe",
    'should_evaluate': False,
    'take_image': True,
    'gen_depend_on': None,
    'versions': {
        'v0': {"INS" : '''What is shown in the image? Describe within two sentences, ignoring any overlaid text or caption.'''},
        'v1': {"INS" : '''What is this image about?'''},
        'v2': {"INS" : '''What is shown in the image?'''},
        'v3': {"INS" : '''Describe what is going on in the image. If the image focuses on people, you should explicitly mention some of the people's characteristics such as ethnicity, race, nationality, immigration status, religion, caste, gender identity, sexual orientation, and disability or disease if the image shows any indicative visual cues. Also, you should explicitly mention his or her name if the image portrays a celebrity.'''},
        'v4': {"INS" : '''Describe what is going on in the image, ignoring any overlaid text.'''},
        'v5': {"INS" : '''Describe the image, focusing only on the visual elements and ignoring any overlaid text. Pay attention to the main subject or main event of the image but do not mention or interpret any overlaid text in the image. Point out the objects, people or animals, what they are doing and the kind of feelings or sentiment conveyed. If there are multiple sub-images, describe them sequentially from from top to bottom and left to right.'''},
    },
    'output_format': {
        'v0': {"INS": "", 'post_process_func': False},
        'v1': {"INS": '''Output in JSON format {"output": description_of_the_image}. Only output JSON.''', 'post_process_func': True},
    }
}

introduce = f'''This is a meme with an overlaid caption: "{from_raw_data}".'''
main_instruction = '''classify the given meme as either hateful or non-hateful considering both the image content and its caption.'''
DIRECT_CLASSIFY = {
    'name': "Classify",
    'should_evaluate': True,
    'take_image': True,
    'gen_depend_on': None,
    'versions': {
        'v1': {
        'INS': f'''{introduce} According to the following definitions: 1. "hateful": "{FHM_VANILLA_DEF_HATE_MEME}" 2. "non-hateful": "{FHM_DEF_BENIGN_MEME}", {main_instruction}'''
        },
        'v2': {
            'INS': f'''{introduce} According to the following definitions: 1. "hateful": "{FHM_DEF_HATE_MEME}" 2. "non-hateful": "{FHM_DEF_BENIGN_MEME}", {main_instruction}'''
        },
        'v3': {
            'INS': f'''{introduce} Based on commonsense knowledge, determine whether or not the meme is potentially offensive, harmful or hateful.'''
        },
        'v4': {
            'INS': f'''{introduce} Based on commonsense knowledge, classify the given meme as either harmful or benign.'''
        },
        'v5': {
            'INS': f'''{FHM_DEF_HATE} According to this definition, determine and explain whether the given meme is hateful or non-hateful considering both the image content and the overlaid caption: "{from_raw_data}".'''
        },
    },
    'output_format': {
        'v1': {"INS": '''If the meme is potentially hateful, output in JSON format {"decision": "hateful", "explanation": in_sentences}. Otherwise, if the meme follows social norms, output {"decision": "non-hateful", "explanation": in_sentences}. Only output JSON.''', 'post_process_func': False},
        'v2': {"INS": '''If the meme contains any hateful content, output in JSON format {"decision": "hateful", "explanation": in_sentences}. Otherwise, if the meme follows social norms, output {"decision": "non-hateful", "explanation": in_sentences}. Only output JSON.''', 'post_process_func': False},
        'v3': {"INS": '''If the meme is potentially offensive, harmful or hateful, output "Yes." and then give your explanation. If the meme is benign and follows social norms, output "No." and then give your explanation.''', 'post_process_func': extract_classification_label_yes_or_no},
        'v4': {"INS": '''If the meme is potentially harmful, offensive, or hateful, output "Harmful" and give your explanation. Otherwise, if the meme is benign and follows social norms, output "Benign" and give your explanation.''', 'post_process_func': extract_yes_or_no},
        'v5': {"INS": '''Output your answer in JSON format {"decision": "hateful_or_non-hateful", "explanation": in_sentences}. Only output JSON.''', 'post_process_func': False},
        'v6': {"INS": '''If the meme is hateful, output "hateful". Otherwise, output "non-hateful". Provide the answer as either "hateful" or "non-hateful" only.''', 'post_process_func': False}
    },
}

check_dependency = '''{check_dependency}'''
HUMAN = {
    'name': "Human", 'should_evaluate': False, 'take_image': True, 'gen_depend_on': None,
    'versions': {
        'v0': {"INS" : '''Is there any human subject in the given image? Ignore any overlaid text or caption.'''},
        'v1': {"INS" : '''Are there any people in this image?'''},
    },
    
    'output_format': {
        'v0': {"INS": '''''', 'post_process_func': extract_yes_or_no},
        'v1': {"INS": '''Start your response with "Yes," or "No," before giving any further explanation.''', 'post_process_func': extract_yes_or_no},
        'v2': {"INS": '''If there are people in the image, output "Yes.". Otherwise, output "No.".''', 'post_process_func': extract_yes_or_no},
    }
}

RACE = {
    'name': "Race", 'should_evaluate': False, 'take_image': True, 'gen_depend_on': [HUMAN['name']],
    'versions': {
        'v0': {"INS" : f'''{check_dependency}What is the perceived race of the human subject(s) in the image? Ignore any overlaid text or caption.'''},
        'v1': {"INS" : f'''{check_dependency}What is the race of the people in the image?'''},
    },
    
    'output_format': {
        'v0': {"INS": '''''', 'post_process_func': False}
    }
}

# Are the people in the image female or male?
GENDER = {
    'name': "Gender", 'should_evaluate': False, 'take_image': True, 'gen_depend_on': [HUMAN['name']],
    'versions': {
        'v0': {"INS" : f'''{check_dependency}What is the gender of the human subject(s) in the image? Ignore any overlaid text or caption.'''},
        'v1': {"INS" : f'''{check_dependency}What is the gender of the people in the image?'''},
    },
    
    'output_format': {
        'v0': {"INS": '''''', 'post_process_func': False},
    }
}

APPEARANCE = {
    'name': "Appearance", 'should_evaluate': False, 'take_image': True, 'gen_depend_on': [HUMAN['name']],
    'versions': {
        'v0': {"INS" : f'''{check_dependency}What are the distinctive physical appearance characteristics of the human subject(s) in the image? Ignore any overlaid text or caption.'''},
    },
    
    'output_format': {
        'v0': {"INS": '''''', 'post_process_func': False},
    }
}

CELEB = {
    'name': "Celeb", 'should_evaluate': False, 'take_image': True, 'gen_depend_on': [HUMAN['name']],
    'versions': {
        'v0': {"INS" : f'''{check_dependency}Who is/are the human subject(s) in the image?'''},
    },
    
    'output_format': {
        'v0': {"INS": '''If there is no clear clues indicating the identity of the human subject(s) in the image, output "I can't tell."''', 'post_process_func': extract_celeb},
        'v1': {"INS": '''If there are, output "Yes." and then point out who he/she is. Otherwise, output "No."''', 'post_process_func': extract_yes_or_no},
    }
}

DISABLE = {
    'name': "Disability", 'should_evaluate': False, 'take_image': True, 'gen_depend_on': [HUMAN['name']],
    'versions': {
        'v0': {"INS" : f'''{check_dependency}Does/Do the human subject(s) in the image have any disability?'''},
        'v1': {"INS" : f'''Do the people in the image seem to have any disability?'''},
        'v2': {"INS" : f'''Are there any disabled or handicapped people in the image?'''},
    },
    'output_format': {
        'v0': {"INS": '''''', 'post_process_func': extract_disable},
        'v1': {"INS": '''If the people do have disability, output "Yes." and then describe the kind of disability. Otherwise, output "No." ''', 'post_process_func': extract_yes_or_no},
        'v2': {"INS": '''If there are, output "Yes." and then describe the kind of disability. Otherwise, output "No."''', 'post_process_func': extract_yes_or_no},
    }
}

SEX = {
    'name': "Sex", 'should_evaluate': False, 'take_image': True, 'gen_depend_on': [HUMAN['name']],
    'v1': {"INS" : f'''{introduce} Are there any potential sex or adult content in the image and its caption?'''},
    'output_format': {
        'v1': {"INS": '''If there is, output "Yes." and then explain. Otherwise, output "No."''', 'post_process_func': extract_yes_or_no},
    }
}

# --------------------------- For Unimodal LLMs --------------------#

UNIFY_SYS = '''You are a helpful assistant.''' #'''You are an expert in meme content comprehension and hatefulness detection.'''
from_Integrate = "{from_Integrate}"
INTEGRATE = {
    'name': "Integrate", 'should_evaluate': False, 'take_image': False, 'gen_depend_on': [HUMAN['name'], RACE['name'], GENDER['name'], APPEARANCE['name'], CELEB['name'], DISABLE['name'], DESCRIBE['name']],
    'versions': {
        'v0': {
            "INS": f'''Given the following information provided about an image, and disregarding any information about overlaid text or captions, synthesize and rephrase these information into a unified, detailed description of the image content. Information: "{from_dependency}"'''
        },
        'v1': {
            "INS" : f'''Given the following information about an image, ignoring any information about overlaid text or caption, integrate and rephrase these details to create one comprehensive and cohesive description of the image content. Information: "{from_dependency}"'''
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
                f'''Based on the following definitions: 1. "hateful": {FHM_DEF_HATE_MEME}. 2. "non-hateful": {FHM_DEF_BENIGN_MEME}, classify the following meme content as either hateful or non-hateful.''',
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
        'CoTori': {
            'gen_depend_on': [INTEGRATE['name']],
            'INS': [
                f'''Given the following image-caption content, which may or may not be an online meme,''',
                '''classify the content as either hateful or non-hateful based on common values, knowledge and social norms.''',
                f'''Image-caption content: {from_dependency}''',
                f'''The caption overlaid on the image reads "{from_raw_data}".''',
                '''Now, let's think step by step:'''
            ]
        },
        'CoT': {
            'gen_depend_on': [INTEGRATE['name']],
            'INS': [
                f'''Given the following image-caption content, which may or may not be an online meme,''',
                '''classify the content as either hateful or non-hateful based on common values, knowledge and social norms.''',
                f'''Here are some guidelines for your reference: {KNOWLEDGE}''',#some tips
                f'''**Image-caption content you need to classify**: {from_dependency}''',
                f'''The caption overlaid on the image reads "{from_raw_data}".''',
                '''Now, let's think step by step:'''
            ]
        },
        'TargetG': {
            'gen_depend_on': [INTEGRATE['name']],
            'INS': [
                f'''Given the following image-caption content which may or may not be an online meme,''',
                '''analyze: if the content is potentially hateful, what is the vulnerable protected group being targeted?''',
                '''Here are some guidelines for your reference: A. Adhere to the general definition for hateful contents or hateful speech based on common values, knowledge and social norms.''',
                '''B. If the content does not seem to involve any specific vulnerable groups, just output "No specific protected group being targeted."''',
                '''C. If the content could be potentially offensive, harmful or hateful against specific groups, choose your answer from the provided list:''',
                '''1. Women (Female); 2. LGBTQ Community; 3. People with Disabilities; 4. Muslims and Islamic Culture; 5. Individuals of Middle Eastern Descent; 6. Jewish Individuals; 7. Individuals of African Descent, including African Americans; 8. Other Colored People; 9. People of Asian Descent; 10. Other protected groups not listed.''',
                f'''Here is the image-caption content you need to analyze: {from_dependency}''',
                f'''The caption overlaid on the image reads "{from_raw_data}".''',
                '''Now, let's think step by step:'''
            ]
        },
        'TargetG1': {
            'gen_depend_on': [INTEGRATE['name']],
            'INS': [
                f'''Given the following image-caption content which may or may not be an online meme,''',
                '''analyze: what vulnerable protected group(s) might be involved in the content?''',
                '''Here are some guidelines for your reference:''',
                '''A. If the content does not seem to involve any specific protected groups, just output "No specific protected group involved."''',
                '''B. If the content does involve specific protected groups, choose your answer(s) from the provided list:''',
                '''1. Women (Female); 2. LGBTQ Community; 3. People with Disabilities; 4. Muslims and Islamic Culture; 5. Individuals of Middle Eastern Descent; 6. Jewish Individuals; 7. Individuals of African Descent, including African Americans; 8. Other Colored People; 9. People of Asian Descent; 10. Other protected groups not listed.''',
                f'''Here is the image-caption content you need to analyze: {from_dependency}''',
                f'''The caption overlaid on the image reads "{from_raw_data}".''',
                '''Now, let's think step by step:'''
            ]
        },
        'TargetG2': {
            'gen_depend_on': [INTEGRATE['name']],
            'INS': [
                f'''Given the following image-caption content which may or may not be an online meme,''',
                '''analyze: what vulnerable protected group(s) might be involved in the content?''',
                '''Here are some guidelines for your reference:''',
                '''A. If the content does not seem to involve any specific protected group, just output "No specific protected group involved."''',
                '''B. If the content does involve specific protected groups, choose your answer(s) from the provided list (you may choose multiple options if there are more than one protected groups involved):''',
                '''1. Women (Female); 2. LGBTQ Community; 3. People with Disabilities; 4. Muslims and Islamic Culture; 5. Individuals of Middle Eastern Descent; 6. Jewish Individuals; 7. Individuals of African Descent, including African Americans; 8. People of Asian Descent; 9. Other Colored People; 10. Native Americans; 11. Other protected groups not listed.''',
                f'''Here is the image-caption content you need to analyze: {from_dependency}''',
                f'''The caption overlaid on the image reads "{from_raw_data}".''',
                '''Now, let's think step by step:'''
            ]
        },
        'CoTwTGContext': {
            'gen_depend_on': [INTEGRATE['name'], INTEGRATE_TG_CONTEXT['name']],
            'INS': [
                f'''Given the following image-caption content, which may or may not be an online meme,''',
                '''classify the content as either hateful or non-hateful based on common values, knowledge and social norms.''',
                f'''Here are some guidelines for your reference: {KNOWLEDGE}\n''',
                f'''{from_IntegrateTGContext}\nImage-caption content you need to classify:''',
                #some tips
                f'''{from_Integrate}''',
                f'''The caption overlaid on the image reads "{from_raw_data}".''',
                '''Now, let's think step by step:'''
            ]
        },
    },
    'output_format': {
        'v0': {"INS": '''''', 'post_process_func': False},
    }
}

VLREASONING = {
    'name': "Reasoning",
    'should_evaluate': False,
    'take_image': True,
    'gen_depend_on': None,
    'versions': {
        'CoT': {
            "INS": [
                f'''{introduce} Based on common values, knowledge and social norms, classify the given meme as either hateful or non-hateful.''',
                '''Now, let's think step by step:'''
            ]
        },
    },
    'output_format': {
        'v0': {"INS": '''''', 'post_process_func': False},
    },
}

DECISION = {
    'name': "Decision", 'should_evaluate': True, 'take_image': False,
    'versions': {
        'v0': {
            'gen_depend_on': None,
            'INS': [
                f'''If you just classified the image-caption content as 1. "perceived to be hateful by the general public" or 2. "perceived to be hateful by specific individuals or groups",''',
                '''output "Conclusion: Hateful." Otherwise, if your previous classification is 3. "perceived to be non-hateful by the general public", output "Conclusion: Non-hateful."'''
            ]
        },
        'v1': {
            'gen_depend_on': None,
            'INS': f'''If you just classified the meme content as hateful, output "Conclusion: Hateful." Otherwise, output "Conclusion: Non-hateful."''',
        }, 
        'v2': {
            'gen_depend_on': None,
            'INS': f'''If you just classified the meme content as hateful, output "Conclusion: Hateful." Otherwise, output "Conclusion: Non-hateful."''',
        }, 
        'v3': {
            'gen_depend_on': None,
            'INS': f'''If you just classified the image-caption content as hateful, output "Conclusion: Hateful." Otherwise, output "Conclusion: Non-hateful."''',
        },  
        'v4': {
            'gen_depend_on': None,
            'INS': f'''If you just classified the meme as hateful, output "Conclusion: Hateful." Otherwise, output "Conclusion: Non-hateful."''',
        }
    },
    'output_format': {
        'v0': {"INS": '''''', 'post_process_func': extract_classification_label},
    }
}


M2T = {
    'lmm_1': {'prompt': {
                    0: {'template': HUMAN, "version": "v0", "out_format": 'v1'}, 
                    1: {'template': RACE, "version": "v0", "out_format": 'v0'},
                    2: {'template': GENDER, "version": "v0", "out_format": 'v0'},
                    3: {'template': APPEARANCE, "version": "v0", "out_format": 'v0'},
                    4: {'template': CELEB, "version": "v0", "out_format": 'v0'},
                    5: {'template': DESCRIBE, "version": "v0", "out_format": 'v0'},
                    # 6: {'template': SEX, "version": "v1", "out_format": 'v1'},
            },
            'multi-turn': False},
    'lmm_2': {'prompt': {
                    0: {'template': DISABLE, "version": "v0", "out_format": 'v0'}, 
            },
            'multi-turn': False},
    'llm_1': {'prompt': {
                    0: {'template': INTEGRATE, "version": "v0", "out_format": 'v0'},    
            },
            'multi-turn': False},
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

d6 = {
    'llm_2': {
        'multi-turn': True,
        'prompt': {
            0: {'template': REASONING, "version": "CoT", "out_format": 'v0'},
            1: {'template': DECISION, "version": "v3", "out_format": 'v0'}
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
            2: {'template': GENERATE_TG_CONTEXT, "version": "v0", "out_format": 'v0'},
            3: {'template': INTEGRATE_TG_CONTEXT, "version": "v0", "out_format": 'v0', 'new_conversation': True},
            4: {'template': REASONING, "version": "CoTwTGContext", "out_format": 'v0', 'new_conversation': True},
            5: {'template': DECISION, "version": "v3", "out_format": 'v0'},
        }
    },
    # 'llm_3': {
    #     'multi-turn': True,
    #     'prompt': {
    #         2: {'template': GENERATE_TG_CONTEXT, "version": "v0", "out_format": 'v0'},
    #     }
    # },
    # 'llm_4': {
    #     'multi-turn': True,
    #     'prompt': {
    #         3: {'template': INTEGRATE_TG_CONTEXT, "version": "v0", "out_format": 'v0', 'new_conversation': True},
    #         4: {'template': REASONING, "version": "CoTwTGContext", "out_format": 'v0', 'new_conversation': True},
    #         5: {'template': DECISION, "version": "v3", "out_format": 'v0'},
    #     }
    # }
}

D4 = {
    'lmm': {
        'prompt': {
            0: {'template': DIRECT_CLASSIFY, "version": "v3", "out_format": 'v3'},
        },
        'multi-turn': False
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

D0 = dict(**M2T, **d0)
D1 = dict(**M2T, **d1)
D2 = dict(**M2T, **d2)
D3 = dict(**M2T, **d3)
D6 = dict(**M2T, **d6)
D6m = dict(**M2T, **d6m)

# ******************************************************************************************* # 

FHM_PROMPT_SCHEMES = {
    # 'S1': S1,
    # 'S2': S2,
    # 'S3': S3,
    # 'S4': S4,
    # 'S5': S5,
    # 'S6': S6,
    'M2T': M2T,
    'D0': D0,
    'D1': D1,
    'D2': D2,
    'D3': D3,
    'D4': D4,
    'D5': D5,
    'D6': D6,
    'D6m': D6m
}


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
    if check_tg in tmp:
        dp_pred = js["TargetGroup"]
        assert isinstance(dp_pred, list)
        if dp_pred:
            questions = []
            for target_group in dp_pred:
                questions.append(Q4TGCONTEXT[target_group])
            if len(questions) > 1:
                tmp = " ".join([f"{i+1}. {q}" for i, q in enumerate(questions)])
            else:
                tmp = questions[0]
            return tmp, js
        else:
            return "", None
    if integrate_tg_context in tmp:
        tg_ls = js["TargetGroup"]
        assert tg_ls
        if len(tg_ls) > 1:
            tg_str = " and ".join(tg_ls)
        else:
            tg_str = tg_ls[0]
        dp_pred = js.pop("processed_prediction")
        tg_examples = " ".join([f"Commonly found hateful contents targeting {tg} include: {GL_TARGETS[tg]}" for tg in tg_ls if tg != "Others"] + [dp_pred])
        tmp = f'''Given the following examples of commonly found hateful contents in online memes against {tg_str}, integrate the information into one comprehensive and coherent list. Examples: {tg_examples}'''
        return tmp, js
    if from_Integrate in tmp:
        dp_pred = js.pop(INTEGRATE['name'])
        return tmp.format(from_Integrate = dp_pred), js
    if from_IntegrateTGContext in tmp:
        dp_pred = js.pop(INTEGRATE_TG_CONTEXT['name'])
        dp_pred = extract_target_group_context(dp_pred)
        tg = js["TargetGroup"]
        if (len(tg) == 1) and (tg[0] == "Others"):
            prefix = "10. Commonly found hateful contents targeting various vulnerable protected groups include:"
        else:
            tg_str = " and ".join(js["TargetGroup"])
            prefix = f"10. Commonly found hateful contents targeting the vulnerable protected groups like {tg_str} include:"
        if dp_pred:
            dp_pred = " ".join([prefix, dp_pred])
        return tmp.format(from_IntegrateTGContext = dp_pred), js
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
            img_path = js['img_mask'] if args.use_mask_img else js['img']
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
        js['seq_in'] = T5_PROMPTS[0].format(segment=text, definitions=fal_def_str.lower())
        #js['seq_in'] = T5_PROMPTS[0].format(segment=text, definitions=fal_def_str.lower(), fallacies=fal_name_str.lower())
    else:
        js = format_chat(args, js)
    return js



# DECISION = {
#     'name': "Decision", 'should_evaluate': True, 'take_image': False,
#     'versions': {
#         'v0': {
#             'gen_depend_on': None,
#             'INS': '''Reviewing all your thinking, classify the image-caption pair as 1. perceived to be hateful by the general public, 2. perceived to be hateful by specific individuals or groups, 3. perceived to be non-hateful by the general public.'''    
#         },
#         'DirectClassify': {
#             'gen_depend_on': [INTEGRATE['name']],
#             'INS': [
#                 f'''Given the following description of an image-caption pair, which may or may not be an online meme,''',
#                 '''classify the content as 1. perceived to be hateful by the general public, 2. perceived to be hateful by specific individuals or groups, 3. perceived to be non-hateful by the general public.''',
#                 f'''Image-caption pair: {from_dependency}''',
#                 f'''The caption overlaid on the image reads "{from_raw_data}".'''
#             ]
#         },
#         'ClassifyWDef': {
#             'gen_depend_on': [INTEGRATE['name']],
#             'INS': [
#                 f'''Given the following definitions: 1. "hateful": {FHM_DEF_HATE_MEME}. 2. "non-hateful": {FHM_DEF_BENIGN_MEME}, classify the following meme content as either hateful or non-hateful.''',
#                 f'''Meme content: {from_dependency}''',
#                 f'''The caption overlaid on the image reads "{from_raw_data}".'''
#             ]
#         },
#         'ClassifyWODef': {
#             'gen_depend_on': [INTEGRATE['name']],
#             'INS': [
#                 f'''Classify the following meme content as either hateful or non-hateful based on common values and knowledge.''',
#                 f'''Meme content: {from_dependency}''',
#                 f'''The caption overlaid on the image reads "{from_raw_data}".'''
#             ]
#         },
#         'v1': {
#             'gen_depend_on': [INTEGRATE['name']],
#             'INS': [
#                 f'''Reflecting on your previous association and reviewing the image-caption content,''',
#                 '''classify the content as 1. perceived to be hateful by the general public, 2. perceived to be hateful by specific individuals or groups, 3. perceived to be non-hateful by the general public.''',
#                 f'''Image-caption content: {from_dependency}''',
#                 f'''The caption overlaid on the image reads "{from_raw_data}".'''
#             ]
#         },
#         'v2': {
#             'gen_depend_on': None,
#             'INS': [
#                 f'''Reflecting on your previous association and reasoning,''',
#                 '''classify the image-caption content as 1. High potential of being perceived as hateful, 2. Moderate potential of being perceived as hateful, 2. Low potential of being perceived as hateful.''',
#                 # f'''Image-caption content: {from_dependency}''',
#                 # f'''The caption overlaid on the image reads "{from_raw_data}".'''
#             ]
#         },
#         'v3': {
#             'gen_depend_on': None,
#             'INS': [
#                 f'''Output "Conclusion: Hateful." if you classify the image-caption content as hateful. Otherwise, output "Conclusion: Non-hateful."''',
#             ]
#         },
#     },
#     'output_format': {
#         'v0': {"INS": '''''', 'post_process_func': extract_classification_label},
#         'v1': {"INS": '''''', 'post_process_func': False},
#     }
# }


# main_instruction = '''According to the definitions, classify the given meme content as either hateful or non-hateful considering both the meme's image description and its overlaid caption.'''
# CLASSIFY = {
#     'name': "Classify",
#     'should_evaluate': True,
#     'take_image': False,
#     'gen_depend_on': True,
#     'v1': {
#         'SYS': '''You are a helpful expert in detecting hateful meme contents.''',
#         'INS': [
#             f'''Given the following definitions: 1. "hateful": {FHM_DEF_HATE_MEME} 2. "non-hateful": {FHM_DEF_BENIGN_MEME} {main_instruction}''',
#             f'''Image description: "{from_dependency}"''',
#             f'''Caption: "{from_raw_data}"''',
#         ]      
#     },
#     'v2': {
#         'SYS': '''You are a helpful expert in detecting hateful speeches.''',
#         'INS': [
#             f'''{FHM_DEF_HATE}. According to this definition, determine and explain whether the following context is hateful or non-hateful.''',
#             f'''Text: "{from_dependency}"'''
#         ]
#     },
#     'v3': {
#         'SYS': '''You are a helpful expert in detecting hateful speeches.''',
#         'INS': [
#             f'''Given the following definitions: 1. "hateful": {FHM_DEF_HATE}. 2. "non-hateful": {FHM_DEF_BENIGN}. According to the definitions, classify the following speech as either hateful or non-hateful.''',
#             f'''Speech: "{from_raw_data}"'''
#         ]
#     },
#     'v4': {
#         'INS': f'''Given the following definitions: 1. "hateful": {FHM_DEF_HATE_MEME}. 2. "non-hateful": {FHM_DEF_BENIGN_MEME}. According to the definitions and your previous analysis, classify the meme content as either hateful or non-hateful.''',

#     },
#     'v5': {
#         'SYS': '''You are a helpful expert in detecting hateful meme contents.''',
#         'INS': [f'''Given the following meme content with a description of its image and the overlaid caption, based on commonsense knowledge, classify the meme content as either harmful or benign.''',
#                 f'''Meme image description: "{from_dependency}"''',
#                 f'''Meme caption: "{from_raw_data}"''']
#     },
#     'output_format': {
#         'v1': {"INS": '''If the meme content is hateful, output in JSON format {"decision": "hateful", "explanation": in_sentences}. Otherwise, output {"decision": "non-hateful", "explanation": in_sentences}. Only output JSON.''', 'post_process_func': False},
#         'v2': {"INS": '''If the speech is potentially hateful, output in JSON format {"decision": "hateful", "explanation": in_sentences}. Otherwise, output {"decision": "non-hateful", "explanation": in_sentences}. Only output JSON.''', 'post_process_func': False},
#         'v3': {"INS": '''If the meme content is potentially harmful, offensive, or hateful, output in JSON format {"decision": "harmful", "explanation": detailed_explanations_in_sentences}. Otherwise, output {"decision": "benign", "explanation": detailed_explanations_in_sentences}. Only output JSON.''', 'post_process_func': False},
#         'v4': {"INS": '''If the meme content is potentially harmful, offensive, or hateful, output "Harmful" and then provide your detailed explanation. Otherwise, if the meme is benign and follows social norms, output "Benign" and provide your detailed explanation.''', 'post_process_func': extract_yes_or_no},
#     },
# }

# # --------------------------- Prompt Schemes --------------------#
# S1 = {
#     'lmm': {
#         'prompt': {0: {'template': DIRECT_CLASSIFY, "version": 'v2', "out_format": 'v1'}},
#         'multi-turn': False
#     }
# }

# S2 = {
#     'lmm': {'prompt': {0: {'template': DESCRIBE, "version": "v1", "out_format": 'v1'}},
#             'multi-turn': False
#         },
#     'llm': {'prompt': {0: {'template': CLASSIFY, "version": "v1", "out_format": 'v1'}},
#             'multi-turn': False
#         }
# }

# S3 = {
#     'lmm': {'prompt': {
#                     0: {'template': DESCRIBE, "version": "v2", "out_format": 'v1'},
#                     1: {'template': HUMAN, "version": "v1", "out_format": 'v2'}, 
#                     2: {'template': RACE, "version": "v1", "out_format": 'v1'},
#                     3: {'template': GENDER, "version": "v1", "out_format": 'v1'},
#                     4: {'template': DISABLE, "version": "v2", "out_format": 'v2'},
#                     5: {'template': CELEB, "version": "v1", "out_format": 'v1'},
#                     6: {'template': SEX, "version": "v1", "out_format": 'v1'},
#             },
#             'multi-turn': False},
#     'llm': {'prompt': {0: {'template': CLASSIFY, "version": "v5", "out_format": 'v3', 'gather_previous_outputs': True}},
#             'multi-turn': False
#     }
# }

# S4 = {
#     'lmm': {'prompt': {
#                     0: {'template': DESCRIBE, "version": "v2", "out_format": 'v1'},
#                     1: {'template': HUMAN, "version": "v1", "out_format": 'v2'}, 
#                     2: {'template': RACE, "version": "v1", "out_format": 'v1'},
#                     3: {'template': GENDER, "version": "v1", "out_format": 'v1'},
#                     4: {'template': DISABLE, "version": "v2", "out_format": 'v2'},
#                     5: {'template': CELEB, "version": "v1", "out_format": 'v1'},
#                     6: {'template': SEX, "version": "v1", "out_format": 'v1'},
#             },
#             'multi-turn': False},
#     'llm': {'prompt': {
#                     0: {'template': INTERPRET, "version": "v1", "out_format": 'v1', 'gather_previous_outputs': True},
#                     1: {'template': CLASSIFY, "version": "v4", "out_format": 'v1'}},
#             'multi-turn': True
#     }
# }


# S5 = {
#     'llm': {'prompt': {
#                     0: {'template': CLASSIFY, "version": "v3", "out_format": 'v2'}
#                     },
#             'multi-turn': False
#     }
# }

# S6 = {
#     'llm': {'prompt': {
#                     0: {'template': INTERPRET, "version": "v2", "out_format": 'v1'},
#                     1: {'template': CLASSIFY, "version": "v4", "out_format": 'v2'}
#                     },
#             'multi-turn': True
#     }
# }

# S7 = {
#     'lmm': {'prompt': {0: {'template': DESCRIBE, "version": "v1", "out_format": 'v1'}},
#             'multi-turn': False
#         },
#     'llm': {'prompt': {0: {'template': FUSE, "version": "v1", "out_format": 'v1'}, 
#                        1: {'template': CLASSIFY, "version": "v1", "out_format": 'v1'}},
#             'multi-turn': False
#         }
# }

# FUSE = {
#     'name': "Fuse",
#     'should_evaluate': False,
#     'take_image': False,
#     'gen_depend_on': True,
#     'v1' : {
#         'SYS': '''You are a skillful expert in creative writing.''',
#         'INS': ['''Fuse the given image caption into the image description to form a short story that is coherent and funny.''',
#                 f'''Image caption: "{from_raw_data}"''',
#                 f'''Image description: "{from_dependency}"''',
#             ]
#     },
#     'output_format': {
#         'v1': {"INS": '''Output in JSON format {"output": fused_text}. Only output JSON.''', 'post_process_func': True},
#         'v2': {"INS": "Fused text:", 'post_process_func': False},
#     } 
# }

# PREPARE = {
#     'name': "Prepare", 'should_evaluate': False, 'take_image': False, 'gen_depend_on': None,
#     'versions': {
#         'v0': {
#             'INS': [
#                 '''You will be given a task as follows: "Go through the description of an image-caption pair, which may or may not be an online meme, classify the image-caption pair as hateful, mildly hateful or non-hateful based on common values and knowledge."''',
#                 '''Analyze in detail what this task is all about and the things you should know for the task.''',
#                 '''Discuss the essential distinctions between "hateful", "mildly hateful" and "non-hateful" content.''',
#                 '''Identify and describe in detail the criteria you should use to make an accurate decision between "hateful", "mildly hateful" and "non-hateful" content.'''
#             ]      
#         },
#         'v1': {
#             'INS': [
#                 '''Based on common values and knowledge, provide a comprehensive definition to "hateful" contents, and''',
#                 '''list as many as possible the vulnerable groups that could be targerted by hateful contents.''',
#             ]      
#         },
#     },
#     'output_format': {
#         'v0': {"INS": '''''', 'post_process_func': False},
#     }
# }

# CONTEXT = {
#     'name': "Context", 'should_evaluate': False, 'take_image': False,
#     'versions': {
#         'v0': {
#             'gen_depend_on': [INTEGRATE['name']],
#             'INS': [
#                 '''Here is the image-caption pair you will investigate in:''',
#                 f'''"{from_dependency}''',
#                 f'''The caption overlaid on the image reads "{from_raw_data}".''',
#                 '''With the previous considerations in mind, provide the relevant cultural and social knowledge context necessary for understanding this image-caption content and evaluating the risk of it being interpreted as hateful.''',
#                 '''DO NOT make the classification at the moment.''',
#             ]      
#         },
#         'v1': {
#             'gen_depend_on': [INTEGRATE['name']],
#             'INS': [
#                 '''Given the following image-caption content, which may or may not contain hateful content,''',
#                 '''provide the relevant cultural and social knowledge context necessary for evaluating the risk of it being interpreted as hateful.'''
#                 f'''Image-caption content: The caption overlaid on the image reads "{from_raw_data}".''',
#                 f'''{from_dependency}'''
#             ]      
#         },
#         'v2': {
#             'gen_depend_on': [INTEGRATE['name']],
#             'INS': [
#                 '''Examining the following image and its caption, which may or may not be labelled as "hateful" in common scenarios,''',
#                 '''if the content does mean to be hateful, identify the likely vulnerable group that is being targeted. You may refer to your previous response about vulnerable groups.'''
#                 f'''Image-caption content: The caption overlaid on the image reads "{from_raw_data}".''',
#                 f'''{from_dependency}'''
#             ]      
#         },
#         'v3': {
#             'gen_depend_on': None,
#             'INS': [
#                 '''If "Others" is your previous response, simply output "No additional context". Otherwise, provide the historical, social and culture context the identified vulnerable group is frequently associated with and targeted by hateful content.''',
#             ]      
#         },
#     },
#     'output_format': {
#         'v0': {"INS": '''''', 'post_process_func': False},
#     }
# }


# QUESTIONS = {
#     'name': "Questions", 'should_evaluate': False, 'take_image': False, 'gen_depend_on': None,
#     'versions': {
#         'v0': {
#             'INS': [
#                 '''Based on the information you provided about the difference between''',
#                 '''"hateful", "mildly hateful" and "non-hateful" contents as well as the relevant cultural and social context,''',
#                 '''ask three critical questions specific to this image-caption content to help determine whether the content is likely to be percieved as hateful or mildly hateful.''',
#             ]      
#         },
#     },
#     'output_format': {
#         'v0': {"INS": '''''', 'post_process_func': False},
#     }
# }

# ANSWERS = {
#     'name': "Answers", 'should_evaluate': False, 'take_image': False, 'gen_depend_on': None,
#     'versions': {
#         'v0': {
#             'INS': '''Now, please answer these questions you just proposed.'''    
#         },
#     },
#     'output_format': {
#         'v0': {"INS": '''''', 'post_process_func': False},
#     }
# }


# ROUTE = {
#     'name': "Route", 'should_evaluate': False, 'take_image': False, 
#     'versions': {
#         'v0': {
#             'gen_depend_on': [INTEGRATE['name']],
#             'INS':  [
#                 '''Given the following topic list, '''
#                 '''Given the following image-caption content:''',
#                 f'''{from_dependency}''',
#                 f'''The caption overlaid on the image reads "{from_raw_data}".''',
#                 '''What topics might this image-caption pair be associated with? Select from the following topic list:''',
#                 '''1. Gender Roles, 2. Race, 3. Religion, 4. LGBTQ Community, 4. Disability, 5. Violence, 5. Hate Crimes, 6. Criminals, 7. Immigration, 8. History, 9. Celebrity, ''',
#                 '''If none of the listed topics is relevant, simply output "Others".'''
#             ]     
#         },
#         'group': {
#             'gen_depend_on': None,
#             'INS':  [
#                 '''Distill your previous conclusion by selecting the group from the list you provided about vulnerable groups targeted by hateful contents. If your conclusion is not found in the list, simply output "Others". ONLY output the group without providing reasoning.''',
#             ]     
#         },
#     },
#     'output_format': {
#         'v0': {"INS": '''''', 'post_process_func': False},
#     }
# }

# INTERPRET = {
#     'name': "Interpret",
#     'should_evaluate': False,
#     'take_image': False,
#     'gen_depend_on': [INTEGRATE['name']],

#     'versions': {
#         'v0' : {
#         },
#         'v1' : {
#             'SYS': '''You are an expert in reading comprehension.''',
#             'INS': [f'''Given the following meme content with a description of its image and the overlaid caption, analyze: what does it mean by the meme's caption "{from_raw_data}"?''',
#                     f'''Meme image description: "{from_dependency}"''',
#                     f'''Meme caption: "{from_raw_data}"''',
#                     ]
#         },
#         'v2' : {
#             'SYS': '''You are an expert in reading comprehension.''',
#             'INS': f'''Interpret the meaning of the following speech: "{from_raw_data}"'''
#         },
#     },
#     'output_format': {
#         'v0': {"INS": '''''', 'post_process_func': False},
#         'v1': {"INS": '''''', 'post_process_func': False},
#         'v2': {"INS": '''Output your analysis in JSON format {"output": your_analysis}. Only output JSON.''', 'post_process_func': True},
#     } 
# }


# CoT = {
#     'name': "CoT",
#     'should_evaluate': False,
#     'take_image': False,
#     'versions': {
#         'DirectClassify': {
#             'gen_depend_on': [INTEGRATE['name']],
#             'INS': [
#                 f'''Given the following image-caption content, which may or may not be an online meme,''',
#                 '''classify the content as either hateful or non-hateful based on common values and social norms.''',
#                 f'''Image-caption content: {from_dependency}''',
#                 f'''The caption overlaid on the image reads "{from_raw_data}".''',
#                 '''Now, let's think step by step:'''
#             ]
#         },
#     },
#     'output_format': {
#         'v0': {"INS": '''''', 'post_process_func': False},
#     } 
# }



# # s_pcqad = {
# #     'llm_2': {
# #         'multi-turn': True,
# #         'prompt': {
# #             0: {'template': PREPARE, "version": "v0", "out_format": 'v0'},
# #             1: {'template': CONTEXT, "version": "v0", "out_format": 'v0'},
# #             2: {'template': QUESTIONS, "version": "v0", "out_format": 'v0'},
# #             3: {'template': ANSWERS, "version": "v0", "out_format": 'v0'},
# #             4: {'template': DECISION, "version": "v0", "out_format": 'v0'},
# #         }
# #     }
# # }

# s_decision = {
#     'llm_2': {
#         'multi-turn': False,
#         'prompt': {
#             0: {'template': DECISION, "version": "DirectClassify", "out_format": 'v0'},
#         }
#     }
# }

# s_Classify_w_def = {
#     'llm_2': {
#         'multi-turn': False,
#         'prompt': {
#             0: {'template': DECISION, "version": "ClassifyWDef", "out_format": 'v0'},
#         }
#     }
# }

# s_Classify_wo_def = {
#     'llm_2': {
#         'multi-turn': False,
#         'prompt': {
#             0: {'template': DECISION, "version": "ClassifyWODef", "out_format": 'v0'},
#         }
#     }
# }

# s_route = {
#     'llm_2': {
#         'multi-turn': False,
#         'prompt': {
#             0: {'template': ROUTE, "version": "v0", "out_format": 'v0'},
#         }
#     }
# }

# s_context = {
#     'llm_2': {
#         'multi-turn': False,
#         'prompt': {
#             0: {'template': CONTEXT, "version": "v1", "out_format": 'v0'},
#         }
#     }
# }

# s_test = {
#     'llm_2': {
#         'multi-turn': True,
#         'prompt': {
#             0: {'template': CoT, "version": "DirectClassify", "out_format": 'v0'},
#             1: {'template': DECISION, "version": "v3", "out_format": 'v0'},
#             # 0: {'template': PREPARE, "version": "v1", "out_format": 'v0'},
#             # 1: {'template': CONTEXT, "version": "v2", "out_format": 'v0'},
#             # 2: {'template': ROUTE, "version": "group", "out_format": 'v0'},
#             # 3: {'template': CONTEXT, "version": "v3", "out_format": 'v0'},
#             # 4: {'template': DECISION, "version": "v1", "out_format": 'v0'},
#             # 5: {'template': DECISION, "version": "v2", "out_format": 'v0'},
#         }
#     }
# }

# PCQAD = dict(**M2T, **s_pcqad)


# TOPIC = dict(**M2T, **s_route)
# C = dict(**M2T, **s_context)
# T = dict(**M2T, **s_test)