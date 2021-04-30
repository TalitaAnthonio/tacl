from transformers import OpenAIGPTLMHeadModel, OpenAIGPTTokenizer
import torch
import pdb 
import json 
from transformers import BertGenerationTokenizer, BertGenerationDecoder, BertGenerationConfig
tokenizer = BertGenerationTokenizer.from_pretrained('google/bert_for_seq_generation_L-24_bbc_encoder')
config = BertGenerationConfig.from_pretrained("google/bert_for_seq_generation_L-24_bbc_encoder")
config.is_decoder = True
model = BertGenerationDecoder.from_pretrained('google/bert_for_seq_generation_L-24_bbc_encoder', config=config)

#model =  OpenAIGPTLMHeadModel.from_pretrained('openai-gpt', cache_dir="../../model")
#tokenizer = OpenAIGPTTokenizer.from_pretrained('openai-gpt', cache_dir="../../model")


#tokenizer = BigBirdTokenizer.from_pretrained('google/bigbird-roberta-base')
#model = BigBirdForPreTraining.from_pretrained('google/bigbird-roberta-base')

#model =  OpenAIGPTLMHeadModel.from_pretrained('openai-gpt', cache_dir="../../model")
#tokenizer = OpenAIGPTTokenizer.from_pretrained('openai-gpt', cache_dir="../../model")

path_to_file = '../analyse-predictions/bestmodels_predictions.json'

with open(path_to_file, 'r') as json_in: 
     data = json.load(json_in)


PATH_TO_FILE_IN_RESULTS = "../data/references_for_lm.json"

with open(PATH_TO_FILE_IN_RESULTS, 'r') as json_in: 
     other_info = json.load(json_in)


def generate_text(text, length): 

    results = []
    inputs = tokenizer(text, return_tensors="pt")['input_ids']
    outputs = model.generate(inputs, max_length=inputs.size(1)+length, num_return_sequences=50, num_beams=50)

    # this is the length in string length. 
    prompt_length = len(tokenizer.decode(inputs[0], skip_special_tokens=True, clean_up_tokenization_spaces=True))
    res = [tokenizer.decode(outputs[i])[prompt_length:] for i in range(len(outputs))]
    return res  

def count_matches(predictions, correct_ref):
    predictions = [prediction.lower() for prediction in predictions]
    if correct_ref.lower() in predictions:  
       return 1 
    else: 
        return 0 


def main(): 
    
    total_matches = 0 

    counter = 0 
    for key, _ in data.items(): 
        counter +=1 
        revised_untill_insertion = data[key]['revised_untill_insertion']
        #text = data[key]['par'] + ' ' + revised_untill_insertion
        text = other_info[key]["language_model_text"]
        res = generate_text(text, len(other_info[key]['reference']))
        print("============")
        print(res)
        print("correct reference", data[key]["CorrectReference"])
        total_matches += count_matches(res, data[key]["CorrectReference"])
        if counter == 20: 
           break 

main()