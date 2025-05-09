import base64
import copy
import json
import os
import regex
from openai import OpenAI
from IPython.display import Image as IPythonImage
from IPython.display import display
from PIL import Image
from tqdm import tqdm
import statistics
from typing import List, NamedTuple
import logging

logger = logging.getLogger(__name__)

for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)
log_file = './call_gpt_gen_captions.log'
logging.basicConfig(
    filename=log_file,
    filemode='a',
    format='%(asctime)s - %(levelname)s - %(name)s -   %(message)s',
    datefmt='%m/%d/%Y %H:%M:%S',
    level=logging.INFO
)

client = OpenAI()


main_ins = "What is going on in this image? Describe the content of the image without interpreting any underlying implications."
transcribe = "If there is any overlaid text, transcribe the text without paraphrasing."
marginal_info = "Ignore any watermarks, post timestamps, usernames, or engagement metrics of tweets or webpage posts."
transcribe_wo_marginal = "If there is any overlaid text, transcribe the text without paraphrasing, but ignore any watermarks, post timestamps, usernames, or any engagement metrics of tweets or webpage posts."
tone = "Do not assume the image's tone or intent to be humorous or lighthearted. Maintain a neutral and descriptive tone."

base_p = f"{main_ins} {transcribe} {marginal_info} {tone} Output your description in one paragraph."

mami_p = f'''{main_ins} Requirements: 1. {transcribe} 2. Identify the genders of any human subjects. 3. If the image intentionally portrays any female subjects in a sexually provocative manner—such as overtly revealing clothing, emphasis on nudity or specific sexual body parts, describe the relevant visual cues. 4. If the image contains any sexual innuendo, point out the related visual cues. 5. If the image features any overweight female subjects, point out the related visual cues. 6. {marginal_info} 7. {tone} 8. Output your description in one paragraph.'''

# What is going on in this image? Describe the content of the image without interpreting any underlying implications. Requirements: 1. If there is any overlaid text, transcribe the text without paraphrasing. 2. Identify the genders of any human subjects. 3. If the image intentionally portrays any female subjects in a sexually provocative manner—such as overtly revealing clothing, emphasis on nudity or specific sexual body parts, describe the relevant visual cues. 4. If the image contains any sexual innuendo, point out the related visual cues. 5. If the image features any overweight female subjects, point out the related visual cues. 6. Ignore any watermarks, post timestamps, usernames, or engagement metrics of tweets or webpage posts. 7. Do not assume the image's tone or intent to be humorous or lighthearted. Maintain a neutral and descriptive tone. 8. Output your description in one paragraph.

fhm_p = f'''{main_ins} {transcribe} If there are any human subjects, identify their perceived genders and races. If any human subject appears to be a celebrity or historical figure, identify them by name. If any human subject appears to have a disability, identify the visual cues that suggest it. {tone} Output your description in one short paragraph.'''

# harm_p = f'''{main_ins} {transcribe_wo_marginal} If there is any celebrity in the image, identify them by name. {tone} Output your description in one paragraph.'''
# harm_p = f'''{main_ins} {transcribe} If there is any celebrity in the image, identify them by name. {marginal_info} {tone} Output your description in one paragraph.'''
celeb_1  = "Identify any celebrities (e.g., politicians) in the image by their names."
celeb_2 = "If there are any celebrities featured in the image, don't forget to mention who they are."
harm_p = f'''{main_ins} {transcribe} {celeb_2} {tone} Output your description in one paragraph.'''
plh = "{plh}"
from_all_vers = "{from_all_vers}"
remove_timestamps = f'''Keep all tweet contents (if there are any) and other wording unchanged, and remove any information about watermarks, post timestamps, non-celebrity usernames, or social media engagement metrics from the given image description. If no such information is found, output the text exactly as it is. **Description**: {plh}'''
integrate = f'''Integrate the following two versions of an image description into one comprehensive, informative version. Remove any information about watermarks, post timestamps, non-celebrity usernames, or social media engagement metrics, but DO NOT alter the wording of any overlaid text or tweet contents (if there are any). Output the finalized description in one paragraph. {from_all_vers}'''
PROMPTS = {
    'PrideMM': base_p,
    'MultiOFF': base_p,
    'MAMI': mami_p,
    'FHM': {
        0: {'prompt': fhm_p, 'key': 'gt_caption', 'w_img': True}
    },
    'Harm-P': {
        0: {'prompt': harm_p, 'key': 'v2', 'w_img': True}, 
        1: {'prompt': integrate, 'key': 'gt_caption', 'w_img': False}
        },
    'Harm-C': {
        0: {'prompt': harm_p, 'key': 'raw_output', 'w_img': True}, 
        1: {'prompt': remove_timestamps, 'key': 'gt_caption', 'w_img': False}
        }
}

