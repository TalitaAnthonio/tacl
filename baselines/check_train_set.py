import json 
from transformers import OpenAIGPTTokenizer, OpenAIGPTLMHeadModel
import pandas as pd 

TOKENIZER = OpenAIGPTTokenizer.from_pretrained('openai-gpt')
MODEL = OpenAIGPTLMHeadModel.from_pretrained('openai-gpt', return_dict=True).eval()
PATH_TO_FILE_IN =  "../data/references_for_lm.json"

with open(PATH_TO_FILE_IN, "r") as json_in: 
     data = json.load(json_in)


def make_dataframe(data, filename_to_write): 
    df = pd.DataFrame.from_dict(data)
    df.to_csv('../data/'+filename_to_write, sep=',', index=False)


def remove_timestamps(context): 
    context = context.split()
    for elem in context: 
        if 'Timestamp' in elem: 
            context = context[2:]
            break 
    return ' '.join(context) 




def trunc_text(text): 
    inputs = TOKENIZER.encode(text, add_special_tokens=False, return_tensors="pt") 
    inputs_truncated = inputs.tolist()[0]       
    inputs_truncated = inputs_truncated[-512:]
    decode = TOKENIZER.decode(inputs_truncated)
    
    return decode



def main():

    train = {}
    for key, _ in data.items(): 
        # remove timestamps 
        context_with_removed_timestamps = remove_timestamps(data[key]['par'])

        # deal with data type differences 
        if type(data[key]['revised_sentence']) == list: 
           context_plus_revised_sentence = context_with_removed_timestamps + ' ' + ' '.join(data[key]['revised_sentence'])
        else: 
            context_plus_revised_sentence = context_with_removed_timestamps + ' ' + data[key]['revised_sentence']
        
        # truncate text in case longer than 512 tokens. 
        context_plus_revised_sentence = trunc_text(context_plus_revised_sentence)

        if data[key]['Split'] == 'DEV': 
            train[key] = context_plus_revised_sentence

    
    with open("contextplusreviseddev.json", "w") as json_out: 
         json.dump(train, json_out)
main()