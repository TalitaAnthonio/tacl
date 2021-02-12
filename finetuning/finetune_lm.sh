export CUDA_VISIBLE_DEVICES=0,1,2,3
python run_clm.py --model_name_or_path openai-gpt --train_file ./data/train_context_revised.csv --validation_file ./data/dev_context_revised.csv --do_train --do_eval --output_dir revised-context-model --block_size 512 --cache_dir ./models --per_device_train_batch_size=4