def postprocess_output_text(text):
    sub_map = {
        r"\\u2019": "'",
        r"\\u201c": "'",
        r"\\u201d": "'",
        r"\\'": "'",
        r"(?:(?:\\u[a-z0-9]{4}){1,}[\s\-\-\*0-9\.\']*){1,}": ""
    }
    text = ascii(text)
    for re, sub_str in sub_map.items():
        text = regex.sub(re, sub_str, text)
    text = text.strip("' ")
    text = " ".join([w for w in text.split() if w != "\\n"])
    return text


def compute_cost(model, usage):
    # pricing in dollars per 1M (1e6) tokens
    pricing = {
        # 'gpt-3.5-turbo': {'input': 0.5, 'output':1.5},
        # 'gpt-4-turbo':{'input': 10, 'output': 30},
        'gpt-4o-mini-2024-07-18': {'input': 0.15, 'output': 0.6}
    }
    for mt, price in pricing.items():
        if model.startswith(mt):
            return round((usage["in"] / 1e6) * price['input'] + (usage["out"] / 1e6) * price['output'], 3)

# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")
    
MIN_IMG_SIZE = {
    'Harm-C': 0.5,
    'Harm-P': 0.8
}

MIN_LENGTH = {
    'Harm-C': 768,
    'Harm-P': 768
}

def resize_image(
    image_path, 
    save_dir, 
    max_size_mb=None, 
    min_size_mb=None,
    min_len=512,
    max_len=5120
):
    """
    Compress image if it's larger than max_size_mb while maintaining quality
    
    Args:
        image_path (str): Path to input image
        max_size_mb (int): Maximum file size in MB
    Returns:
        str: Path to compressed image
    """
    # Open image
    img = Image.open(image_path)
    # Get original format
    original_format = img.format if img.format else 'JPEG'
    if max_size_mb and min_size_mb:
        # Get file size in MB
        file_size = os.path.getsize(image_path) / (1024 * 1024)
        ori_file_size = copy.deepcopy(file_size)

        if (file_size >= min_size_mb) and (file_size <= max_size_mb):
            return image_path
        if file_size > max_size_mb:
            op = "Compressed"
        elif file_size < min_size_mb:
            op = "Enlarged"
        output_name = image_path.split("/")[-1].split(".")[0] + f"_{op.lower()}." + original_format.lower()
        output_path = os.path.join(save_dir, output_name)
        
        if not os.path.exists(output_path):
            if file_size > max_size_mb:
                # Initial quality
                quality = 95
                while file_size > max_size_mb and quality > 5:
                    img.save(output_path, original_format, quality=quality)
                    file_size = os.path.getsize(output_path) / (1024 * 1024)
                    quality -= 5
            elif file_size < min_size_mb:
                # Enlarge image
                width, height = img.size
                scale_factor = 1.1  # Increase by 10% each iteration
                while file_size < min_size_mb:
                    new_width = int(width * scale_factor)
                    new_height = int(height * scale_factor)
                    img = img.resize((new_width, new_height), Image.LANCZOS)
                    img.save(output_path, original_format)
                    file_size = os.path.getsize(output_path) / (1024 * 1024)
                    width, height = new_width, new_height
        else:
            file_size = os.path.getsize(output_path) / (1024 * 1024)

        logger.info(f"{op} {image_path} from {ori_file_size}MB to {file_size}MB.")    
        return output_path
    
    if min_len:
        # Get image dimensions
        width, height = img.size
        long_edge = max(width, height)
        if (long_edge >= min_len) and (long_edge <= max_len):
            return image_path
        if long_edge < min_len:
            op = "Enlarged"
            target_len = min_len
        elif long_edge > max_len:
            op = "Compressed"
            target_len = max_len
        output_name = image_path.split("/")[-1].split(".")[0] + f"_{op.lower()}." + original_format.lower()
        output_path = os.path.join(save_dir, output_name)
        
        if not os.path.exists(output_path):
            assert target_len > 0
            # Calculate scale factor to reach target_long_edge
            scale_factor = target_len / long_edge
            # Calculate new dimensions while maintaining aspect ratio
            new_width = int(width * scale_factor)
            new_height = int(height * scale_factor)
            # Resize image
            img = img.resize((new_width, new_height), Image.LANCZOS)
            img.save(output_path, original_format)
        else:
            img = Image.open(output_path)
        resized_w, resized_h = img.size
        logger.info(f"{op} {image_path} from {height}x{width} to {resized_h}x{resized_w}.")    
        return output_path


