import kagglehub
from huggingface_hub import hf_hub_download
from pathlib import Path
import os
# Download latest version
# path = kagglehub.dataset_download("williamberrios/hateful-memes")
# print("Path to dataset files:", path)



# # Download latest version
# path = kagglehub.dataset_download("deeptanshu111/hateful-memes")
# print("Path to dataset files:", path)




# # Download latest version
# path = kagglehub.dataset_download("goldenlock/hateful-memes")
# print("Path to dataset files:", path)


# # Download latest version
# path = kagglehub.dataset_download("chauri/facebook-hateful-memes")
# print("Path to dataset files:", path)



# # Download latest version
# path = kagglehub.dataset_download("icarus96/facebookhatefuldataset-withouttextcaptions")
# print("Path to dataset files:", path)

# # Download latest version
# path = kagglehub.dataset_download("chukwuebukaanulunko/multimodal-misogyny-detection-mami-2022")

# print("Path to dataset files:", path)

pths = ["./GoatBench/test"]
rid = ["HKBU-NLP/GOAT-Bench"]
# ignore_patterns=["*.bin"]

for data_dir, repo in zip(pths,rid):
    os.makedirs(data_dir, exist_ok=True)
    hf_hub_download(repo_id=repo, subfolder='test', filename="misogyny.zip", repo_type="dataset", local_dir=data_dir)