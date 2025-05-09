import os
import time

gpu_ids = "2,3"
which_gpus = f"export CUDA_VISIBLE_DEVICES={gpu_ids}"
port = '1234' if gpu_ids == '0,1' else '1235'
occupy = "python ./testG/train.py -p 0.8 -n 2 -t 604800"
#                --target_result_surfix {"_updated"} \
# do not use --use_dataset_cache when testing different prompts
#                 --use_mask_img \

#'llava1.6-7bf', 'llava1.6-8bf', 'llama3.2-11bf', 'qwen2-vl-7bf', 'llava1.6-8bf', 'llava1.6-13bf'

for split in ['dev']:#'dev', 'test'
    for seed in [42]:
        for batch_size in [32]:
            for llm in ['qwen2.5-14bf']: #'llama3.1-8bf', 'qwen2.5-7bf', 'qwen2.5-14bf'
                for lmm in ['llava1.6-7bf']: #'llava1.6-7bf', 'qwen2-vl-7bf'
                    for scheme in ['D6']:#[f"D{n}" for n in range(6)]
                        print(f"scheme={scheme}")
                        load_data_surfix = "-"
                        try:
                            run_cmd = f'''torchrun --nproc_per_node 2 --master_port {port} run.py \
                            --split {split} \
                            --load_data_surfix {load_data_surfix} \
                            --llm_max_new_tokens 1024 \
                            --lmm_max_new_tokens 256 \
                            --seed {seed} \
                            --scheme {scheme}\
                            --llm {llm} \
                            --lmm {lmm} \
                            --per_device_eval_batch_size {batch_size} \
                            --which_task=harmp \
                            --cfg config.cfg \
                            --report_to none \
                            --output_dir=./results \
                            --overwrite_output_dir \
                            --do_predict \
                            --remove_unused_columns False
                            '''
                            with open ('./sh_cmd/run_.sh', 'w') as rsh:
                                rsh.writelines([which_gpus, "\n", run_cmd]) #, 
                                rsh.close()
                            os.system("sh sh_cmd/run_.sh")
                        except:
                            continue

# time.sleep(10)
# with open ('./sh_cmd/run01.sh', 'w') as rsh:
#     rsh.writelines([which_gpus, "\n", occupy]) #, 
#     rsh.close()
# os.system("sh sh_cmd/run01.sh")

with open ('./sh_cmd/run23.sh', 'w') as rsh:
    rsh.writelines([which_gpus, "\n", occupy]) #, 
    rsh.close()
os.system("sh sh_cmd/run23.sh")