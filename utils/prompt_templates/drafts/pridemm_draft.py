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
            "INS": f'''{Introduce} Classify the meme as either harmful or harmless to: (1) the LGBTQ+ community and its supporters, or (2) the specific individual or organization involved, based on widely accepted values, established knowledge, cultural understanding, and social norms. Now, let's analyze step by step:'''
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

check_dependency = '''{check_dependency}'''
HUMAN = {
    'name': "Human", 'should_evaluate': False, 'take_image': True, 'gen_depend_on': None,
    'versions': {
        'v0': {"INS" : '''Is there any human subject in the image? Ignore any overlaid text or caption.'''},
    },
    'output_format': {
        'v0': {"INS": '''Start your response with "Yes," or "No," before giving any further explanation.''', 'post_process_func': extract_yes_or_no}
    }
}

RACE = {
    'name': "Race", 'should_evaluate': False, 'take_image': True, 'gen_depend_on': [HUMAN['name']],
    'versions': {
        'v0': {"INS" : f'''{check_dependency}What is/are the perceived race(s) of the human subject(s) in the image? Ignore any overlaid text or caption.'''},
    },
    'output_format': {
        'v0': {"INS": '''''', 'post_process_func': False}
    }
}

# Are the people in the image female or male?
GENDER = {
    'name': "Gender", 'should_evaluate': False, 'take_image': True, 'gen_depend_on': [HUMAN['name']],
    'versions': {
        'v0': {"INS" : f'''{check_dependency}What is/are the gender(s) of the human subject(s) in the image? Ignore any overlaid text or caption.'''},
    },
    'output_format': {
        'v0': {"INS": '''''', 'post_process_func': False},
    }
}

APPEARANCE = {
    'name': "Appearance", 'should_evaluate': False, 'take_image': True, 'gen_depend_on': [HUMAN['name']],
    'versions': {
        'v0': {"INS" : f'''{check_dependency}What are the distinctive physical appearance characteristics of the human subject(s) in the image? Ignore any overlaid text or caption. Describe within three sentences.'''},
    },
    'versions': {
        'v1': {"INS" : f'''{check_dependency}What are the distinctive physical appearance characteristics of the human subject(s) in the image? Ignore any overlaid text or caption.'''},
    },
    'output_format': {
        'v0': {"INS": '''''', 'post_process_func': False},
    }
}
# --------------------------- For Unimodal LLMs --------------------#

