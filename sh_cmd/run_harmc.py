import os
import time

gpu_ids = "2,3"
WHICH_GPUs = f"export CUDA_VISIBLE_DEVICES={gpu_ids}"
port = '1234' if gpu_ids == '0,1' else '1235'
occupy = "python ./testG/train.py -p 0.9 -n 2 -t 604800"
N_PROCESSES = len(gpu_ids.split(","))
#                --target_result_surfix {"_updated"} \
# do not use --use_dataset_cache when testing different prompts
#                 --use_mask_img \

#'llava1.6-7bf', 'llava1.6-8bf', 'llama3.2-11bf', 'qwen2-vl-7bf', 'llava1.6-8bf', 'llava1.6-13bf', 'llama3.1-8bf', 'qwen2.5-7bf', 'qwen2.5-14bf'
LLM_max_new_tokens = 1024
LMM_max_new_tokens = 256
for task in ['harmc']:
    for split in ['test']:
        for seed in [42]:#, 0, 123, 2025, 27
            for batch_size in [32]:
                for llm in ['qwen2.5-14bf']:
                    for lmm in ['llava1.6-7bf']:
                        for scheme in ['PP']:
                            print(f"scheme={scheme}")
                            llm_max_new_tokens = LLM_max_new_tokens
                            lmm_max_new_tokens = LMM_max_new_tokens
                            load_data_surfix = "-"
                            if (task == 'fhm') and (split == 'test'):
                                load_data_surfix = 'seen'
                                #lmm_max_new_tokens = 256
                            try:
                                run_cmd = f'''torchrun --nproc_per_node {N_PROCESSES} --master_port {port} run.py \
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
                                with open ('./sh_cmd/run_.sh', 'w') as rsh:
                                    rsh.writelines([WHICH_GPUs, "\n", run_cmd]) #, 
                                    rsh.close()
                                os.system("sh sh_cmd/run_.sh")
                            except:
                                continue

with open ('./sh_cmd/run23.sh', 'w') as rsh:
    rsh.writelines([WHICH_GPUs, "\n", occupy]) #, 
    rsh.close()
os.system("sh sh_cmd/run23.sh")