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

introduce = f'''This is a meme with an overlaid caption: "{from_raw_data}".'''
main_instruction = '''classify the given meme as either hateful or non-hateful considering both the image content and its caption.'''
DIRECT_CLASSIFY = {
    'name': "Classify",
    'should_evaluate': True,
    'take_image': True,
    'gen_depend_on': None,
    'versions': {
        'v0': {
        'INS': f''''''
        }
    },
    'output_format': {
        'v0': {"INS": '''If the meme is potentially offensive, harmful or hateful, output "Yes." and then give your explanation. If the meme is benign and follows social norms, output "No." and then give your explanation.''', 'post_process_func': extract_classification_label_yes_or_no}
    },
}

DESCRIBE = {
    'name': "Describe",
    'should_evaluate': False,
    'take_image': True,
    'gen_depend_on': None,
    'versions': {
        'v0': {"INS" : '''What is shown in the image? Describe within three sentences, ignoring any overlaid text or caption.'''},
        'v1': {"INS" : f'''This is an image with overlaid caption(s) that reads "{from_raw_data}". Question: What is shown in the image? Describe within three sentences.'''},
        'v2': {"INS" : f'''The overlaid text on the image reads: "{from_raw_data}". Question: What is shown in the image? Describe within three sentences. DO NOT assume the nature of the image's tone or intent as humorous, comical, playful or lighthearted in your description.'''},
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

# Are the people in the image female or male?
GENDER = {
    'name': "Gender", 'should_evaluate': False, 'take_image': True, 'gen_depend_on': [HUMAN['name']],
    'versions': {
        'v0': {"INS" : f'''{check_dependency}Ignore any overlaid text or caption in the image. What is/are the gender(s) of the human subject(s) in the image?'''}
    },
    'output_format': {
        'v0': {"INS": '''''', 'post_process_func': False},
    }
}

FEMALE = {
    'name': "Female", 'should_evaluate': False, 'take_image': True, 'gen_depend_on': [HUMAN['name']],
    'versions': {
        'v0': {"INS" : f'''{check_dependency}Ignore any overlaid text or caption in the image. Is/Are there any human subject(s) in the image female?'''}
    },
    'output_format': {
        'v0': {"INS": '''Start your response with "Yes," or "No," before giving further explanation.''', 'post_process_func': extract_yes_or_no},
    }
}

# Ignore any overlaid text or caption in the image. Does the image's visual content contain sexual innuendo?
SEX = {
    'name': "Sex", 'should_evaluate': False, 'take_image': True, 'gen_depend_on': [HUMAN['name']],
    'versions': {
        'v0': {"INS" : f'''{check_dependency}Ignore any overlaid text or caption in the image. Does the image's visual content contain sexual innuendo? If yes, explain the related visual cues.'''},
        'v1': {"INS" : f'''{check_dependency}Does the image's visual content contain adult content? Ignore any overlaid text or caption in the image.'''},
    },
    'output_format': {
        'v0': {"INS": '''Start your response with "Yes," or "No," before giving further explanation.''', 'post_process_func': extract_yes_or_no},
    }
}

FEMALE_SEXUAL = {
    'name': "Sexual", 'should_evaluate': False, 'take_image': True, 'gen_depend_on': [FEMALE['name']],
    'versions': {
        'att': {"INS" : f'''{check_dependency}Ignore any overlaid text or caption in the image. Is/Are the female subject(s) in the image dressed revealingly?'''},
        'att1': {"INS" : f'''{check_dependency}Ignore any overlaid text or caption in the image. Is/Are the female subject(s) in the image dressed revealingly in a way that tends to be sexually provocative?'''},
        'sexy': {"INS" : f'''{check_dependency}Ignore any overlaid text or caption in the image. Does the image's visual content highlight the sexiness of the female's figure?'''},
        'sexy1': {"INS" : f'''{check_dependency}Does the image's visual content highlight the sexiness of the female's figure? Ignore any overlaid text or caption in the image.'''},
        'sexy2': {"INS" : f'''{check_dependency}Does the image's visual content highlight the sexiness of the female's figure in a way that is sexually provocative? Ignore any overlaid text or caption in the image.'''},
        'body': {"INS" : f'''{check_dependency}Ignore any overlaid text or caption in the image. Does this image show sexual body parts of the female subject(s), such as the breast, the hip or the genital?'''},
        'body1': {"INS" : f'''{check_dependency}Ignore any overlaid text or caption in the image. Does this image highlight sexual body parts of the female subject(s), such as the breast, the hip or the genital?'''},
        
        'body2': {"INS" : f'''{check_dependency}Ignore any overlaid text or caption in the image. Does this image highlight sexual body parts of the female subject(s), such as the breast, the hip/buttock, or the genital?'''},
        'fat': {"INS" : f'''{check_dependency}Ignore any overlaid text or caption in the image. Does/Do the female subject(s) in the image appear to be overweight?'''},
        'fat1': {"INS" : f'''{check_dependency}Ignore any overlaid text or caption in the image. Does/Do the female subject(s) in the image appear to be of large body size (considered as fat)?'''},
        'exag': {"INS" : f'''{check_dependency}Ignore any overlaid text or caption in the image. Does the image exaggerate any body parts of the female subject(s)?'''}
    },
    'output_format': {
        'v0': {"INS": '''Start your response with "Yes," or "No," before giving any further explanation.''', 'post_process_func': extract_yes_or_no},
    }
}

APPEARANCE = {
    'name': "Appearance", 'should_evaluate': False, 'take_image': True, 'gen_depend_on': [FEMALE['name']],
    'versions': {
        'v0': {"INS" : f'''{check_dependency}Ignore any overlaid text or caption in the image. What are the distinctive physical appearance characteristics of the female subject(s) in the image?'''},
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
        'v0': {"INS": '''If there is no clear clues indicating the identity of the human subject(s) in the image, output "I can't tell."''', 'post_process_func': extract_celeb}
    }
}

# --------------------------- For Unimodal LLMs --------------------#
UNIFY_SYS = '''You are a helpful assistant.''' #'''You are an expert in meme content comprehension and hatefulness detection.'''
INTEGRATE = {
    'name': "Integrate", 'should_evaluate': False, 'take_image': False, 'gen_depend_on': [HUMAN['name'], GENDER['name'], SEX['name'], FEMALE['name'], FEMALE_SEXUAL['name'], APPEARANCE['name'], DESCRIBE['name']],
    'versions': {
        'v0': {
            "INS": f'''Given the following information provided about an image, and disregarding any information about overlaid text or captions, synthesize and rephrase these information into a unified, comprehensive description of the image content. Information: "{from_dependency}"'''
        },
        'v1': {
            "INS": f'''Given the following information provided about an image, and disregarding any information about overlaid text or captions, synthesize and rephrase these information into a unified, comprehensive description of the image content. DO NOT ASSUME the nature of the image's tone and intent as humorous, comical, playful or lighthearted in the description. Information: "{from_dependency}"'''
        },
        'v2': {
            "INS" : f'''Given the following information about an image, ignoring any information about overlaid text or caption, integrate and rephrase these details to create one comprehensive and cohesive description of the image content. Information: "{from_dependency}"'''
        },
    },
    'output_format': {
        'v0': {"INS": '''''', 'post_process_func': post_process_to_remove_gibberish},
    }
}

from_Integrate = "{from_Integrate}"
REASONING_SEP_VERS = {}
for k, v in GLs.items():
    REASONING_SEP_VERS[k] = {
        'gen_depend_on': [INTEGRATE['name']],
        'INS': [
            f'''Given the following image-caption content, which may or may not be an online meme,''',
            '''classify the content as either misogynistic or non-misogynistic based on common values, knowledge, social norms and the provided guidelines.''',
            f'''Guidelines: {v}''',
            f'''Image-caption content you need to classify: {from_Integrate}''',
            f'''The caption overlaid on the image reads "{from_raw_data}".''',
            # '''Now, let's think step by step:'''
            '''Now, let's analyze by applying all the guidelines one by one:'''
        ]
    }
REASONING_SEP_VERS_2 = {}
for k, v in Step_Guidelines.items():
    REASONING_SEP_VERS_2[k] = {
        'gen_depend_on': [INTEGRATE['name']],
        'INS': [
            f'''Given the following image-caption content, which may or may not be an online meme,''',
            f'''determine whether or not the content meets the criteria to be classified as {v['stance']} in the provided guidelines.''',
            f'''Guidelines: {v['gl']}''',
            f'''Image-caption content you need to analyze: {from_Integrate}''',
            f'''The caption overlaid on the image reads "{from_raw_data}".''',
            # '''Now, let's think step by step:'''
            '''Now, let's analyze by applying the guidelines one by one:'''
        ]
    }

REASONING_STAGE1 = {}
for t_abbr, t_dict in STAGE1_GL.items():
    type_name, type_gl = t_dict['type'].lower(), t_dict['guideline']
    REASONING_STAGE1[t_abbr] = {
        'gen_depend_on': [INTEGRATE['name']],
        'INS': [
            f'''Given the following image-caption content, which may or may not be an online meme,''',
            '''classify the content as either misogynistic or non-misogynistic based on common values, knowledge, social norms and the provided guidelines.''',
            # f'''analyze whether or not there is evidence of {type_name} that would classify the content as misogynistic according to the provided guidelines.''',
            f'''Guidelines: {type_gl}''',
            f'''**Image-caption content you need to classify**: {from_Integrate}''',
            f'''The caption overlaid on the image reads "{from_raw_data}".''',
            # '''Now, let's think step by step:'''
            '''Now, let's analyze by applying all the guidelines one by one:'''
        ]
    }

from_Integrate_after_check = '''{from_Integrate_after_check}'''
from_raw_data_after_check = '''{from_raw_data_after_check}'''
check_stage1_pred_cls = '''{check_stage1_pred_cls}'''
REASONING_STAGE2 = {}
# for type_name, type_dict in TYPES_META.items():
#     if 'Q_if_miso' in type_dict:
#         t_abbr = type_dict['abbr']+"*"
#         add_gls = "\n".join([f"{id+1}. {rule}" for id, rule in enumerate(type_dict['Q_if_miso'])])
for t_abbr, t_dict in STAGE2_GL.items():
    type_gl = t_dict['guideline']
    REASONING_STAGE2[t_abbr+"*"] = {
        # 'gen_depend_on': None,
        # 'INS': f'''{check_stage1_pred_cls}Since you just classified the content as misogynistic in view of evidence(s) about {type_name.lower()}, now, analyze whether or not the image-caption content would be re-considered as non-misogynistic according to following additional guidelines. Here are the additional guidelines: {add_gls} Now, let's analyze the content by applying the guidelines one by one:'''
        'gen_depend_on': [INTEGRATE['name']],
        'INS': f'''{check_stage1_pred_cls}Given the following image-caption content, which may or may not be an online meme, classify the content as either misogynistic or non-misogynistic based on common values, knowledge, social norms and the provided guidelines. Guidelines: {type_gl}\n**Image-caption content you need to classify**: {from_Integrate_after_check} The caption overlaid on the image reads "{from_raw_data_after_check}". Now, let's analyze by applying all the guidelines one by one:''',
    }

REASONING_BASE_VERS = {
    'ClassifyWODef': {
        'gen_depend_on': [INTEGRATE['name']],
        'INS': [
            f'''Classify the following meme content as either hateful or non-hateful based on common values, knowledge and social norms.''',
            f'''Meme content: {from_Integrate}''',
            f'''The caption overlaid on the image reads "{from_raw_data}".'''
        ]
    },
    'CoTwContext': {
        'gen_depend_on': [INTEGRATE['name']],
        'INS': [
            f'''Given the following image-caption content, which may or may not be an online meme,''',
            '''classify the content as either misogynistic or non-misogynistic based on common values, knowledge and social norms.''',
            f'''Here are some guidelines for your reference: {KNOWLEDGE}''',#some tips
            f'''Image-caption content you need to classify: {from_Integrate}''',
            f'''The caption overlaid on the image reads "{from_raw_data}".''',
            # '''Now, let's think step by step:'''
            '''Now, let's analyze by applying the guidelines one by one:'''
        ]
    },
    'SelfReflect': {
        'gen_depend_on': None,
        'INS': [
            f'''Review your previous analysis to ensure it aligns with the provided guidelines. Revise any aspects of your reasoning that did not adhere to these guidelines, and finalize your classification. Now, let's check the reasoning against the guidelines one by one:'''
        ]
    },
}
REASONING_VERS = dict(**REASONING_BASE_VERS, **REASONING_SEP_VERS, **REASONING_SEP_VERS_2, **REASONING_STAGE1, **REASONING_STAGE2)
REASONING = {
    'name': "Reasoning", 'should_evaluate': False, 'take_image': False,
    'versions': REASONING_VERS,
    'output_format': {
        'v0': {"INS": '''''', 'post_process_func': False},
    }
}

STEP_DECISION_STAGE1 = {}
for t_abbr, t_dict in STAGE1_GL.items():
    type_name = t_dict['type']
    STEP_DECISION_STAGE1[t_abbr] = {
        'should_evaluate': False,
        'gen_depend_on': None,
        # 'INS': f'''If you just classified the content as misogynistic because evidence of {type_name.lower()} exists, output "Conclusion: Misogynistic ({type_name})." Otherwise, output "Conclusion: NO Evidence."''',
        'INS': f'''If you just found evidence that suggests {type_name.lower()}, output "Conclusion: Misogynistic ({type_name})." If you just classified the content as misogynistic based on other reasons, output "Conclusion: Misogynistic (reason_in_a_phrase)." Otherwise, just output "Conclusion: Non-misogynistic."'''
    }
STEP_DECISION_STAGE2 = {}
for t_abbr, _ in STAGE2_GL.items():
# for type_name, type_dict in TYPES_META.items():
#     if 'Q_if_miso' in type_dict:
    #t_abbr = type_dict['abbr']+"*"
    STEP_DECISION_STAGE2[t_abbr+"*"] = {
        'should_evaluate': False,
        'gen_depend_on': None,
        # 'INS': f'''If you maintain your initial classification, just output "Conclusion: Misogynistic ({type_name})." Otherwise, if you just re-classified the content as non-misogynistic by applying the additional guidelines, output "Conclusion: Non-misogynistic."'''
        'INS': f'''If you just classified the image-caption content as misogynistic, output "Conclusion: Misogynistic." Otherwise, output "Conclusion: Non-misogynistic."''',
    }
STEP_DECISION_ORI = {
    'v0': {
        'should_evaluate': False,
        'gen_depend_on': None,
        'INS': f'''If you just classified the image-caption content as misogynistic, output "Conclusion: Misogynistic." Otherwise, output "Conclusion: Non-misogynistic."''',
    },
    'v1': {
        'should_evaluate': False,
        'gen_depend_on': None,
        'INS': f'''If you just determined that the guideline's criteria are not applicable to this specific image-caption content, output "Conclusion: Criteria Not Applicable." Otherwise, if you just applied the criteria to classify the content as misogynistic, output "Conclusion: Misogynistic." or output "Conclusion: Non-misogynistic." if the criteria suggest that the content is non-misogynistic.''',
    }
}
STEP_DECISION_OUTPUT_ORI = {
    'v0': {"INS": '''''', 'post_process_func': mami_extract_classification_label},
    'v1': {"INS": '''''', 'post_process_func': mami_extract_stage_decision_label},
}
STEP_DECISION_STAGE1_OUTPUT_EXTRATOR = {}
for t_abbr, t_dict in STAGE1_GL.items():
    this_extractor = MAMI_Extractor(t_dict['type'])
    STEP_DECISION_STAGE1_OUTPUT_EXTRATOR[t_abbr] = {
        "INS": '''''', 'post_process_func': this_extractor.mami_extract_stage_decision_label
    }
STEP_DECISION = {
    'name': "StepDecision", 'take_image': False,
    'versions': dict(**STEP_DECISION_ORI, **STEP_DECISION_STAGE1, **STEP_DECISION_STAGE2),
    'output_format': dict(**STEP_DECISION_OUTPUT_ORI, **STEP_DECISION_STAGE1_OUTPUT_EXTRATOR)
}

GPT_DIRECT_CLASSIFY = {
    'name': "Classify", 'should_evaluate': False, 'take_image': True, 'gen_depend_on': None,
    'versions': {
        'v0': {'INS': f'''Classify this meme as either misogynistic or non-misogynistic.'''},
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
        }
    },
    'output_format': {
        'v0': {"INS": '''''', 'post_process_func': mami_extract_classification_label},
    }
}

from_prestep_decision = '''{from_prestep_decision}'''
STEP_WHY = {
    'name': "StepWhy", 'should_evaluate': False, 'take_image': False,
    'versions': {
        'v0': {
            'gen_depend_on': None,
            'INS': f'''{from_prestep_decision}''',
        },
    },
    'output_format': {
        'v0': {"INS": '''''', 'post_process_func': mami_extract_step_reasons},
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

M2T = {
    'lmm': {'prompt': {
                    0: {'template': HUMAN, "version": "v0", "out_format": 'v0'}, 
                    1: {'template': GENDER, "version": "v0", "out_format": 'v0'},
                    2: {'template': SEX, "version": "v1", "out_format": 'v0'},
                    3: {'template': FEMALE, "version": "v0", "out_format": 'v0'},
                    #4: {'template': FEMALE_SEXUAL, "version": "att1", "out_format": 'v0'},
                    4: {'template': FEMALE_SEXUAL, "version": "sexy2", "out_format": 'v0'},
                    5: {'template': FEMALE_SEXUAL, "version": "body2", "out_format": 'v0'},
                    6: {'template': FEMALE_SEXUAL, "version": "fat", "out_format": 'v0'},
                    7: {'template': FEMALE_SEXUAL, "version": "fat1", "out_format": 'v0'},
                    # 8: {'template': FEMALE_SEXUAL, "version": "exag", "out_format": 'v0'},
                    # 9: {'template': GENITAL, "version": "f", "out_format": 'v0'},
                    # 10: {'template': GENITAL, "version": "m", "out_format": 'v0'},
                    8: {'template': APPEARANCE, "version": "v0", "out_format": 'v0'},
                    9: {'template': DESCRIBE, "version": "v2", "out_format": 'v0'},
            },
            'multi-turn': False},
    'llm_1': {'prompt': {
                    0: {'template': INTEGRATE, "version": "v1", "out_format": 'v0'},    
            },
            'multi-turn': False},
}

# ******************************************************************************************* 

d6 = {
    'llm_2': {
        'multi-turn': True,
        'prompt': {
            0: {'template': REASONING, "version": "CoTwContext", "out_format": 'v0'},
            # 1: {'template': REASONING, "version": "SelfReflect", "out_format": 'v0'},
            1: {'template': DECISION, "version": "v0", "out_format": 'v0'}
        }
    }
}

d6 = {}
llm_id = 2
# for k in range(len(REASONING_SEP_VERS)):
#     d6[f"llm_{llm_id}"] = {
#         'multi-turn': True,
#         'prompt': {
#             0: {'template': REASONING, "version": f"g{k}", "out_format": 'v0', 'max_new_tokens': 512, 'new_conversation': True},
#             k+1: {'template': STEP_DECISION, "version": f"v0", "out_format": 'v0'},
#             k+14 : {'template': STEP_WHY, "version": f"v0", "out_format": 'v0'}
#         }
#     }
#     llm_id += 1

# for k in range(len(REASONING_SEP_VERS_2)):
#     d6[f"llm_{llm_id}"] = {
#         'multi-turn': True,
#         'prompt': {
#             0: {'template': REASONING, "version": f"s{k}", "out_format": 'v0', 'max_new_tokens': 512, 'new_conversation': True},
#             k+1: {'template': STEP_DECISION, "version": f"v1", "out_format": 'v1'}
#         }
#     }
#     llm_id += 1

# # Step-by-step
for type_name, type_dict in TYPES_META.items():
    if 'Q_if_miso' in type_dict:
        d6[f"llm_{llm_id}"] = {
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
        d6[f"llm_{llm_id}"] = {
            'multi-turn': True,
            'prompt': {
                0: {'template': REASONING, "version": type_dict['abbr'], "out_format": 'v0'}, #'max_new_tokens': 512
                1: {'template': STEP_DECISION, "version": type_dict['abbr'], "out_format": type_dict['abbr']}
            }
        }
        llm_id += 1
fid = llm_id - 1
d6[f"llm_{fid}"]['prompt'][1]['gather_step_decisions'] = True
final_step_version = d6[f"llm_{fid}"]['prompt'][1]["version"]
d6[f"llm_{fid}"]['prompt'][1]['template']['versions'][final_step_version]['gen_depend_on'] = [STEP_DECISION['name']]
d6[f"llm_{fid}"]['prompt'][1]['template']['versions'][final_step_version]['should_evaluate'] = True

# # Test single aspect
# d6["llm_2"] = {
#     'multi-turn': True,
#     'prompt': {
#         0: {'template': REASONING, "version": 'obj', "out_format": 'v0'}, #'max_new_tokens': 512
#         1: {'template': STEP_DECISION, "version": 'obj', "out_format": 'obj'},
#         2: {'template': REASONING, "version": 'obj'+"*", "out_format": 'v0'},
#         3: {'template': STEP_DECISION, "version": 'obj'+"*", "out_format": 'v1'},
#     }
# }
D6 = dict(**M2T, **d6)
# ******************************************************************************************* # 
MAMI_PROMPT_SCHEMES = {
    'B1': B1,
    'GPT': GPT,
    'M2T': M2T,
    'D6': D6,
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
        # dp_pred_key = 'processed_dependency_prediction'
        # if dp_pred_key not in js:
        #     dp_pred_key = "processed_prediction"
        # dp_pred = js.pop(dp_pred_key)
        # assert isinstance(dp_pred, str)
        # # Reinforce body shaming cues in image if there's any
        # image_info_dict = js.pop("gathered_predictions")
        # for info_type, info in image_info_dict.items():
        #     if info_type.strip("0123456789").endswith("-fat") and (info is not None):
        #         dp_pred = " ".join([dp_pred, info])
        dp_pred, js = get_Integrate_dp_pred(js)
        return tmp.format(from_Integrate = dp_pred), js
    
    if from_prestep_decision in tmp:
        dp_pred_key = "processed_prediction"
        dp_pred = js.pop(dp_pred_key)
        js["step_pred_label"] = dp_pred
        assert isinstance(dp_pred, dict)
        if dp_pred['pred_label'] == 1:
            pred_cls = 'Misogynistic'
            reason_ls = "1. Harmful Stereotypes; 2. Body Shaming; 3. Objectification of Women; 4. Sexualization of Women; 5. Suggesting Violence Towards Women; 6. Anti-Feminist/Anti-Feminism."
        else:
            pred_cls = 'Non-misogynistic'
            reason_ls = "A. NO evidence suggesting Guideline 3; B. NO evidence suggesting Guideline 4; C. Application of Guideline 4."
        tmp = f'''What are the corresponding reasons you just gave to justify your classification of the image-caption content as **{pred_cls}**? Directly choose your answer(s) from the provided list (you may choose multiple options if there are more than one reasons): {reason_ls}'''
        return tmp, js
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
        # js['seq_in'] = T5_PROMPTS[0].format(segment=text, definitions=fal_def_str.lower())

        #js['seq_in'] = T5_PROMPTS[0].format(segment=text, definitions=fal_def_str.lower(), fallacies=fal_name_str.lower())
    else:
        js = format_chat(args, js)
    return js