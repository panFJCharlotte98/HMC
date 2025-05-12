import os
import torch
import numpy as np
from torch import nn
import json
import torch.distributed as dist
from transformers.trainer import Trainer
from arguments import WrappedTrainingArguments
from transformers.utils import logging
from transformers.modeling_utils import PreTrainedModel, unwrap_model
from transformers.trainer_utils import PredictionOutput, speed_metrics
from typing import Optional, Dict, Union, List, Tuple, Any, NamedTuple
from torch.utils.data import Dataset, DataLoader
from transformers.trainer_callback import TrainerState
import time
from utils.tool import extract_json_output
import math
import regex

skip_first_batches = None
# Name of the files used for checkpointing
TRAINING_ARGS_NAME = "training_args.bin"
TRAINER_STATE_NAME = "trainer_state.json"
OPTIMIZER_NAME = "optimizer.pt"
SCHEDULER_NAME = "scheduler.pt"
SCALER_NAME = "scaler.pt"
SAMPLER_WEIGHTS_NAME = "sampler_weights.pt"

logger = logging.get_logger(__name__)

# For Llama2
B_INST, E_INST = "[INST]", "[/INST]"
# For Llama3
END_OF_TURN, END_INST = "<|eot_id|>", "<|start_header_id|> assistant <|end_header_id|>"

class EvalPrediction(NamedTuple):
    predictions: List[str]
    items: List[dict]

