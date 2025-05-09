from utils.knowledge.pridemm import *
from utils.tool import *
from_raw_data = '{from_raw_data}'
from_dependency = '{from_dependency}'
from_previous_turn = '{from_previous_turn}'
# --------------------------- For Multimodal LMMs --------------------#
introduce = f'''This is a meme with an overlaid caption: "{from_raw_data}".'''
main_instruction = '''classify the given meme as either hateful or non-hateful considering both the image content and its caption.'''
DIRECT_CLASSIFY = {
    'name': "Classify",
    'should_evaluate': True,
    'take_image': True,
    'gen_depend_on': None,
    'versions': {
        'v3': {
            'INS': f'''{introduce} Based on commonsense knowledge, determine whether or not the meme is potentially offensive, harmful or hateful.'''
        },
        'v4': {
            'INS': f'''{introduce} Based on commonsense knowledge, classify the given meme as either harmful or benign.'''
        }
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

DESCRIBE = {
    'name': "Describe",
    'should_evaluate': False,
    'take_image': True,
    'gen_depend_on': None,
    'versions': {
        'v0': {
            "INS" : '''This is an online meme related to LGBTQ+ pride movement. Question: What is this meme about? Note: DO NOT ASSUME the nature of the meme's tone and intent as humorous or lighthearted. Describe in a neutral tone.''',
        },
        'v1': {
            "INS" : '''This is an online meme related to LGBTQ+ pride movements. Describe the meme's content objectively, without interpreting its underlying implications. Caution: Do not assume the meme’s tone or intent to be humorous or lighthearted. Maintain a neutral and descriptive tone.''',
        },
        'v2': {
            "INS" : '''Question: What is this image about? Note: Transcribe any overlaid text without interpreting its implications. DO NOT assume the image's tone or intent as humorous or lighthearted.''',
        },
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
        'v0': {"INS" : f'''{check_dependency}What are the distinctive physical appearance characteristics of the human subject(s) in the image? Ignore any overlaid text or caption.'''},
    },
    'output_format': {
        'v0': {"INS": '''''', 'post_process_func': False},
    }
}
# --------------------------- For Unimodal LLMs --------------------#

UNIFY_SYS = '''You are a helpful assistant.''' #'''You are an expert in meme content comprehension and hatefulness detection.'''
from_Integrate = "{from_Integrate}"
INTEGRATE = {
    'name': "Integrate", 'should_evaluate': False, 'take_image': False, 'gen_depend_on': [HUMAN['name'], RACE['name'], GENDER['name'], APPEARANCE['name'], DESCRIBE['name']],
    'versions': {
        'v0':{
            "INS": [
                f'''Given the following information provided about an online meme, synthesize and rephrase these information into a unified, comprehensive and neutral description of the meme content. Note: Transcribe any overlaid text without paraphrasing. DO NOT mention the meme's tone and intent as humorous or lighthearted in the description. **Information**: {from_dependency}''',
                f'''The caption or text recognized in the image reads "{from_raw_data}".''',
            ]
        }    
    },
    'output_format': {
        'v0': {"INS": '''''', 'post_process_func': post_process_to_remove_gibberish},
    }
}


check_targets = '''{check_targets}'''
REASONING = {
    'name': "Reasoning", 'should_evaluate': False, 'take_image': False,
    'versions': {
        'CoTwContext': {
            'gen_depend_on': [INTEGRATE['name']],
            'INS': [
                f'''Given the following description of an online meme related to LGBTQ+ pride movement,''',
                '''classify the content as either hateful or non-hateful towards LGBTQ+ community based on common values and knowledge, social norms and the provided guidelines.''',
                f'''Guidelines: {KNOWLEDGE}''',#some tips
                f'''**Meme content you need to classify**: {from_dependency}''',
                # f'''The caption overlaid on the image reads "{from_raw_data}".''',
                '''Now, let's analyze by applying the guidelines one by one:'''
            ]
        },
        'CoTwContext1': {
            'gen_depend_on': [INTEGRATE['name']],
            'INS': [
                f'''Given the following description of an online meme related to LGBTQ+ pride movement,''',
                '''classify the content as either harmful or harmless to the public image of LGBTQ+ community based on common values and knowledge, social norms and the provided guidelines.''',
                # '''classify the content as either harmful or harmless to LGBTQ+ community based on common values, knowledge, social norms and the provided guidelines.''',
                f'''Guidelines: {KNOWLEDGE}''',#some tips
                f'''**Meme content you need to classify**: {from_dependency}''',
                # f'''The caption overlaid on the image reads "{from_raw_data}".''',
                '''Now, let's analyze by applying the guidelines one by one:'''
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
        'Target_LGBT': {
            'gen_depend_on': [INTEGRATE['name']],
            'INS': [
                f'''Given the following description of an online meme related to LGBTQ+ pride movement,''',
                '''analyze: which specific group(s) within the LGBTQ+ community are explicitly mentioned in the meme content?''',
                '''Here are some guidelines for your reference:''',
                '''A. If the content does not seem to involve any specific LGBTQ+ subgroups but instead refers to the LGBTQ+ community as a whole, just output "No specific subgroup mentioned."''',
                '''B. Otherwise, choose your answer(s) from the provided list (you may choose multiple options if there are more than one subgroup being mentioned):''',
                '''1. Gay; 2. Transgender; 3. (Semi-) Bisexual; 4. Other LGBTQ+ subgroups not listed.''',
                f'''**Meme content you need to analyze**: {from_dependency}''',
                '''Now, let's analyze step by step:'''
            ]
        },
        'Target_Entity': {
            'gen_depend_on': [INTEGRATE['name']],
            'INS': [
                f'''Given the following description of an online meme related to LGBTQ+ pride movement,''',
                '''analyze: what social or cultural entities are explicitly mentioned in the meme content?''',
                '''Here are some guidelines for your reference:''',
                '''A. If the content does not seem to explicitly mention any specific sociocultural entities, just output "No specific sociocultural entity mentioned."''',
                '''B. Otherwise, choose your answer(s) from the provided list (you may choose multiple options if there are more than one entity mentioned):''',
                '''1. Women (Female); 2. Children (Kids); 3. Corporations; 4. Streaming media platforms; 5. Goverment; 6. Political ideologies or parties; 7. Religions; 8. Countries or regions; 9. Celebrities. 10. Other sociocultural entities not listed.''',
                f'''**Meme content you need to analyze**: {from_dependency}''',
                '''Now, let's analyze step by step:'''
            ]
        },
        'Target': {
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

EXTRACT = {
    'name': "Extract", 'should_evaluate': False,'take_image': False, 'gen_depend_on': None,
    'versions': {
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
        'Target': {
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
    },
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
            'INS': f'''If you just classified the meme content as hateful towards LGBTQ+ community, output "Conclusion: Hateful." Otherwise, output "Conclusion: Non-hateful."''',
        },
        'v1': {
            'gen_depend_on': None,
            'INS': f'''If you just classified the meme content as harmful towards the public image of LGBTQ+ community, output "Conclusion: Harmful." Otherwise, output "Conclusion: Harmless."''',
            # 'INS': f'''If you just classified the meme content as harmful towards LGBTQ+ community, output "Conclusion: Harmful." Otherwise, output "Conclusion: Harmless."''',
        },
        'v2': {
            'gen_depend_on': None,
            'INS': f'''If you just classified the meme content as offensive towards the LGBTQ+ community, output "Conclusion: Offensive." Otherwise, output "Conclusion: Non-offensive."''',
        }
    },
    'output_format': {
        'v0': {"INS": '''''', 'post_process_func': extract_classification_label},
    }
}


M2T = {
    'lmm': {'prompt': {
                    0: {'template': HUMAN, "version": "v0", "out_format": 'v0'}, 
                    1: {'template': RACE, "version": "v0", "out_format": 'v0'},
                    2: {'template': GENDER, "version": "v0", "out_format": 'v0'},
                    3: {'template': APPEARANCE, "version": "v0", "out_format": 'v0'},
                    #4: {'template': CELEB, "version": "v0", "out_format": 'v0'},
                    4: {'template': DESCRIBE, "version": "v0", "out_format": 'v0'},
            },
            'multi-turn': False},
    'llm_1': {'prompt': {
                    0: {'template': INTEGRATE, "version": "v0", "out_format": 'v0'},    
            },
            'multi-turn': False},
}

# ******************************************************************************************* # 
d6 = {
    'llm_2': {
        'multi-turn': True,
        'prompt': {
            0: {'template': REASONING, "version": "Target_LGBT", "out_format": 'v0'},
            1: {'template': EXTRACT, "version": "Target_LGBT", "out_format": 'lgbt'},
            2: {'template': REASONING, "version": "Target_Entity", "out_format": 'v0', 'new_conversation': True, 'depend_on_prestep': True},
            3: {'template': EXTRACT, "version": "Target_Entity", "out_format": 'entity'},
            # 4: {'template': REASONING, "version": "Interpret", "out_format": 'v0', 'new_conversation': True, 'depend_on_prestep': True, 'max_new_tokens': 256},
            4: {'template': REASONING, "version": "CoTwTGC", "out_format": 'v0', 'new_conversation': True, 'depend_on_prestep': True},
            5: {'template': DECISION, "version": "v1", "out_format": 'v0'}
            
            # 0: {'template': REASONING, "version": "CoTwContext1", "out_format": 'v0'},
            # 1: {'template': DECISION, "version": "v1", "out_format": 'v0'}
        }
    }
}

D6 = dict(**M2T, **d6)

# ******************************************************************************************* # 

PrideMM_PROMPT_SCHEMES = {
    'M2T': M2T,
    'D6': D6,
}

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

def prompt_pridemm(args, model_tag, js):
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