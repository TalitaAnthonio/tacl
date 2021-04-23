
# use open-ai gpt for gpt2 
# other models: xlnet-base-uncased, openai-gpt, gpt2, transfo-xl-wt103 (but very slow)
# the fillmask pipeline only works for one token masked.
# revised_untill_insertion is the key for  ../data/bigram_insertions_for_lm_generative.json
# ValueError: `num_return_sequences` has to be smaller or equal to `num_beams`.

# python generate_references.py --ModelToUse 'openai-gpt' --ReturnSequences 100 --Beams 100 --FilenameToWrite 'test.json' --FileIn ../data/references_for_lm.json

from transformers import pipeline, set_seed, XLNetConfig, XLNetTokenizer, XLNetLMHeadModel,  OpenAIGPTTokenizer, OpenAIGPTLMHeadModel
import json 
import torch 
import pdb 
device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
device='cpu'
torch.cuda.empty_cache()


import argparse 
ap = argparse.ArgumentParser(description="use language modeling for generative models (gpt or xlnet)")

ap.add_argument("--ModelToUse", required=True, type=str, default='openai-gpt', 
                help="gpt for gpt; other strings will run xlnet")
ap.add_argument("--ReturnSequences", required=True, type=int, default=100, 
                help="number of sequences to return")

ap.add_argument("--Beams", required=True, type=int, default=100, 
                help="number of sequences to return")
ap.add_argument('--FilenameToWrite', required=True, help='name of file to write out', type=str)
ap.add_argument('--FileIn', required=True, help = 'name of the file to use', type=str)

args = vars(ap.parse_args())
model_to_use = args['ModelToUse']
num_return_sequences = args['ReturnSequences']
num_beams = args['Beams']
path_to_file_out = args['FilenameToWrite']
path_to_file_in = args['FileIn']
TRUNC_BY_WORD = False


print("--------------")
print('devices used', device)
print('device range', torch.cuda.device_count())


#device='cpu'
#print(device)

# read the first and second dict 

with open(path_to_file_in, "r") as json_in: 
     single_insertions = json.load(json_in)

if model_to_use == 'openai-gpt': 
    model =  OpenAIGPTLMHeadModel.from_pretrained('openai-gpt', cache_dir="../../model")
    tokenizer = OpenAIGPTTokenizer.from_pretrained('openai-gpt', cache_dir="../../model")
else: 
    model_path='xlnet-base-cased'
    model =   XLNetLMHeadModel.from_pretrained(model_path, cache_dir="../../model").to(device)
    tokenizer = XLNetTokenizer.from_pretrained(model_path, cache_dir="../../model")



# always used the defautl configuration file 
def use_text_generation(text_to_predict, insertion_length): 
    
    tokenized_text =  tokenizer.tokenize(text_to_predict)
    print("length of the tokenized text", len(tokenized_text)) 
    if len(tokenized_text) >= 512: 

        inputs = tokenizer.encode(text_to_predict, add_special_tokens=False, return_tensors="pt") 

        # truncate 
        inputs_truncated = inputs.tolist()[0]
        truncate_point = (512-insertion_length) * -1 
        print(truncate_point)
        inputs_truncated = inputs_truncated[truncate_point:]
        
        #if insertion_length == 2: 
        #    inputs_truncated = inputs_truncated[-511:]
        #else: 
        #    inputs_truncated = inputs_truncated[-512:]
        
        inputs = torch.tensor(inputs_truncated, dtype=torch.int64).unsqueeze(0)
        encoded_inputs = tokenizer.decode(inputs[0])
        prompt_length = len(tokenizer.decode(inputs[0], skip_special_tokens=True, clean_up_tokenization_spaces=True))

        if device!='cpu': 
            outputs = model.generate(inputs, max_length=inputs.size()[1]+insertion_length, num_return_sequences=num_return_sequences, num_beams=num_return_sequences)
            model.to(device)

        else: 
            outputs = model.generate(inputs, max_length=inputs.size()[1]+insertion_length, num_return_sequences=num_return_sequences, num_beams=num_beams)
    
    else: 
    
        inputs = tokenizer.encode(text_to_predict, add_special_tokens=False, return_tensors="pt") 
        encoded_inputs = tokenizer.decode(inputs[0])

        prompt_length = len(tokenizer.decode(inputs[0], skip_special_tokens=True, clean_up_tokenization_spaces=True))
        #print(inputs.size()[1]+insertion_length)
        if device != 'cpu': 
            outputs = model.generate(inputs, max_length=inputs.size()[1]+insertion_length, num_return_sequences=num_return_sequences, num_beams=num_return_sequences)
            model.to(device)

        else: 
            outputs = model.generate(inputs, max_length=inputs.size()[1]+insertion_length, num_return_sequences=num_return_sequences, num_beams=num_beams)

    return {"generated_texts": [tokenizer.decode(outputs[i])[prompt_length:] for i in range(len(outputs))], "tokenized_in_model": encoded_inputs}