UNIFY_SYS = '''You are a helpful assistant.''' #'''You are an expert in meme content comprehension and hatefulness detection.'''
from_Integrate = "{from_Integrate}"
INTEGRATE = {
    'name': "Integrate", 'should_evaluate': False, 'take_image': False, 
    'gen_depend_on': [HUMAN['name'], RACE['name'], GENDER['name'], APPEARANCE['name'], DESCRIBE['name']],
    # 'gen_depend_on': [DESCRIBE['name']],
    'versions': {
        'v0':{
            "INS": [
                f'''Given the following information provided about an online meme, synthesize and rephrase these information into a unified, coherent, and neutral description of the meme content. DO NOT mention the meme's tone and intent as humorous or light-hearted in the description. **Information**: {from_dependency}''',
                f'''The overlaid caption or text recognized in the meme reads: "{from_raw_data}".''',
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
        'stance': {
            'gen_depend_on': None,
            "INS": '''Output your previous conclusion as "Conclusion: your_choice_from_the_options". **Options**: 1. Neutral; 2. Support; 3. Oppose.''',
        },
        'subgroup': {
            'gen_depend_on': None,
            "INS": [
                # '''If you just concluded that the meme content does not explicitly focus on any specific LGBTQ+ subgroup, output "Conclusion: No specific subgroup referenced."''',
                # '''Otherwise, output "Conclusion: your_choices_from_the_provided_option_list".''',
                '''If you just concluded that the meme content particularly mentions, references or implicitly implies specific LGBTQ+ subgroup(s), output: "Conclusion: Your choice of the most directly referenced subgroup from the option list. Otherwise, output "Conclusion: No specific subgroup referenced or implied." ''',
                '''**Option list**:'''
                '''1. Gay; 2. Trans women; 3. Trans men; 4. (Semi-) Bisexual individuals; 5. Non-binary individuals; 6. Other subgroup not listed.''',
            ]
        },
        'hateTarget': {
            'gen_depend_on': None,
            "INS": '''Output "Conclusion: your_choice_from_the_option_list". **Option list**: 1. Undirected; 2. Specific Individual; 3. LGBTQ+ Community; 4. Organization.''',
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
        'children': {
            'gen_depend_on': [INTEGRATE['name']],
            "INS": [
                f'''Given the following description of an online meme related to LGBTQ+ movements,''',
                '''does the meme explicitly involve topics related to children, youth, or education?''',
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
        'media': {
            'gen_depend_on': [INTEGRATE['name']],
            "INS": [
                f'''Given the following description of an online meme related to LGBTQ+ movements,''',
                '''does the meme explicitly reference any streaming media platforms?''',
                f'''**Description of the meme content**: {from_dependency}''',
            ],
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
    },
    'output_format': {
        'stance': {"INS": '''''', 'post_process_func': pridemm_extract_stance},
        'subgroup': {"INS": '''''', 'post_process_func': pridemm_extract_subgroup},
        "hateTarget": {"INS": '''''', 'post_process_func': pridemm_extract_target},
        'y&n': {"INS": '''Start your response with "Yes," or "No," before giving any further explanation.''', 'post_process_func': extract_yes_or_no},
        'YN': {"INS": '''''', 'post_process_func': extract_yes_or_no}
    }
}


CoT_INS = '''Now, let's analyze by applying the guidelines one by one:'''
Classify_INS_community = '''classify the content as either harmful or harmless to LGBTQ+ community and supporters, based on widely accepted social norms, values, cultural understanding, and the provided guidelines.'''
Classify_INS_individual = '''classify the content as either harmful or harmless to the involved public figure, based on widely accepted social norms, values, cultural understanding, and the provided guidelines.'''
Classify_INS_organization = '''classify the content as either harmful or harmless to the public image of the involved organization, based on widely accepted social norms, values, cultural understanding, and the provided guidelines.'''

assign_prompt_by_target = '''{assign_prompt_by_target}'''
stage2_assign_prompt_by_target = '''{stage2_assign_prompt_by_target}'''
assign_Classify_INS = '''{assign_Classify_INS}'''
assign_classify_INS_by_target = '''{assign_classify_INS_by_target}'''
assign_GL_by_target = '''{assign_GL_by_target}'''
make_guidelines = '''{make_guidelines}'''
make_guidelines_based_on_hate_target = '''{make_guidelines_based_on_hate_target}'''
check_targets = '''{check_targets}'''
check_hate_target = '''{check_hate_target}'''
check_hate_target_hateful = '''{check_hate_target_hateful}'''
make_guidelines_based_on_hate_target_hateful = '''{make_guidelines_based_on_hate_target_hateful}'''
from_pos_aux_info = '''{from_pos_aux_info}'''
REASONING = {
    'name': "Reasoning", 'should_evaluate': False, 'take_image': False,
    'versions': {
        'CoT*': {
            'gen_depend_on': [INTEGRATE['name']],
            'INS': [
                f'''Given the following description of an online meme related to LGBTQ+ pride movements,''',
                # '''classify the meme as either "harmful" or "harmless" to the public image of LGBTQ+ community, its supporters, allies, as well as pride movements, based on widely accepted social norms, values, cultural understanding, and the provided guidelines.''',
                '''classify the content as either harmful or harmless to LGBTQ+ community and supporters, based on widely accepted social norms, values, cultural understanding, and the provided guidelines.''',
                #f'''{assign_Classify_INS}''',
                # '''classify the content as either harmful or harmless to the public image of LGBTQ+ community based on common values, knowledge, social norms and the provided guidelines.''',
                f'''Guidelines: {make_guidelines}''',
                #f'''Guidelines: {KNOWLEDGE_7092}''',
                f'''**Meme content you need to classify**: {from_dependency}''',
                #f'''{from_pos_aux_info}''',
                #'''**Now, let's analyze step by step**:''',
                # '''Now, let's analyze by applying the guidelines one by one:'''
                CoT_INS
            ]
        },
        'CoTxTarget': {
            'gen_depend_on': [INTEGRATE['name']],
            'INS': [
                f'''Given the following description of an online meme related to LGBTQ+ pride movements,''',
                f'''{assign_prompt_by_target}''',
                f'''**Meme content you need to classify**: {from_dependency}''',
                CoT_INS
            ]
        },
        'CoTxTarget2': {
            'gen_depend_on': [INTEGRATE['name']],
            'INS': f'''{stage2_assign_prompt_by_target}'''
        },
        'stance':{
            'gen_depend_on': [INTEGRATE['name']],
            "INS": [
                f'''Given the following description of an online meme related to LGBTQ+ pride movements,''',
                '''analyze: what is the meme's stance toward the LGBTQ+ movement and community? Choose the most accurate stance from "Neutral", "Support" and "Oppose".''',
                #f'''**Guidelines**: {Stance_GL}''',
                f'''**Meme content you need to analyze**: {from_dependency}''',
                '''**Now, let's analyze step by step**:'''
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
        'hateTarget': {
            'gen_depend_on': [INTEGRATE['name']],
            "INS": [
                f'''Given the following description of an online meme related to LGBTQ+ movements, analyze: What is the meme's target subject? Select the most appropriate category from these options: 1. Undirected; 2. Specific Individual; 3. LGBTQ+ Community; 4. Organization. **Target Classification Guidelines**: {TG_GL}''',
                f'''**Description of the meme content**: {from_dependency}''',
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
        'CoT': {
            'gen_depend_on': [INTEGRATE['name']],
            'INS': [
                f'''Given the following description of an online meme related to LGBTQ+ movements,''',
                '''classify the meme content as either "harmful" or "harmless" to the public image of LGBTQ+ community based on common values, knowledge and social norms.''',# and the provided guidelines
                # '''classify the meme content as either harmful or harmless to the LGBTQ+ community based on common values, knowledge and social norms.''',
                f'''**Guidelines**: {make_guidelines}''',
                f'''**Meme content you need to classify**: {from_dependency}''',
                '''**Now, let's analyze step by step**:'''
            ]
        },
        'Target_Entity': {
            'gen_depend_on': [INTEGRATE['name']],
            'INS': [
                f'''Given the following description of an online meme related to LGBTQ+ movements,''',
                '''analyze: what aspects are explicitly involved in the meme content?''',
                '''Here are some guidelines for your reference:''',
                '''A. If the content does not seem to explicitly mention any specific sociocultural entities, just output "No specific sociocultural entity mentioned."''',
                '''B. Otherwise, choose your answer(s) from the provided list (you may choose multiple options if there are more than one entity mentioned):''',
                '''1. Women (Female); 2. Children (Kids); 3. Corporations; 4. Streaming media platforms; 5. Goverment; 6. Political ideologies or parties; 7. Religions; 8. Countries or regions; 9. Celebrities. 10. Other sociocultural entities not listed.''',
                f'''**Meme content you need to analyze**: {from_dependency}''',
                '''Now, let's analyze step by step:'''
            ]
        },
        'CoTtg': {
            'gen_depend_on': [INTEGRATE['name']],
            "INS": [
                f'''Given the following description of an online meme related to LGBTQ+ movements,''',
                f'''classify the meme content as either "harmful" or "harmless" {check_hate_target} based on common values, knowledge and social norms.''',
                f'''{make_guidelines_based_on_hate_target}''',
                f'''**Meme content you need to classify**: {from_dependency}''',
                '''**Now, let's analyze step by step**:'''
            ]
        },
        'CoTHateTg': {
            'gen_depend_on': [INTEGRATE['name']],
            "INS": [
                f'''Given the following description of an online meme related to LGBTQ+ movements,''',
                f'''classify the meme content as either "hateful" or "non-hateful" {check_hate_target_hateful} based on common values, knowledge and social norms.''',
                f'''{make_guidelines_based_on_hate_target_hateful}''',
                f'''**Meme content you need to classify**: {from_dependency}''',
                '''**Now, let's analyze step by step**:'''
            ]
        },
        'CoT2': {
            'gen_depend_on': [INTEGRATE['name']],
            'INS': [
                f'''Given the following description of an online meme related to LGBTQ+ movements,''',
                '''classify the meme content as either "harmful to some targets" or "harmless in general" based on common values, knowledge and social norms.''',# and the provided guidelines
                # '''classify the meme content as either harmful or harmless to the LGBTQ+ community based on common values, knowledge and social norms.''',
                f'''**Guidelines**: {make_guidelines}''',
                f'''**Meme content you need to classify**: {from_dependency}''',
                '''**Now, let's analyze step by step**:'''
            ]
        },
        'CoT3': {
            'gen_depend_on': [INTEGRATE['name']],
            'INS': [
                f'''Given the following description of an online meme related to LGBTQ+ movements,''',
                '''classify the meme content as either "hateful toward certain targets" or "non-hateful in general" based on common values, knowledge and social norms.''',# and the provided guidelines
                # '''classify the meme content as either harmful or harmless to the LGBTQ+ community based on common values, knowledge and social norms.''',
                f'''**Guidelines**: {make_guidelines}''',
                f'''**Meme content you need to classify**: {from_dependency}''',
                '''**Now, let's analyze step by step**:'''
            ]
        },
        'CoT1': {
            'gen_depend_on': [INTEGRATE['name']],
            'INS': [
                f'''Given the following description of an online meme related to LGBTQ+ movements,''',
                '''Classify the meme content as either hateful or non-hateful toward the LGBTQ+ community, based on widely accepted social norms, cultural context, and established understanding of harmful stereotypes, biases, and discriminatory narratives.''',
                f'''**Guidelines**: {make_guidelines}''',
                f'''**Meme content you need to classify**: {from_dependency}''',
                '''**Now, let's analyze step by step**:'''
            ]
        },
        'Interpret': {
            'gen_depend_on': [INTEGRATE['name']],
            'INS': [
                f'''Given the following description of an image,''',
                '''interpret its intended message perceived by a general, unbiased audience within two sentences.''',
                f'''**Image description**: {from_dependency}'''
            ]
        },
        'CoTwTGC': {
            'gen_depend_on': [INTEGRATE['name']],
            'INS': [
                f'''Given the following description of an online meme related to LGBTQ+ pride movement,''',
                '''classify the content as either harmful or harmless to the public image of LGBTQ+ community based on common values, knowledge, social norms and the provided guidelines.''',
                # '''classify the content as either offensive or non-offensive to the LGBTQ+ community based on common values, knowledge, social norms and the provided guidelines.''',
                f'''Guidelines: {check_targets}''',#some tips
                f'''**Meme content you need to classify**: {from_dependency}''',
                #f'''The text overlaid on the image reads "{from_raw_data}".''',
                #f'''{from_previous_turn}''',
                '''**Now, let's analyze by applying the guidelines one by one**:'''
            ]
        },
        'Target_ori': {
            'gen_depend_on': [INTEGRATE['name']],
            'INS': [
                f'''Given the following description of an online meme related to LGBTQ+ pride movement,''',
                '''analyze: what social or cultural groups are probably involved in the meme content?''',
                '''Here are some guidelines for your reference:''',
                '''A. If the content does not seem to involve any specific sociocultural group, just output "No specific sociocultural group involved."''',
                '''B. Otherwise, choose your answer(s) from the provided list (you may choose multiple options if there are more than one group involved):''',
                '''1. Gay; 2. Transgender individuals; 3. (Semi-) Bisexual individuals; 4. Other LGBTQ+ groups; 5. LGBTQ+ community as a whole; 6. Women (Female); 7. Corporations; 8. Streaming media platforms; 9. Goverment; 10. Political ideologies or parties; 11. Religions; 12. Countries or regions; 13. Celebrities. 14. Other sociocultural groups not listed.''',
                f'''**Meme content you need to analyze**: {from_dependency}''',
                '''Now, let's analyze step by step:'''
            ]
        },
    },
    'output_format': {
        'v0': {"INS": '''''', 'post_process_func': post_process_to_remove_gibberish},
    }
}
check_what_hate_target = '''{check_what_hate_target}'''
EXTRACT = {
    'name': "Extract", 'should_evaluate': False,'take_image': False, 'gen_depend_on': None,
    'versions': {
        'Target': {
            "INS": '''Output "Conclusion: your_choice_from_the_option_list". **Option list**: 1. Undirected; 2. Specific Individual; 3. LGBTQ+ Community; 4. Organization.''',
        },
        'WhatTarget': {
            "INS": f'''{check_what_hate_target}''',
        },
        'Target_LGBT': {
            "INS": [
                '''If you concluded that the content does not explicitly mention any specific LGBTQ+ subgroup, output "Conclusion: No specific subgroup mentioned."''',
                '''Otherwise, output "Conclusion: your_choices_from_the_provided_option_list".''',
                '''(Option list:'''
                '''1. Gay; 2. Transgender; 3. (Semi-) Bisexual; 4. Other LGBTQ+ subgroups not listed.)''',
            ]
        },
        'Target_Entity': {
            "INS": [
                '''If you concluded that the content does not explicitly mention any specific sociocultural entity, output "Conclusion: No specific sociocultural entity mentioned."''',
                '''Otherwise, output "Conclusion: your_choices_from_the_provided_option_list".''',
                '''(Option list:'''
                '''1. Women (Female); 2. Children (Kids); 3. Corporations; 4. Streaming media platforms; 5. Goverment; 6. Political ideologies or parties; 7. Religions; 8. Countries or regions; 9. Celebrities. 10. Other sociocultural entities not listed.)''',
            ]
        },
        'Target_ori': {
            "INS": [
                '''If you concluded that the content does not involve any specific sociocultural groups, output "Conclusion: No specific sociocultural group involved."''',
                '''Otherwise, output "Conclusion: your_choices_from_the_provided_option_list".''',
                '''(Option list:'''
                '''1. Gay; 2. Transgender individuals; 3. (Semi-) Bisexual individuals; 4. Other LGBTQ+ groups; 5. LGBTQ+ community as a whole; 6. Women (Female); 7. Corporations; 8. Streaming media platforms; 9. Goverment; 10. Political ideologies or parties; 11. Religions; 12. Countries or regions; 13. Celebrities. 14. Other sociocultural groups not listed.)''',
            ]
        },
    },
    'output_format': {
        'v0': {"INS": '''''', 'post_process_func': pridemm_extract_target_group},
        'lgbt': {"INS": '''''', 'post_process_func': pridemm_extract_lgbt_subgroup},
        'entity': {"INS": '''''', 'post_process_func': pridemm_extract_entity},
        "target": {"INS": '''''', 'post_process_func': pridemm_extract_target}
    },
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

assign_decision_prompt_by_target = '''{assign_decision_prompt_by_target}'''
DECISION = {
    'name': "Decision", 'should_evaluate': True, 'take_image': False,
    'versions': {
        'v0': {
            'gen_depend_on': None,
            'INS': f'''If you just classified the meme content as harmful (either explicitly or implicitly), output "Conclusion: Harmful." Otherwise, output "Conclusion: Harmless."''',
            # 'INS': f'''If you just classified the meme content as harmful toward LGBTQ+ community, output "Conclusion: Harmful." Otherwise, output "Conclusion: Harmless."''', 
            # towards the public image of LGBTQ+ community
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

stage2_assign_decision_prompt_by_target = '''{stage2_assign_decision_prompt_by_target}'''
STEP_DECISION = {
    'name': "StepDecision", 'take_image': False,
    'versions': {
        's1': {
            'should_evaluate': False, 
            'gen_depend_on': None,
            'INS': f'''If you just classified the meme content as harmful (either explicitly or implicitly), output "Conclusion: Harmful." Otherwise, output "Conclusion: Harmless."''',
        },
        's2': {
            'should_evaluate': True, 
            'gen_depend_on': None,
            'INS': f'''{stage2_assign_decision_prompt_by_target}''',
        },
    },
    'output_format': {
        'v0': {"INS": '''''', 'post_process_func': extract_classification_label},
    }
}

def stage2_assign_decision_extract_by_target(js):
    assert "aux_info" in js
    aux_info = js["aux_info"]
    assert "step_decision" in js
    step_decision = js["step_decision"]
    skip_run = '''Output "Skip".'''
    if step_decision["s1"]["pred_label"] == 0:
        if aux_info["individual"] is not None:
            assert aux_info["individual"]["flag"] == 1
            if aux_info["hateTarget"] == "individual":
                if aux_info["LGBTQindividual"] is None:
                    # Non-LGBTQ+ individual
                    plh = "individual"
                else:
                    plh = "LGBTQ+ individual"
                return f'''If you just classified the meme content as hurtful (either explicitly or implicitly) to the {plh}, output "Conclusion: Hurtful." Otherwise, output "Conclusion: Non-hurtful."'''
        else:
            #if aux_info["organization"] is not None:
            if (aux_info["hateTarget"] == "organization") and (aux_info["organization"] is not None):
                return f'''If you just classified the meme content as harmful (either explicitly or implicitly) to the public image of the organization, output "Conclusion: Harmful." Otherwise, output "Conclusion: Harmless."'''
        return skip_run
    else:
        return skip_run


def assign_decision_extract_by_target(js):
    assert "aux_info" in js
    aux_info = js["aux_info"]
    use_default = False
    if aux_info["individual"] is not None:
        assert aux_info["individual"]["flag"] == 1
        if aux_info["hateTarget"] == "individual":
            if aux_info["LGBTQindividual"] is None:
                # Non-LGBTQ+ individual
                plh = "individual"
            else:
                plh = "LGBTQ+ individual"
            return f'''If you just classified the meme content as hurtful (either explicitly or implicitly) to the {plh}, output "Conclusion: Hurtful." Otherwise, output "Conclusion: Non-hurtful."'''
    else:
        #if aux_info["organization"] is not None:
        if (aux_info["hateTarget"] == "organization") and (aux_info["organization"] is not None):
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
            1: {'template': DECISION, "version": "gpt", "out_format": 'v0'},
        }
    }
}

M2T = {
    'lmm': {
        'prompt': {
            0: {'template': HUMAN, "version": "v0", "out_format": 'v0'}, 
            1: {'template': RACE, "version": "v0", "out_format": 'v0'},
            2: {'template': GENDER, "version": "v0", "out_format": 'v0'},
            3: {'template': APPEARANCE, "version": "v0", "out_format": 'v0'},
            4: {'template': APPEARANCE, "version": "v1", "out_format": 'v0'},
            #4: {'template': CELEB, "version": "v0", "out_format": 'v0'},
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
d6 = {
    'llm_2': {
        'multi-turn': False,
        'prompt': {
            0: {'template': AUX, "version": "children", "out_format": 'y&n'},#, "load_from_prestep": True, "return_prestep_path": True
            1: {'template': AUX, "version": "religion", "out_format": 'y&n', "load_from_prestep": True, "return_prestep_path": True},
            2: {'template': AUX, "version": "media", "out_format": 'y&n', "load_from_prestep": True, "return_prestep_path": True},
            3: {'template': AUX, "version": "country", "out_format": 'y&n', "load_from_prestep": True, "return_prestep_path": True},
            4: {'template': AUX, "version": "politic", "out_format": 'y&n', "load_from_prestep": True, "return_prestep_path": True},
            5: {'template': AUX, "version": "company1", "out_format": 'y&n', "load_from_prestep": True, "return_prestep_path": True},
            6: {'template': AUX, "version": "company2", "out_format": 'y&n', "load_from_prestep": True, "return_prestep_path": True},
            7: {'template': AUX, "version": "company3", "out_format": 'y&n', "load_from_prestep": True, "return_prestep_path": True},
            8: {'template': AUX, "version": "self", "out_format": 'y&n', "load_from_prestep": True, "return_prestep_path": True},
        }
    },
    'llm_3': {
        'multi-turn': True,
        'prompt': {
            0: {'template': REASONING, "version": "subgroup", "out_format": 'v0', "load_from_prestep": True, "return_prestep_path": True},#, 'max_new_tokens': 1536
            1: {'template': AUX, "version": "subgroup", "out_format": 'subgroup'},
        }
    },
    'llm_4': {
        'multi-turn': True,
        'prompt': {
            0: {'template': REASONING, "version": "hateTarget", "out_format": 'v0', "load_from_prestep": True, "return_prestep_path": True},
            2: {'template': AUX, "version": "hateTarget", "out_format": 'hateTarget'}
        }
    },
    'llm_5': {
        'multi-turn': True,
        'prompt': {
            0: {'template': REASONING, "version": "individual", "out_format": 'v0', "load_from_prestep": True, "return_prestep_path": True},
            3: {'template': AUX, "version": "individual", "out_format": 'YN'},
            4: {'template': AUX, "version": "LGBTQindividual", "out_format": 'YN'},
        }
    },
    'llm_6': {
        'multi-turn': True,
        'prompt': {
            0: {'template': REASONING, "version": "organization", "out_format": 'v0', "load_from_prestep": True, "return_prestep_path": True},
            5: {'template': AUX, "version": "organization", "out_format": 'YN'}
        }
    },
    # 'llm_5': {
    #     'multi-turn': True,
    #     'prompt': {
    #         0: {'template': REASONING, "version": "stance", "out_format": 'v0', "load_from_prestep": True, "return_prestep_path": True},
    #         3: {'template': AUX, "version": "stance", "out_format": 'stance'}
    #     }
    # },
    # 'llm_7': {
    #     'multi-turn': True,
    #     'prompt': {
    #         6: {'template': REASONING, "version": "CoT*", "out_format": 'v0', 'new_conversation': True, 'depend_on_prestep': True, 'max_new_tokens': 1536},#'max_new_tokens': 1536
    #         7: {'template': DECISION, "version": "v0", "out_format": 'v0'}
    #     }
    # },
    
    # best so far
    'llm_7': {
        'multi-turn': True,
        'prompt': {
            6: {'template': REASONING, "version": "CoTxTarget", "out_format": 'v0', 'new_conversation': True, 'depend_on_prestep': True, 'max_new_tokens': 1536},#'max_new_tokens': 1536
            7: {'template': DECISION, "version": "tg", "out_format": 'v0'}
        }
    },

    # # Staged scheme
    # 'llm_7': {
    #     'multi-turn': True,
    #     'prompt': {
    #         6: {'template': REASONING, "version": "CoT*", "out_format": 'v0', 'new_conversation': True, 'depend_on_prestep': True, 'max_new_tokens': 1536},
    #         7: {'template': STEP_DECISION, "version": "s1", "out_format": 'v0'},
    #         8: {'template': REASONING, "version": "CoTxTarget2", "out_format": 'v0', 'new_conversation': True, 'depend_on_prestep': True, 'max_new_tokens': 1536},
    #         9: {'template': STEP_DECISION, "version": "s2", "out_format": 'v0'}
    #     }
    # },
  
    # 'llm_2': {
    #     'multi-turn': True,
    #     'prompt': {
    #         # 0: {'template': REASONING, "version": "Target_LGBT", "out_format": 'v0'},
    #         # 1: {'template': EXTRACT, "version": "Target_LGBT", "out_format": 'lgbt'},
    #         # 2: {'template': REASONING, "version": "Target_Entity", "out_format": 'v0', 'new_conversation': True, 'depend_on_prestep': True},
    #         # 3: {'template': EXTRACT, "version": "Target_Entity", "out_format": 'entity'},
    #         # # 4: {'template': REASONING, "version": "Interpret", "out_format": 'v0', 'new_conversation': True, 'depend_on_prestep': True, 'max_new_tokens': 256},
    #         # 4: {'template': REASONING, "version": "CoTwTGC", "out_format": 'v0', 'new_conversation': True, 'depend_on_prestep': True},
    #         # 5: {'template': DECISION, "version": "v1", "out_format": 'v0'}
            
    #         # 0: {'template': REASONING, "version": "CoT", "out_format": 'v0'},#, 'max_new_tokens': 1536
    #         # 1: {'template': DECISION, "version": "v0", "out_format": 'v0'}

    #         0: {'template': REASONING, "version": "Target", "out_format": 'v0'},#, 'max_new_tokens': 1536
    #         1: {'template': EXTRACT, "version": "Target", "out_format": 'target'},

    #         2: {'template': REASONING, "version": "CoTHateTg", "out_format": 'v0', 'new_conversation': True, 'depend_on_prestep': True},
    #         3: {'template': DECISION, "version": "v1", "out_format": 'v0'}

    #         # 0: {'template': REASONING, "version": "CoT1", "out_format": 'v0'},
    #         # 1: {'template': DECISION, "version": "v1", "out_format": 'v0'}
    #     }
    # }
}

D6 = dict(**M2T, **d6)

# ******************************************************************************************* # 

PrideMM_PROMPT_SCHEMES = {
    'B1': B1,
    'GPT': GPT,
    'M2T': M2T,
    'D6': D6,
}

def assign_Classify_INS_by_target(js):
    assert "aux_info" in js
    aux_info = js["aux_info"]
    if aux_info['hateTarget'] in ["lgbtq", "undirected"]:
        return Classify_INS_community
    if aux_info['hateTarget'] == "individual":
        return Classify_INS_individual
    if aux_info['hateTarget'] == "organization":
        return Classify_INS_organization
    
def assign_guidelines(js):
    # pre_GL = [R1]#, R2, R3, R4, R5
    # GL = " ".join([f"{rid+1}. {rule}" for rid, rule in enumerate(pre_GL)])
    assert "aux_info" in js
    aux_info = js["aux_info"]
    Rules = [R_combine, R_neutral, R_stance, R_explicit, R_implicit]
    Rules = [R_interpret, R_stance, R_explicit, R_implicit]
    Rules = [R_interpret, R_stance, R_explicit, R_implicit_new]
    
    R_harmful_new_ = R_harmful_new
    # R_harmful_new_ = " ".join([R_harmful_new_start, R_harmful_new_examples])

    # # Subgroup
    aux_subg = aux_info["subgroup"]
    r_subgroup = ""
    text = ""
    if aux_subg:
        if (len(aux_subg) == 1):
            one_sg = aux_subg[0]
            text = one_sg
            examples = ""
            # if one_sg.lower().startswith("trans"):
            #     examples = f"\n".join([TYPES["Trans"], TYPES[one_sg]])
            # elif one_sg.lower().startswith("other"):
            #     examples = TYPES["LGBTQ+ subgroups"]
            # else:
            #     examples = TYPES[one_sg]
            if ("bisexual" in one_sg.lower()) or ("subgroups" in one_sg.lower()):
                examples = TYPES["(Semi-) Bisexual individuals"]
            r_subgroup = f'''{examples}'''
    #     else:
    #         subgs = []
    #         subg_examples = []
    #         if all([w in aux_subg for w in ["Trans women", "Trans men"]]):
    #             subgs.append("transgender individuals")
    #             subg_examples.append(TYPES["Trans"])
    #         else:
    #             if "Trans women" in aux_subg:
    #                 subgs.append("trans women")
    #                 subg_examples.extend([TYPES["Trans"], TYPES["Trans women"]])
    #         others = [w for w in aux_subg if not w.lower().startswith("trans")]
    #         if others:
    #             if len(others) > 1:
    #                 subgs.append("other LGBTQ+ subgroups")
    #                 subg_examples.append(TYPES["LGBTQ+ subgroups"])
    #         if subgs:
    #             if len(subgs) > 1:
    #                 text = " ".join([", ".join(subgs[:-1]), f"and {subgs[-1]}"])
    #             else:
    #                 text = subgs[0]
    #             examples = f"\n".join(subg_examples)
    #             r_subgroup = f'''{examples}'''
    # if ("gay" in js['text'].lower().split()) and ("gay" not in text.lower()):
    #     r_subgroup = " ".join([r_subgroup, TYPES["Gay"]])

    if r_subgroup:
        # R_harmful_new_ = f"{R_harmful_new_start} {r_subgroup} {R_harmful_new_examples}" 
        R_harmful_new_ = f"{R_harmful_new_} {r_subgroup}"
    # if aux_info["hateTarget"] == "lgbtq":
    #     Rules.append(R_harmful)    
    
    # Specific aspects
    issues = []
    for k, item in aux_info.items():
        if (k != "self") and (not k.startswith("company")) and (k in ['country', 'politic']):
            if isinstance(item, dict) and item["flag"]:
                topic = TYPES[k]['topic']
                examples = TYPES[k]['examples']
                issues.append(f"{examples}")
    if any([item["flag"] for k, item in aux_info.items() if k.startswith("company")]):
        topic = TYPES["company"]['topic']
        examples = TYPES["company"]['examples']
        issues.append(f"{examples}")
    R_harmful_indirect = ""
    if issues:
        R_harmful_new_ = " ".join([R_harmful_new_, f" ".join(issues)])
        # R_harmful_indirect = " ".join([R_harmful_indirectly, f" ".join(issues)])
    
    # #Rules.append(R_harmful_violence)
    # #Rules.append(R_harmful_ori)
    Rules.append(R_harmful_new_)

    if R_harmful_indirect:
        Rules.append(R_harmful_indirect)

    # # Harmless
    if aux_info["self"]["flag"]:
        Rules.append(TYPES["self"])

    Rules.append(R_harmless_ori)
    # Rules.append(R_harmless)
    # Rules.append(R_harmless_support)
    GL = f"\n".join([f"{rid+1}. {rule}" for rid, rule in enumerate(Rules)])
    return GL


def assign_prompt_INS_by_target(js):
    assert "aux_info" in js
    aux_info = js["aux_info"]

    # if aux_info['hateTarget'] in ["lgbtq", "undirected"]:
    #     Rules = [R_interpret, R_stance, R_explicit, R_implicit_new, R_harmful_new]
    #     if aux_info["self"]["flag"]:
    #         Rules.append(TYPES["self"])
    #     Rules.append(R_harmless_ori)
    # if aux_info['hateTarget'] == "individual":
    #     Rules = [R_interpret, R_stance_individual, R_explicit_individual, R_implicit_individual, R_harmless_ori]
    # if aux_info['hateTarget'] == "organization":
    #     Rules = [R_interpret, R_stance_organization, R_explicit_organization, R_implicit_organization, R_harmful_organization, R_harmless_ori]
    use_default = False
    if aux_info["individual"] is not None:
        assert aux_info["individual"]["flag"] == 1
        if aux_info["hateTarget"] == "individual":
            if aux_info["LGBTQindividual"] is None:
                # Non-LGBTQ+ individual
                plh = "individual"
                Rules = [Individual_GL, R_interpret, R_stance_individual, R_explicit_individual, R_implicit_individual, R_harmless_ori]
            else:
                plh = "LGBTQ+ individual"
                Rules = [R_interpret, R_stance_lgbt_individual, R_explicit_individual, R_implicit_lgbt_individual, R_harmful_lgbt_individual, R_harmless_ori]
            classify_ins = f'''classify the content as either hurtful or non-hurtful to the specific {plh} involved, according to widely accepted social norms, values, cultural understanding, and the provided guidelines.'''
        else:
            use_default = True
    else:
        #if aux_info["organization"] is not None:
        if (aux_info["hateTarget"] == "organization") and (aux_info["organization"] is not None):
            Rules = [R_organization, R_interpret, R_explicit_organization, R_implicit_organization, R_harmful_organization, R_harmless_ori]
            classify_ins = f'''classify the content as either harmful or harmless to the public image of the organization(s) involved, according to widely accepted social norms, values, cultural understanding, and the provided guidelines.'''
        else:
            use_default = True
    if use_default:
        Rules = assign_guidelines(js)
        classify_ins = '''classify the content as either harmful or harmless to LGBTQ+ community and supporters, based on widely accepted social norms, values, cultural understanding, and the provided guidelines.'''
    
    if isinstance(Rules, list):
        GL = f"\n".join([f"{rid+1}. {rule}" for rid, rule in enumerate(Rules)])
    else:
        GL = Rules
    prompt = " ".join([classify_ins, f"Guidelines: {GL}"])
    return prompt

def stage2_assign_prompt_INS_by_target(js):
    assert "aux_info" in js
    aux_info = js["aux_info"]
    assert "step_decision" in js
    step_decision = js["step_decision"]
    skip_run = '''Output "Skip".'''
    if step_decision["s1"]["pred_label"] == 0:
        ins1 = f'''Given the following description of an online meme related to LGBTQ+ pride movements,'''
        dp_pred_key = 'processed_dependency_prediction'
        if dp_pred_key not in js:
            dp_pred_key = "processed_prediction"
        dp_pred = js.pop(dp_pred_key)
        assert isinstance(dp_pred, str)
        ins3 = f'''**Meme content you need to classify**: {dp_pred}'''
        ins4 = CoT_INS

        need_run = True
        if aux_info["individual"] is not None:
            assert aux_info["individual"]["flag"] == 1
            if aux_info["hateTarget"] == "individual":
                if aux_info["LGBTQindividual"] is None:
                    # Non-LGBTQ+ individual
                    plh = "individual"
                    Rules = [Individual_GL, R_interpret, R_stance_individual, R_explicit_individual, R_implicit_individual, R_harmless_ori]
                else:
                    plh = "LGBTQ+ individual"
                    Rules = [R_interpret, R_stance_lgbt_individual, R_explicit_individual, R_implicit_lgbt_individual, R_harmful_lgbt_individual, R_harmless_ori]
                classify_ins = f'''classify the content as either hurtful or non-hurtful to the specific {plh} involved, according to widely accepted social norms, values, cultural understanding, and the provided guidelines.'''
            else:
                need_run = False
        else:
            #if aux_info["organization"] is not None:
            if (aux_info["hateTarget"] == "organization") and (aux_info["organization"] is not None):
                Rules = [R_organization, R_interpret, R_explicit_organization, R_implicit_organization, R_harmful_organization, R_harmless_ori]
                classify_ins = f'''classify the content as either harmful or harmless to the public image of the organization(s) involved, according to widely accepted social norms, values, cultural understanding, and the provided guidelines.'''
            else:
                need_run = False
        if need_run:
            if isinstance(Rules, list):
                GL = f"\n".join([f"{rid+1}. {rule}" for rid, rule in enumerate(Rules)])
            else:
                GL = Rules
            ins2 = " ".join([classify_ins, f"Guidelines: {GL}"])
            prompt = " ".join([ins1, ins2, ins3, ins4])
            return prompt
        else:
            return skip_run
    else:
        return skip_run

def add_aux_info(js):
    add_info = []
    additional_info = ""
    assert "aux_info" in js
    aux_info = js["aux_info"]
    # Subgroup
    aux_subg = aux_info["subgroup"]
    if aux_subg:
        if len(aux_subg) > 1: 
            text = " ".join([", ".join(aux_subg[:-1]), f"and {aux_subg[-1]}"])
        else:
            text = aux_subg[0]
        subg_info = f"The meme content specifically focuses on or implies the LGBTQ+ subgroup(s) of {text}."
        add_info.append(subg_info)
    # Specific aspects
    for k, item in aux_info.items():
        if isinstance(item, dict) and (k != "self") and item["flag"]:
            add_info.append(item["output"])
    # Self-reflective
    if aux_info["self"]["flag"]:
        add_info.append(aux_info["self"]["output"])
    if additional_info:
        additional_info = f"\n".join(add_info)
    return additional_info

def assign_what_target(js):
    if js["Target"]:
        tg_map= {
            'individual': '''So, according to the meme content, what is the specific individual being discussed? Start your response with "The specific individual being discussed is".''',
            'organization': '''So, according to the meme content, what is/are the specific organization(s) being discussed? Start your response with "The specific organization being discussed is".''',
            'undirected': '''So, according to the meme content, what is the specific topic being focused? Start your response with "The focused topic is".''',
        }
    return

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
    if make_guidelines in tmp:
        return tmp.format(make_guidelines = assign_guidelines(js)), js
    if assign_prompt_by_target in tmp:
        return assign_prompt_INS_by_target(js), js
    if assign_decision_prompt_by_target in tmp:
        return assign_decision_extract_by_target(js), js
    
    if stage2_assign_prompt_by_target in tmp:
        return stage2_assign_prompt_INS_by_target(js), js
    if stage2_assign_decision_prompt_by_target in tmp:
        return stage2_assign_decision_extract_by_target(js), js
    
    if assign_Classify_INS in tmp:
        return tmp.format(assign_Classify_INS = assign_Classify_INS_by_target(js)), js
    
    if check_if_has_individual in tmp:
        assert "aux_info" in js
        aux_info = js["aux_info"]
        #print(list(aux_info.keys()))
        a = f'''Output "No.".'''
        if "individual" in list(aux_info.keys()):
            if aux_info["individual"] is not None:
                assert aux_info["individual"]["flag"] == 1
                a = f'''Is this specific individual an LGBTQ+ individual? Start your response with "Yes," or "No," before giving any further explanation.'''           
        return a, js
    
    if from_pos_aux_info in tmp:
        return tmp.format(from_pos_aux_info = add_aux_info(js)), js
    
    if check_hate_target in tmp:
        text = ""
        if js["Target"]:
            map_ = {
                'individual': '''to the public image of the specific individual involved''',
                'organization': '''to the public image of the organization(s) involved''',
                'community': '''to the public image of the LGBTQ+ community''',
                'undirected': ""
            }
            text = map_[js["Target"]]
        return tmp.format(check_hate_target = text), js
    
    # if make_guidelines_based_on_hate_target in tmp:
    #     GL = ""
    #     if js["Target"] == 'community':
    #         GL = " ".join([f"{rid+1}. {rule}" for rid, rule in enumerate([R2, R3new, R45])])
    #         GL = f'''**Guidelines**: {GL}'''
    #     if js["Target"] == 'individual':
    #         GL = f'''**Cautions**: {R_individual}'''
    #     return tmp.format(make_guidelines_based_on_hate_target = GL), js
    
    if check_hate_target_hateful in tmp:
        text = ""
        if js["Target"]:
            map_ = {
                'individual': '''to the specific individual involved''',
                'organization': '''to the organization(s) involved''',
                'community': '''to the LGBTQ+ community''',
                'undirected': ""
            }
            text = map_[js["Target"]]
        return tmp.format(check_hate_target_hateful = text), js
    if make_guidelines_based_on_hate_target_hateful in tmp:
        GL = ""
        return tmp.format(make_guidelines_based_on_hate_target_hateful = GL), js
    
    if check_what_hate_target in tmp:
        return tmp.format(check_what_hate_target = assign_what_target(js)), js
    if check_targets in tmp:
        assert ("Target_Entity" in js) and ("Target_LGBT" in js)
        targets = js["Target_Entity"] + js["Target_LGBT"]
        knowledge = GL.format(plh = " ".join([TYPES[tg] for tg in targets if tg in TYPES]))
        return tmp.format(check_targets = knowledge), js
    
    if from_previous_turn in tmp:
        dp_pred_key = "processed_prediction"
        dp_pred = js.pop(dp_pred_key)
        return tmp.format(from_previous_turn = dp_pred), js
   
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