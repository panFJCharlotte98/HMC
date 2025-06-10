import os
import time

gpu_ids = "0,1"
WHICH_GPUs = f"export CUDA_VISIBLE_DEVICES={gpu_ids}"
port = '1235' if gpu_ids == '0,1' else '1236'
N_PROCESSES = 2

for task in ['fhm', 'harmc', 'harmp', 'multioff', 'pridemm', 'mami']:
    for split in ['test']:
        for seed in [42]:
            for batch_size in [1]:
                for llm in ['qwen2.5-14bf']: 
                    for lmm in ['gpt4o-mini']:
                        for scheme in ["GPT"]:
                            print(f"scheme={scheme}")
                            load_data_surfix = "-"
                            if (task == 'fhm') and (split == 'test'):
                                load_data_surfix = 'seen'
                            which_gpus = WHICH_GPUs
                            n_proc = N_PROCESSES
                            try:
                                run_cmd = f'''torchrun --nproc_per_node {n_proc} --master_port {port} run.py \
                                --use_resized_img \
                                --split {split} \
                                --load_data_surfix {load_data_surfix} \
                                --llm_max_new_tokens 1536 \
                                --lmm_max_new_tokens 256 \
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
                                    rsh.writelines([which_gpus, "\n", run_cmd])
                                    rsh.close()
                                os.system("sh run_cmd/run.sh")
                            except:
                                continue