#export CUDA_VISIBLE_DEVICES=3
python generate_references.py --ModelToUse 'openai-gpt' --ReturnSequences 100 --Beams 100 --FilenameToWrite 'test.json' --FileIn ../data/references_for_lm.json
