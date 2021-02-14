import json 
from lm_scorer import GPTScorer
from transformers import OpenAIGPTLMHeadModel, OpenAIGPTTokenizer
from progress.bar import Bar
import pdb

PATH_TO_FILE_IN_RESULTS = "results-on-test-set.json"
TOKENIZER = OpenAIGPTTokenizer.from_pretrained('openai-gpt')
MODEL = OpenAIGPTLMHeadModel.from_pretrained('openai-gpt', return_dict=True).eval()
PATH_TO_FILE_IN =  "../data/references_for_lm.json"
PATH_TO_FILE_OUT = "results-on-test-set-reranked-context.json"

with open(PATH_TO_FILE_IN, 'r') as json_in: 
     data = json.load(json_in)


def convert_lines_to_dict_format(path_to_json_lines):
    results_in_dict_format = {}
    with open(path_to_json_lines) as json_in: 
            for line in json_in: 
                line = json.loads(line)
                key = line['key']
                results_in_dict_format[key] = line 
                # add data from other file 
                results_in_dict_format[key].update(data[key])
    return results_in_dict_format

def trunc_text(text): 
    inputs = TOKENIZER.encode(text, add_special_tokens=False, return_tensors="pt") 
    inputs_truncated = inputs.tolist()[0]

    tokenized_text = []
    total_length = 0 
    if len(inputs_truncated) >= 512: 
       context_line_splitted = text.split('\n')
       context_line_splitted.reverse()
       for sent in context_line_splitted: 
           tokenized_sent = TOKENIZER.encode(sent, add_special_tokens=False, return_tensors="pt") 
           total_length += len(tokenized_sent.tolist()[0])
           if total_length < 511: 
              tokenized_text.append(TOKENIZER.decode(tokenized_sent.tolist()[0]))
       tokenized_text.reverse()
       return ' '.join(tokenized_text)
    else: 
        return text.replace('\n', ' ')


def compute_perplexity(generated_sequences): 
    generated_sequences_with_perplexity_plus_revised_collection = []
    for rank, sequence, insertion in generated_sequences:  
        # compute the perplexity. 
        # truncate text if necessary 
        sequence = trunc_text(sequence) 

        # remove timestamps 
        sequence = remove_timestamps(sequence)
        perplexity_for_sentence = GPTScorer(TOKENIZER, MODEL, sequence=sequence).get_perplexity()
        generated_sequences_with_perplexity_plus_revised_collection.append([rank, sequence, insertion, perplexity_for_sentence])
    generated_sequences_with_perplexity_plus_revised_collection.sort(key=lambda x: x[-1], reverse=False)
    return generated_sequences_with_perplexity_plus_revised_collection 

def rerank_using_perplexity(revised_untill_insertion, revised_after_insertion, generated_sequences): 
    # everything up to the insertion 
    generated_sequences_within_sentence = []
    for position, generated_sequence in enumerate(generated_sequences, 1): 
        full_sequence_with_generated_insertion = "{0} {1} {2}".format(revised_untill_insertion, generated_sequence.lstrip(), revised_after_insertion)
        generated_sequences_within_sentence.append([position, full_sequence_with_generated_insertion, generated_sequence])
    rerank_with_perplexity = compute_perplexity(generated_sequences_within_sentence)
    return [elem[2] for elem in rerank_with_perplexity]

def remove_timestamps(context): 
    context = context.split()
    for elem in context: 
        if 'Timestamp' in elem: 
            context = context[2:]
            break 
    return ' '.join(context) 


def main(): 
    # revised_afer_insertion 
    results_in_dict_format = convert_lines_to_dict_format(PATH_TO_FILE_IN_RESULTS)
    
    bar = Bar('Processing ..', max=len(results_in_dict_format.keys()))
    
    d = {}
    counter = 0 
    for key, _ in results_in_dict_format.items(): 
        if results_in_dict_format[key]['Split'] == 'TEST': 
            bar.next()
            counter +=1 
            if counter == 333: 
                context = results_in_dict_format[key]['par']
                generated_sequences = results_in_dict_format[key]['predictions']['generated_texts']
                revised_untill_insertion = context.rstrip('\n')  + results_in_dict_format[key]['revised_untill_insertion']
                if 'revised_after_insertion' not in results_in_dict_format[key].keys(): 
                    revised_after_insertion = results_in_dict_format[key]['revised_afer_insertion']
                else: 
                    revised_after_insertion = results_in_dict_format[key]['revised_after_insertion']
            
                reranked = rerank_using_perplexity(revised_untill_insertion, revised_after_insertion, generated_sequences)
                
                d[key] = results_in_dict_format[key]
                d[key].update({"generated_text_perplexity_context": reranked})
            
    bar.finish()

    with open(PATH_TO_FILE_OUT, 'w') as json_out: 
            json.dump(d, json_out)


main()