def use_text_generation_truncate_by_sentence(text_to_predict, insertion_length): 
    inputs = tokenizer.encode(text_to_predict, add_special_tokens=False, return_tensors="pt") 
    inputs_truncated = inputs.tolist()[0]

    tokenized_text = []
    total_length = 0 
    if len(inputs_truncated) >= 512: 
       context_line_splitted = text_to_predict.split('\n')
       context_line_splitted.reverse()
       for sent in context_line_splitted: 
           tokenized_sent = tokenizer.encode(sent, add_special_tokens=False, return_tensors="pt") 
           total_length += len(tokenized_sent.tolist()[0])
           if total_length < (512-insertion_length): 
              tokenized_text.append(tokenizer.decode(tokenized_sent.tolist()[0]))
       tokenized_text.reverse()
       text_to_predict = ' '.join(tokenized_text)
    else: 
        text_to_predict = text_to_predict    
    inputs = tokenizer.encode(text_to_predict, add_special_tokens=False, return_tensors="pt") 
    encoded_inputs = tokenizer.decode(inputs[0])

    prompt_length = len(tokenizer.decode(inputs[0], skip_special_tokens=True, clean_up_tokenization_spaces=True))
    #print(inputs.size()[1]+insertion_length)
    if device != 'cpu': 
        outputs = model.generate(inputs, max_length=inputs.size()[1]+insertion_length, num_return_sequences=num_return_sequences, num_beams=num_return_sequences)
        model.to(device)

    else: 
        outputs = model.generate(inputs, max_length=inputs.size()[1]+insertion_length, num_return_sequences=num_return_sequences, num_beams=num_beams)

    return {"generated_texts": [tokenizer.decode(outputs[i])[prompt_length:] for i in range(len(outputs))], "tokenized_in_model": encoded_inputs}



def main():
    counter = 0 

    with open(path_to_file_out, "w") as json_out: 
        for revision_id, _ in single_insertions.items(): 
            if  single_insertions[revision_id]['Split'] == 'TEST': 
                counter +=1 
                insertion = single_insertions[revision_id]["insertion"]
                print("running {0}".format(counter))
                text_to_generate_from =  single_insertions[revision_id]['par'].rstrip('\n') + single_insertions[revision_id]['revised_untill_insertion']
                #text_to_generate_from = single_insertions[revision_id]["revised_untill_insertion"]
                max_insertion_length = single_insertions[revision_id]["reference-type"]
                print("reference type is", max_insertion_length)
                if max_insertion_length == 'unigram': 
                    print("the length is a unigram")
                    max_length = 1 
                elif max_insertion_length == 'bigram': 
                    max_length = 2 
                else: 
                    max_length = 3

                if text_to_generate_from.split() != []: 
                    try:
                        if TRUNC_BY_WORD:
                            text_to_generate_from = single_insertions[revision_id]["language_model_text"]  
                            predicted_text = use_text_generation(text_to_generate_from, max_length)
                        else: 
                            context = single_insertions[revision_id]['par']
                            text_to_generate_from = context.rstrip('\n') + single_insertions[revision_id]['revised_untill_insertion']
                            predicted_text = use_text_generation_truncate_by_sentence(text_to_generate_from, max_length)

                        dict_to_write =  {"predictions": predicted_text, "key": revision_id, "revised_sentence": single_insertions[revision_id]["revised_sentence"], "insertion": single_insertions[revision_id]["insertion"]}
                        json_out.write(json.dumps(dict_to_write, default=str) + '\n')
                    except IndexError: 
                        dict_to_write = {"predictions": "check again", "key": revision_id}
                        json_out.write(json.dumps(dict_to_write, default=str) + '\n') 

                else:
                    dict_to_write = {"predictions": "check again", "key": revision_id}
                    json_out.write(json.dumps(dict_to_write, default=str) + '\n') 
main()

