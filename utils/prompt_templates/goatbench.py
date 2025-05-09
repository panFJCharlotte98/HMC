
from utils.prompt_templates.fhm import FHM_PROMPT_SCHEMES, prompt_fhm
from utils.prompt_templates.harmc import HARMC_PROMPT_SCHEMES, prompt_harmc
from utils.prompt_templates.harmc import assign_guidelines_ as harmc_assign_guidelines
from utils.prompt_templates.harmp import assign_guidelines_ as harmp_assign_guidelines
from utils.prompt_templates.harmp import HARMP_PROMPT_SCHEMES, prompt_harmp
from utils.prompt_templates.mami import MAMI_PROMPT_SCHEMES, prompt_mami
from utils.prompt_templates.multioff import MultiOFF_PROMPT_SCHEMES, prompt_multioff
from utils.prompt_templates.pridemm import PrideMM_PROMPT_SCHEMES, prompt_pridemm
from utils.tool import *

#--------------------------------Harmful------------------------------------#
from_raw_data = '{from_raw_data}'
from_dependency = '{from_dependency}'
check_harmc = '''{check_harmc}'''
check_harmp = '''{check_harmp}'''
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
CELEB = {
    'name': "Celeb", 'should_evaluate': False, 'take_image': True, 'gen_depend_on': None,
    'versions': {
        'trump': {"INS" : f'''{check_harmc}Is {cname_map['trump']} in the image?'''},
        'politician': {"INS": f'''{check_harmc}Does this image feature any politican of the United States? If yes, who are they?'''},
        'cleaders': {"INS": f'''{check_harmc}Does this image feature any head of state? If yes, who are they?'''},
        'celeb': {"INS": f'''{check_harmp}Is any politician or celebrity portrayed in the image? If yes, who?'''},
        'pleaders': {"INS": f'''{check_harmp}Is any head of state portrayed in the image?'''},
    },
    'output_format': {
        'v0': {"INS": '''Start your response with "Yes," or "No," before giving further explanation.''', 'post_process_func': extract_yes_or_no},
    }
}
DESCRIBE = {
    'name': "Describe", 'should_evaluate': False,'take_image': True,'gen_depend_on': None,
    'versions': {
        'vp': {"INS" : f'''{check_harmp}What is shown in this meme?'''},
        'vc': {"INS" : f'''{check_harmc}What is shown in this meme?'''},
    },
    'output_format': {
        'vp': {"INS": "", 'post_process_func': post_process_description},
        'vc': {"INS": "", 'post_process_func': post_process_to_remove_gibberish},
    }
}
assign_trump_prompt_by_task = '''{assign_trump_prompt_by_task}'''
AUX = {
    'name': "Aux", 'should_evaluate': False, 'take_image': True, 'gen_depend_on': None,
    'versions': {
        'trump': {"INS" : f'''{assign_trump_prompt_by_task}'''},
        'biden': {"INS" : f'''Is {cname_map['biden']} depicted in the image?'''},
        'obama': {"INS" : f'''Is {cname_map['obama']} depicted in the image?'''},
        'hillary': {"INS" : f'''Is {cname_map['hillary']} depicted in the image?'''},
        'b&o': {"INS" : f'''Does this image feature {cname_map['biden']} and {cname_map['obama']}?'''},
        'party': {"INS" : f'''{check_harmp}Is any political party explicitly involved in this image?'''},
    },
    'output_format': {
        'v0': {"INS": '''Start your response with "Yes," or "No," before giving the explanation.''', 'post_process_func': extract_yes_or_no},
    }
}
UNIFY_SYS = '''You are a helpful assistant.'''
from_data_text = "{from_data_text}"
INTEGRATE_P = {
    'name': "Integrate", 'should_evaluate': False, 'take_image': False, 'gen_depend_on': [AUX['name'], CELEB['name'], DESCRIBE['name']], 
    'versions': {
        'v0': {
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
INTEGRATE_C = {
    'name': "Integrate", 'should_evaluate': False, 'take_image': False, 'gen_depend_on': [CELEB['name'], DESCRIBE['name']],
    'versions': {
        'v0': {
            "INS": [
                f'''Given the following information provided about an online meme, synthesize and rephrase these information into a coherent, unified, and neutral description of the meme's content, **Information**: {from_dependency}''',
                f'''{from_data_text}'''
            ]
        },
    },
    'output_format': {
        'v0': {"INS": '''''', 'post_process_func': post_process_to_remove_gibberish},
    }
}
assign_guidelines_harmp = "{assign_guidelines_harmp}"
assign_guidelines_harmc = "{assign_guidelines_harmc}"
REASONING = {
    'name': "Reasoning", 'should_evaluate': False, 'take_image': False,
    'versions': {
        'pCoT+': {
            'gen_depend_on': [INTEGRATE_P['name']],
            'INS': [
                f'''Given the following description of an image related to U.S. politics,''',
                '''classify the image content as either harmful or harmless based on common values, knowledge, social norms and the provided guidelines.''',
                f'''**Guidelines**: {assign_guidelines_harmp}''',
                f'''**Description of the image**: {from_dependency}''',
                '''Now, let's analyze by applying the guidelines one by one:'''
            ]
        },
        'cCoT+': {
            'gen_depend_on': [INTEGRATE_C['name']],
            'INS': [
                f'''Given the following description of an online meme related to COVID-19 pandemic,''',
                '''classify the meme content as either harmful or harmless based on widely accepted values, established knowledge and social norms.''',
                f'''**Here are some guidelines for your reference**: {assign_guidelines_harmc}''',
                f'''**Meme content you need to classify**: {from_dependency}''',
                #'''Now, let's analyze by applying the guidelines one by one:''',
                '''Now, let's think step by step:'''
            ]
        },
    },
    'output_format': {
        'v0': {"INS": '''''', 'post_process_func': post_process_to_remove_gibberish},
    }
}
assign_decision_prompt = '''{assign_decision_prompt}'''
DECISION = {
    'name': "Decision", 'should_evaluate': True, 'take_image': False,
    'versions': {
        'v0': {
            'gen_depend_on': [REASONING['name']],
            'INS': f'''{assign_decision_prompt}''',
        },
    },
    'output_format': {
        'v0': {"INS": '''''', 'post_process_func': harmc_extract_classification_label},
    }
}
M2T = {
    'lmm_1': {
        'prompt': {
            # Harm-P
            0: {'template': CELEB, "version": "celeb", "out_format": 'v0'},
            1: {'template': CELEB, "version": "pleaders", "out_format": 'v0'},
            2: {'template': DESCRIBE, "version": "vp", "out_format": 'vp'},
            # Harm-C
            3: {'template': CELEB, "version": "politician", "out_format": 'v0'},
            4: {'template': CELEB, "version": "cleaders", "out_format": 'v0'},
            5: {'template': CELEB, "version": "trump", "out_format": 'v0'},
            6: {'template': DESCRIBE, "version": "vc", "out_format": 'vc'},
        },
        'multi-turn': False},
    'lmm_2': {
        'prompt': {
            0: {'template': AUX, "version": "trump", "out_format": 'v0'},
            1: {'template': AUX, "version": "biden", "out_format": 'v0', "load_from_prestep": True},
            2: {'template': AUX, "version": "obama", "out_format": 'v0', "load_from_prestep": True},
            3: {'template': AUX, "version": "b&o", "out_format": 'v0', "load_from_prestep": True},
            4: {'template': AUX, "version": "hillary", "out_format": 'v0', "load_from_prestep": True},
            5: {'template': AUX, "version": "party", "out_format": 'v0', "load_from_prestep": True},
        },
        'multi-turn': False},
    'llm_1': {
        'prompt': {
            0: {'template': INTEGRATE_P, "version": "v0", "out_format": 'v0', "load_from_prestep": True, "return_prestep_path": False},
            1: {'template': INTEGRATE_C, "version": "v0", "out_format": 'v0', "load_from": {'m_type': 'lmm_2', 'rid': 4}, "return_load_from_path": False},
        },
        'multi-turn': False
    },
}
p1 = {
    'llm_2': {
        'multi-turn': True,
        'prompt': {
            0: {'template': REASONING, "version": "pCoT+", "out_format": 'v0', 'max_new_tokens': 1536},
            1: {'template': REASONING, "version": "cCoT+", "out_format": 'v0', 'new_conversation': True},
            2: {'template': DECISION, "version": "v0", "out_format": 'v0'},
        }
    }
}
PP = dict(**M2T, **p1)
GBHARMFUL_PROMPT_SCHEMES = {
    'M2T': M2T,
    'PP': PP,
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
    if check_harmc in tmp:
        if js['task'] == "harmc":
            return tmp.replace(check_harmc, ""), js
        else:
            return "", None
    if check_harmp in tmp:
        if js['task'] == "harmp":
            return tmp.replace(check_harmp, ""), js
        else:
            return "", None
    if assign_trump_prompt_by_task in tmp:
        if js['task'] == "harmp":
            trump_ins = f'''Is {cname_map['trump']} depicted in the image?'''
        if js['task'] == "harmc":
            trump_ins = f'''Is {cname_map['trump']} in the image?'''
        return tmp.format(assign_trump_prompt_by_task = trump_ins), js
    if assign_guidelines_harmc in tmp:
        assert "aux_info" in js
        return tmp.format(assign_guidelines_harmc = harmc_assign_guidelines(js)), js
    if assign_guidelines_harmp in tmp:
        assert "aux_info" in js
        return tmp.format(assign_guidelines_harmp = harmp_assign_guidelines(js)), js
    if assign_decision_prompt in tmp:
        if js['task'] == 'harmp':
            decision_ins = '''If you just classified the image content as harmful, output "Conclusion: Harmful." Otherwise, output "Conclusion: Harmless."'''
        if js['task'] == 'harmc':
            decision_ins = '''If you just classified the meme content as harmful, output "Conclusion: Harmful." Otherwise, output "Conclusion: Harmless."'''
        return tmp.format(assign_decision_prompt = decision_ins), js
    if from_data_text in tmp:
        if js['text']:
            prompt = f'''Also, some overlaid text in the image is recognized as: "{js['text']}"'''
        else:
            prompt = ""
        return tmp.format(from_data_text = prompt), js
    return tmp, js

def prompt_gb_harmful(args, js):
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

def format_chat(args, model_tag, js):
    if args.task == "gb_hateful":
        return prompt_fhm(args, model_tag, js)
    elif args.task == "gb_offensive":
        return prompt_multioff(args, model_tag, js)
    elif args.task == "gb_misogynistic":
        return prompt_mami(args, model_tag, js)
    elif args.task == "gb_harmful":
        return prompt_gb_harmful(args, js)

GOATBENCH_PROMPT_SCHEMES = {
    "hateful": FHM_PROMPT_SCHEMES,
    "offensive": MultiOFF_PROMPT_SCHEMES,
    "misogynistic": MAMI_PROMPT_SCHEMES,
    "harmful": GBHARMFUL_PROMPT_SCHEMES,
}

def prompt_goatbench(args, model_tag, js):
    """
    input:
        js is one data sample in the format of dictionary
        js['text'] is a string
    """
    js = format_chat(args, model_tag, js)
    return js