def img2text(prompt, base64_image, model):
    if base64_image:
        response = client.responses.create(
            model=model,
            input=[
                {
                    "role": "user",
                    "content": [
                        { "type": "input_text", "text": prompt},
                        {
                            "type": "input_image",
                            "image_url": f"data:image/jpeg;base64,{base64_image}",
                            "detail": "high",
                        },
                    ],
                }
            ],
        )
    else:
        response = client.responses.create(
            model=model,
            input=prompt
        )
    
    output_text = postprocess_output_text(response.output_text)
    usage = {'out': response.usage.output_tokens, 'in': response.usage.input_tokens}

    one_cost = compute_cost(model, usage)
    return output_text, one_cost, usage

def caption_img_w_gpt(
    datasets, 
    splits, 
    model="gpt-4o-mini-2024-07-18",
    resize_img=False
):
    count = 0
    accumulative_usage = {'in': 0, 'out': 0}
    for dataset in datasets:
        logger.info(f"***Dataset: {dataset}***")
        ori_sizes, after_sizes = {}, {}
        for sp in splits:
            if (dataset == 'FHM') and (sp == 'test'):
                sp = sp + "_seen"
            #ori_sizes[sp], after_sizes[sp] = {}, {}
            ori_sizes[sp], after_sizes[sp] = {'w': {}, 'h': {}}, {'w': {}, 'h': {}}
            logger.info(f"***Split: {sp}***")
            if dataset.startswith("Harm-"):
                target_path = f"./data/HarMeme_V1/caption_annotations/{dataset}/{sp}.json"
                new_img_save_to = f"./data/HarMeme_V1/caption_annotations/{dataset}/{sp}"
            else:
                target_path = f"./data/{dataset}/caption_annotations/{sp}.json"
                new_img_save_to = f"./data/{dataset}/caption_annotations/{sp}"
            
            if resize_img and (not os.path.exists(new_img_save_to)):
                os.makedirs(new_img_save_to)
            if dataset == "MAMI":
                all_img_paths = {}
                for item in json.load(open(f"./data/{dataset}/data/{sp}.json")):
                    all_img_paths[item['id']] = item['img']
            
            res_dict = json.load(open(target_path))
            for id, item in tqdm(res_dict.items()):
                accumu_cost = compute_cost(model, accumulative_usage)
                if accumu_cost >= 5.:
                    logger.info(f"Spent ${accumu_cost} processing {count} images.")
                    break
                # check path validity
                if (dataset == "MAMI") and (not os.path.exists(item['img'])):
                    item['img'] = all_img_paths[id]
                    res_dict[id]['img'] = all_img_paths[id]

                # do_condition = (("gt_caption" in item) and (item["gt_caption"] == ""))
                # do_condition = True
                # if do_condition:
                # count += 1
                img = Image.open(item['img'])
                width, height = img.size
                ori_sizes[sp]['w'][id] = width
                ori_sizes[sp]['h'][id] = height
                
                resized_img_path = item['img']
                if resize_img:
                    #ori_sizes[sp][id] = os.path.getsize(item['img']) / (1024 * 1024)
                    resized_img_path = resize_image(
                        item['img'], 
                        new_img_save_to, 
                        #min_size_mb=MIN_IMG_SIZE[dataset],
                        min_len=MIN_LENGTH[dataset]
                    )
                    #after_sizes[sp][id] = os.path.getsize(resized_img_path) / (1024 * 1024)
                    img = Image.open(resized_img_path)
                    after_sizes[sp]['w'][id], after_sizes[sp]['h'][id] = img.size
                    
                p_plan = PROMPTS[dataset]
                for sid, step in p_plan.items():
                    prompt = step['prompt']
                    target_key = step['key']
                    if (target_key not in item) or ((target_key in item) and (item[target_key] == "")):
                        count += 1
                        if plh in prompt:
                            prompt = prompt.format(plh = item[p_plan[sid-1]['key']])
                        if from_all_vers in prompt:
                            prompt = prompt.format(from_all_vers = " ".join([f"**Version {vid+1}**: {ver}" for vid, ver in enumerate([v for k, v in item.items() if k.startswith("v")])]))
                        base64_image = None
                        if step['w_img']:
                            # Getting the Base64 string
                            base64_image = encode_image(resized_img_path)
                        try:
                            caption, this_cost, this_usage = img2text(prompt, base64_image, model)
                            for k, v in this_usage.items():
                                accumulative_usage[k] += v
                            logger.info(f"{sp} img {id} cost: ${this_cost}")
                            res_dict[id][target_key] = caption
                            json.dump(res_dict, open(target_path, 'w'), indent=4)
                        except Exception as e:
                            logger.info(f"Error!!! Failed on img {id} because {e}")
                    
            accumu_cost = compute_cost(model, accumulative_usage)
            msg = f"Spent ${accumu_cost} accumulatively processing {count} images after {dataset}:{sp} split."
            logger.info(msg) 
            print(msg)
            # Image size statistics
            tmp = {'before': ori_sizes, 'after': after_sizes}
            for k, sizes in tmp.items():
                width_values, height_values = list(sizes[sp]['w'].values()), list(sizes[sp]['h'].values())
                if width_values and height_values:
                    print(f"{dataset}: {sp}| #{count} images in total \n Width: min: {min(width_values)}, max: {max(width_values)}, mean: {statistics.mean(width_values)}, median: {statistics.median(width_values)} \n Height: min: {min(height_values)}, max: {max(height_values)}, mean: {statistics.mean(height_values)}, median: {statistics.median(height_values)}")

            # ori_size_values = list(ori_sizes[sp].values())
            # print(f"{dataset}: {sp}| #{count} images in total | min: {min(ori_size_values)}, max: {max(ori_size_values)}, mean: {statistics.mean(ori_size_values)}, median: {statistics.median(ori_size_values)}")
            # after_size_values = list(after_sizes[sp].values())
            # print(f"{dataset}: {sp}| #{count} images in total | min: {min(after_size_values)}, max: {max(after_size_values)}, mean: {statistics.mean(after_size_values)}")
    accumu_cost = compute_cost(model, accumulative_usage)
    msg = f"Spent ${accumu_cost} processing {count} images."
    logger.info(msg) 
    print(msg)

datasets = ["Harm-P", "Harm-C", "FHM"] #'Harm-P', 
splits = ['test']
caption_img_w_gpt(datasets, splits)



