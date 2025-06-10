import os
import time

gpu_ids = "0,1"
WHICH_GPUs = f"export CUDA_VISIBLE_DEVICES={gpu_ids}"
port = '1234' if gpu_ids == '0,1' else '1235'
N_PROCESSES = 2

DEFAULT_LLM_max_new_tokens = 1024
DEFAULT_LMM_max_new_tokens = 256

B1 = {'lmm': 512, 'llm': DEFAULT_LLM_max_new_tokens}
B2 = {'lmm': 256, 'llm': 1024}
task_scheme_max_new_tokens_map = {
    'fhm' : {
        'B1': B1,
        'B2': B2,
        'PP': B2,
        'PL': B2,
    },
    'gb_hateful' : {
        'B2': B2,
        'PP': B2,
    },
    'harmc' : {
        'B1': B1,
        'B2': B2,
        'PP': B2,
        'PD': B2,
        'PL': B2,
    },
    'harmp' : {
        'B1': B1,
        'B2': {'lmm': 356, 'llm': 1024},
        'PP': {'lmm': 356, 'llm': 1024},
        'PD': {'lmm': 356, 'llm': 1024},
        'P2': {'lmm': 356, 'llm': 1024},
    },
    'gb_harmful' : {
        'B1': B1,
        'B2': B2,
        'PP': B2,
    },
    'mami' : {
        'B1': B1,
        'B2': B2,
        'PP': B2,
        'PL': B2,
    },
    'gb_misogynistic' : {
        'B1': B1,
        'B2': B2,
        'PP': B2
    },
    'multioff' : {
        'B1': B1,
        'B2': {'lmm': 512, 'llm': 1024},
        'PP': {'lmm': 512, 'llm': 1024},
        'P4': {'lmm': 512, 'llm': 1024},
        'P5': {'lmm': 512, 'llm': 1024},
        'P41': {'lmm': 512, 'llm': 1024},
    },
    'gb_offensive' : {
        'B1': B1,
        'B2': {'lmm': 512, 'llm': 1024},
        'PP': {'lmm': 512, 'llm': 1024},
        'P4': {'lmm': 512, 'llm': 1024},
        'P5': {'lmm': 512, 'llm': 1024},
        'P41': {'lmm': 512, 'llm': 1024},
    },
    'pridemm' : {
        'B1': B1,
        'B2': {'lmm': 512, 'llm': 1024},
        'PP': {'lmm': 512, 'llm': 1024},
    },
}


for task in ['fhm', 'harmc', 'harmp', 'multioff', 'pridemm', 'mami', 'gb_hateful', 'gb_harmful', 'gb_misogynistic', 'gb_offensive']:
    for split in ['test']:
        for seed in [42]:
            for batch_size in [16]:
                for llm in ['qwen2.5-14bf', 'mistral-12bf', 'qwen2.5-7bf', 'llama3.1-8bf']:
                    for lmm in ['llava1.6-7bf', 'qwen2-vl-7bf', 'llava1.6-7bf,qwen2-vl-7bf']:
                        if (lmm ==  'llava1.6-7bf,qwen2-vl-7bf') and (task not in ['fhm', 'gb_hateful']):
                            continue
                        else:
                            for scheme in ['B1', 'B2', 'PP', 'PL']:
                                print(f"scheme={scheme}")
                                llm_max_new_tokens = task_scheme_max_new_tokens_map[task][scheme]['llm']
                                lmm_max_new_tokens = task_scheme_max_new_tokens_map[task][scheme]['lmm']
                                load_data_surfix = "-"
                                if (task == 'fhm') and (split == 'test'):
                                    load_data_surfix = 'seen'
                                
                                try:
                                    run_cmd = f'''torchrun --nproc_per_node {N_PROCESSES} --master_port {port} run.py \
                                    --use_greedy_decoding_for_mini_models \
                                    --use_resized_img \
                                    --split {split} \
                                    --load_data_surfix {load_data_surfix} \
                                    --llm_max_new_tokens {llm_max_new_tokens} \
                                    --lmm_max_new_tokens {lmm_max_new_tokens} \
                                    --seed {seed} \
                                    --scheme {scheme}\
                                    --llm {llm} \
                                    --lmm {lmm} \
                                    --per_device_eval_batch_size {batch_size} \
                                    --which_task={task} \
                                    --cfg config.cfg \
                                    --report_to none \
                                    --output_dir=./results \
                                    --overwrite_output_dir \
                                    --do_predict \
                                    --remove_unused_columns False
                                    '''
                                    with open ('./run_cmd/run.sh', 'w') as rsh:
                                        rsh.writelines([WHICH_GPUs, "\n", run_cmd])
                                        rsh.close()
                                    os.system("sh run_cmd/run.sh")
                                except:
                                    continue