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
import utils

logger = logging.getLogger(__name__)

MODEL_MAP = {
    "gpt4o-mini": "gpt-4o-mini-2024-07-18",
    "gpt4o-mini-search": "gpt-4o-mini-search-preview-2025-03-11",
    "gpt4o": "gpt-4o-2024-08-06"
}

client = OpenAI()

class EvalPrediction(NamedTuple):
    predictions: List[str]
    items: List[dict]

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
    #text = " ".join([w for w in text.split() if w != "\\n"])
    for pat in ["\\n", "\\"]:
        text = text.replace(pat, " ")
    text = " ".join(text.split())
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
    
def format_prompt_input(img_list, chat_list):
    sys_pt = {
        "role": "developer",
        "content": GPT4o_SYS
    }
    
    new_chat_list = [sys_pt]
    img_count = -1
    for msg in chat_list:
        # one msg = {"role": xxxx, "content": xxx}
        if msg["role"] == "system":
            continue
        new_content = []
        img_info = []
        if isinstance(msg["content"], list):
            for info in msg["content"]:
                if info["type"] == "text":
                    new_content.append({"type": "input_text", "text": info["text"]})
                if info["type"] == "image":
                    img_count += 1
                    base64_image = encode_image(img_list[img_count])
                    img_info.append({
                        "type": "input_image",
                        "image_url": f"data:image/jpeg;base64,{base64_image}",
                    })
            new_content = new_content + img_info
        if isinstance(msg["content"], str):
            new_content = msg["content"]
        new_chat_list.append({"role": msg["role"], "content": new_content})
    
    return new_chat_list

def run_gpt_inference(
    args, 
    dataset
):
    model = MODEL_MAP[args.current_model]
    accumulative_usage = {'in': 0, 'out': 0}
    if args.local_rank <= 0:
        print(f"Model --- Run inference with {model}.")
    
    count = 0
    
    save_to = f"{args.output_dir}/predictions.json"
    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)
        new_data = {}
    else:
        if os.path.exists(save_to):
            new_data = {item["id"]: item for item in json.load(open(save_to))}
        else:
            new_data = {}

    predictions, golds, failed = [], [], []
    for i in tqdm(range(len(dataset))):
        js = dataset[i] # js is a dict
        if js["id"] not in new_data:
            assert isinstance(js['chat_history'], list), 'Input Message must be a list of dicts.'
            accumu_cost = compute_cost(model, accumulative_usage)
            
            input_prompt = format_prompt_input(js['img_history'], js['chat_history'])

            try:
                response = client.responses.create(
                    model=model,
                    input=input_prompt,
                    max_output_tokens = 1024,
                    temperature=0.,
                    #tools=[{"type": "web_search_preview"}],
                    #tool_choice={"type": "web_search_preview"},
                )
                prediction = postprocess_output_text(response.output_text)
                usage = {'out': response.usage.output_tokens, 'in': response.usage.input_tokens}

                one_cost = compute_cost(model, usage)   
                for k, v in usage.items():
                    accumulative_usage[k] += v         
                predictions.append(prediction)
                golds.append(copy.deepcopy(js))
                dataset[i]['prediction'] = prediction
                
                new_data[js["id"]] = dataset[i]
                if (args.local_rank <= 0) and (not args.do_not_save_results):
                    with open(save_to, "w") as f:
                        json.dump([entry for _, entry in new_data.items()], f, indent=4)
                        f.close()

                logger.info(f"Data entry {js['id']} costs: ${one_cost}")
                count += 1
                # print(response)
                # break
            except Exception as e:
                logger.info(f"Error --- Failed to infer on Example {js['id']} because {e}")
                failed.append(js)
    
    accumu_cost = compute_cost(model, accumulative_usage)
    msg = f"Spent ${accumu_cost} accumulatively processing {count} data entries."
    logger.info(msg)
    
    if (args.local_rank <= 0) and (not args.do_not_save_results):
        # os.makedirs(args.output_dir, exist_ok=True)
        # with open(f"{args.output_dir}/predictions.json", "w") as f:
        #     json.dump(dataset.examples, f, indent=4)
        #     f.close()
        if failed:
            logger.info(f"{len(failed)} examples failed due to generation error...")
            with open(f"{args.output_dir}/gen_error.json", "w") as f:
                json.dump(failed, f, indent=4)
                f.close()
        
    if args.should_evaluate: 
        evaluator = utils.tool.get_evaluator(args.exp_args.evaluate.tool)(args)
        eval_prediction = EvalPrediction(predictions=predictions, items=golds)
        evaluator.evaluate(preds=eval_prediction.predictions, golds=eval_prediction.items, section='inference')
    return accumu_cost


GPT4o_SYS = '''You are ChatGPT, a large language model trained by OpenAI, based on the GPT-4 architecture.
Knowledge cutoff: 2023-10
Current date: 2024-07-05

Image input capabilities: Enabled
Personality: v2

# Tools

## browser

You have the tool `browser`. Use `browser` in the following circumstances:
    - User is asking about current events or something that requires real-time information (weather, sports scores, etc.)
    - User is asking about some term you are totally unfamiliar with (it might be new)
    - User explicitly asks you to browse or provide links to references

Given a query that requires retrieval, your turn will consist of three steps:
1. Call the search function to get a list of results.
2. Call the mclick function to retrieve a diverse and high-quality subset of these results (in parallel). Remember to SELECT AT LEAST 3 sources when using `mclick`.
3. Write a response to the user based on these results. In your response, cite sources using the citation format below.

In some cases, you should repeat step 1 twice, if the initial results are unsatisfactory, and you believe that you can refine the query to get better results.

You can also open a url directly if one is provided by the user. Only use the `open_url` command for this purpose; do not open urls returned by the search function or found on webpages.

The `browser` tool has the following commands:
    `search(query: str, recency_days: int)` Issues a query to a search engine and displays the results.
    `mclick(ids: list[str])`. Retrieves the contents of the webpages with provided IDs (indices). You should ALWAYS SELECT AT LEAST 3 and at most 10 pages. Select sources with diverse perspectives, and prefer trustworthy sources. Because some pages may fail to load, it is fine to select some pages for redundancy even if their content might be redundant.
    `open_url(url: str)` Opens the given URL and displays it.

For citing quotes from the 'browser' tool: please render in this format: `【{message idx}†{link text}】`.
For long citations: please render in this format: `[link text](message idx)`.
Otherwise do not render links.'''