class EvaluateFriendlyTrainer(Trainer):
    def __init__(
        self,
        evaluator,
        *args: WrappedTrainingArguments,
        ignore_pad_token_for_loss: bool = True,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.evaluator = evaluator
        self.compute_metrics = self._compute_metrics
        self.ignore_pad_token_for_loss = ignore_pad_token_for_loss
        self.mtask_args = None
        # if self.args.exp_args.model.model_tag.startswith("t5"):
        #     self.mtask_args = self.args.exp_args

    def evaluate(
        self,
        eval_dataset: Optional[Dataset] = None,
        ignore_keys: Optional[List[str]] = None,
        metric_key_prefix: str = "eval",
        max_time: Optional[int] = None,
    ) -> Dict[str, float]:
        self._max_length, self._num_beams  = None, None
        self._max_time = max_time
        if self.mtask_args is not None:
            self._max_length = self.mtask_args.model.generation_max_length
            self._num_beams = self.mtask_args.model.generation_num_beams
            
        # memory metrics - must set up as early as possible
        self._memory_tracker.start()
        eval_dataset = self.eval_dataset if eval_dataset is None else eval_dataset
        eval_dataloader = self.get_eval_dataloader(eval_dataset)
        start_time = time.time()
        # Temporarily disable metric computation, we will do it in the loop here.
        compute_metrics = self.compute_metrics
        self.compute_metrics = None
        try:
            output = self.evaluation_loop(
                eval_dataloader,
                description="Evaluation",
                # No point gathering the predictions if there are no metrics, otherwise we defer to
                # self.args.prediction_loss_only
                prediction_loss_only=True if compute_metrics is None else None,
                ignore_keys=ignore_keys,
                metric_key_prefix=metric_key_prefix,
            )
        finally:
            self.compute_metrics = compute_metrics
        if eval_dataset is not None and self.compute_metrics is not None:
            eval_preds = self._post_process_function(
                eval_dataset,
                output.predictions,
                "eval_{}".format(math.ceil(self.state.epoch)),
            )
            summary = self.compute_metrics(eval_preds, section="dev", epoch=self.state.epoch)
            output.metrics.update(summary)

        n_samples = len(eval_dataset if eval_dataset is not None else self.eval_dataset)
        output.metrics.update(speed_metrics(metric_key_prefix, start_time, n_samples))
        # Prefix all keys with metric_key_prefix + '_'
        for key in list(output.metrics.keys()):
            if not key.startswith(f"{metric_key_prefix}_"):
                output.metrics[f"{metric_key_prefix}_{key}"] = output.metrics.pop(key)
        self.log(output.metrics)
        self.control = self.callback_handler.on_evaluate(self.args, self.state, self.control, output.metrics)
        self._memory_tracker.stop_and_update_metrics(output.metrics)
        return output.metrics


    def predict(
        self,
        test_dataset: Optional[Dataset],
        metric_key_prefix: str = "predict"
    ) -> PredictionOutput:
        self._max_length, self._num_beams  = None, None
        if self.mtask_args is not None:
            self._max_length = self.mtask_args.model.generation_max_length
            self._num_beams = self.mtask_args.model.generation_num_beams
            
        # memory metrics - must set up as early as possible
        self._memory_tracker.start()
        test_dataloader = self.get_test_dataloader(test_dataset)
        start_time = time.time()

        # Temporarily disable metric computation, we will do it in the loop here.
        compute_metrics = self.compute_metrics
        self.compute_metrics = None
        try:
            output = self.evaluation_loop(
                test_dataloader,
                description="Inference",
                metric_key_prefix=metric_key_prefix,
            )
            # self.tokenizer.pad_token_id
            pad_id = self.processing_class.pad_token_id if self.model.type == 'llm' else self.processing_class.tokenizer.pad_token_id
            output.predictions[output.predictions==-100] = pad_id
        finally:
            self.compute_metrics = compute_metrics
        eval_preds = self._post_process_function(
            test_dataset, 
            output.predictions, 
            metric_key_prefix
        )
        if self.args.should_evaluate:
            if self.compute_metrics is not None:
                output.metrics.update(self.compute_metrics(eval_preds, section="inference", epoch=None))
            #if not self.args.predict_without_evaluation_on_test_dataset:
            output.metrics.update(speed_metrics(metric_key_prefix, start_time, len(test_dataset)))
            # Prefix all keys with metric_key_prefix + '_'
            for key in list(output.metrics.keys()):
                if not key.startswith(f"{metric_key_prefix}_"):
                    output.metrics[f"{metric_key_prefix}_{key}"] = output.metrics.pop(key)
            self.log(output.metrics)
            self._memory_tracker.stop_and_update_metrics(output.metrics)

        return output       
    
    def prediction_step(
        self,
        model: nn.Module,
        inputs: Dict[str, Union[torch.Tensor, Any]],
        prediction_loss_only: bool,
        ignore_keys: Optional[List[str]] = None,
    ) -> Tuple[Optional[float], Optional[torch.Tensor], Optional[torch.Tensor]]:
        """
        Customized prediction_step
        Override the original prediction_step to enable predict with generate
        """
        
        # fj: modify src transformers/trainer.py/Trainer _prepare_input referring to latest version: https://github.com/huggingface/transformers/blob/main/src/transformers/trainer.py
        inputs = self._prepare_inputs(inputs)
        
        if self.model.model_tag.startswith("t5"):
            gen_kwargs = {
                "max_length": self._max_length if self._max_length is not None else self.model.config.max_length,
                "num_beams": self._num_beams if self._num_beams is not None else self.model.config.num_beams,
                "no_repeat_ngram_size": 0,  # FIXME: hard coding the no_repeat_ngram_size
            }
            generated_tokens = self.model.model.generate(
                inputs["input_ids"],
                attention_mask=inputs["attention_mask"],
                use_cache=True,
                **gen_kwargs,
            )
            # # in case the batch is shorter than max length, the output should be padded
            # if generated_tokens.shape[-1] < gen_kwargs["max_length"]:
            #     generated_tokens = self._pad_tensors_to_max_len(generated_tokens, gen_kwargs["max_length"])
            with torch.no_grad():
                outputs = model(**inputs)
                if 'labels' in inputs:
                    if self.label_smoother is not None:
                        loss = self.label_smoother(outputs, inputs["labels"]).mean().detach()
                    else:
                        loss = (outputs["loss"] if isinstance(outputs, dict) else outputs[0]).mean().detach()
                else:
                    loss = None
            labels = inputs["labels"]
            # if labels.shape[-1] < gen_kwargs["max_length"]:
            #     labels = self._pad_tensors_to_max_len(labels, gen_kwargs["max_length"])
            return (loss, generated_tokens, labels)
        else:   
            with torch.no_grad():
                generated_tokens = self.model.model.generate(
                    **inputs,
                    **self.model.gen_kwargs,
                )
                # extract response in batch
                generated_tokens = generated_tokens[:, inputs.input_ids.shape[1]:]
                loss, labels = None, None
                return (loss, generated_tokens, labels)

    def _post_process_function(
        self, 
        dataset: Dataset, 
        predictions: np.ndarray, 
        stage: str
    ) -> EvalPrediction:        
        assert isinstance(dataset, Dataset)
        if self.model.type == 'llm':
            #predictions = self.tokenizer.batch_decode(predictions, skip_special_tokens=True)
            predictions = self.processing_class.batch_decode(predictions, skip_special_tokens=True)
        
        if self.model.type == 'lmm':
            clean_up_tokenization_spaces = True if self.model.model_tag.startswith('qwen2-vl') else False
            predictions = self.processing_class.batch_decode(predictions, skip_special_tokens=True, clean_up_tokenization_spaces=clean_up_tokenization_spaces)
        
        # Save locally.

        if (stage == 'predict' or stage.startswith('eval_')) and (self.args.local_rank <= 0) and (not self.args.do_not_save_results):
            if self.model.model_tag.startswith("t5"):
                save_fn = stage + '_predictions.json'
            else:
                save_fn = 'predictions.json'
            all_data, failed = [], []
            post_processed_predictions = []
            for idx in range(len(predictions)):
                raw_output = " ".join(predictions[idx].split())
                thinking_content = ""
                if self.model.model_tag.startswith("qwen3") and isinstance(raw_output, str) and self.args.enable_thinking:
                    thinking_content = regex.findall(r"<think>.*<\/think>", raw_output)[0]
                    raw_output = regex.sub(r"<think>.*<\/think>", "", raw_output).strip()
                out_format_version = self.args.current_prompt_meta['out_format']
                need_extract = self.args.current_prompt_meta['template']['output_format'][out_format_version]['post_process_func']
                if need_extract is True:
                    processed_prediction = extract_json_output(raw_output)
                elif callable(need_extract):
                    processed_prediction = need_extract(raw_output)
                else:
                    processed_prediction = raw_output
                #post_processed_predictions.append(processed_prediction)
                meta_js = dataset.examples[idx].attrs
                failed_record = []
                # if 'prediction' in meta_js:
                #     meta_js.pop('prediction')
                if 'failed_record' in meta_js:
                    failed_record = meta_js.pop('failed_record')
            
                keys_to_remove = ['prediction', "processed_prediction", "processed_dependency_prediction", "gathered_predictions"]
                if (self.args.task == 'mami') and (self.args.current_prompt_meta['template']['name'] == "Integrate"):
                    keys_to_remove.remove("gathered_predictions")
                for c_key in keys_to_remove:
                    if c_key in meta_js:
                        meta_js.pop(c_key)
                # if "processed_prediction" in meta_js:
                #     meta_js.pop("processed_prediction")
                # if "processed_dependency_prediction" in meta_js:
                #     meta_js.pop("processed_dependency_prediction") 
                if processed_prediction in ['failed_to_extract_json', 'gen_error']:
                    new_kv = {
                        "prediction": raw_output, 
                        "processed_prediction": meta_js['text'],
                        "failed_record": failed_record + [f"{self.args.current_model_type}-{self.args.current_round}-{processed_prediction}"]
                    }
                    failed.append(dict(**new_kv, **meta_js))
                else:
                    new_kv = {
                        "prediction": raw_output, 
                        "processed_prediction": processed_prediction
                    }
                if (self.args.current_prompt_meta['template']['name']=='Extract') and (self.args.current_prompt_meta['version'].lower().startswith('target')):
                    new_kv.update({self.args.current_prompt_meta['version']: processed_prediction})
                if (self.args.current_prompt_meta['template']['name'].startswith("Aux")):
                    # do_condition = True
                    # if isinstance(processed_prediction, dict):
                    #     do_condition = processed_prediction["flag"]
                    # if do_condition:
                    if "aux_info" not in meta_js:
                        meta_js["aux_info"] = {self.args.current_prompt_meta['version']: processed_prediction}
                    else:
                        meta_js["aux_info"][self.args.current_prompt_meta['version']] = processed_prediction
                if (self.args.task == 'pridemm') and (self.args.current_prompt_meta['template']['name'].startswith("StepDecision")):
                    if "step_decision" not in meta_js:
                        meta_js["step_decision"] = {self.args.current_prompt_meta['version']: processed_prediction}
                    else:
                        meta_js["step_decision"][self.args.current_prompt_meta['version']] = processed_prediction
                    dataset.examples[idx].attrs = meta_js
                if thinking_content:
                    new_kv["thinking"] = thinking_content

                all_data.append(dict(**new_kv, **meta_js))
            
            with open(f"{self.args.output_dir}/{save_fn}", "w") as f:
                json.dump(all_data, f, indent=4,) 
            if failed:
                with open(f"{self.args.output_dir}/failed_post_process.json", "w") as f:
                    json.dump(failed, f, indent=4,) 
                logger.info(f"{self.args.current_model_type}-{self.args.current_round}-#failed:{len(failed)}")
            print(f"#data instances = {len(all_data)}")
            # with open(f"{self.args.output_dir}/{save_fn}", "w") as f:
            #     json.dump(
            #         [dict(**{"prediction": " ".join(predictions[idx].split())}, **dataset.examples[idx].attrs) for idx in range(len(predictions))],
            #         f,
            #         indent=4,
            #     )
        return EvalPrediction(predictions=predictions, items=[dataset.examples[idx].attrs for idx in range(len(predictions))])
        # return EvalPrediction(predictions=post_processed_predictions, items=[dataset.examples[idx].attrs for idx in range(len(predictions))])

    def _compute_metrics(self, eval_prediction: EvalPrediction, section='predict', epoch=None) -> dict:
        return self.evaluator.evaluate(preds=eval_prediction.predictions, golds=eval_prediction.items, section=section, epoch=epoch)
