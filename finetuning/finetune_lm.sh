export CUDA_VISIBLE_DEVICES=0,1,2,3
python run_clm.py --model_name_or_path openai-gpt --train_file ../data/train.csv --validation_file ./data/dev.csv --do_train --do_eval --output_dir finetuned-model --block_size 512 --per_device_train_batch_size=4
