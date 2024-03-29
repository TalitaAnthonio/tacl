import json 
from lm_scorer import GPTScorer
from transformers import OpenAIGPTLMHeadModel, OpenAIGPTTokenizer
from progress.bar import Bar

PATH_TO_FILE_IN_RESULTS = "results-on-dev-set-finetuned.json"
TOKENIZER = OpenAIGPTTokenizer.from_pretrained('finetuned-model')
MODEL = OpenAIGPTLMHeadModel.from_pretrained('finetuned-model', return_dict=True).eval()
PATH_TO_FILE_IN =  "../data/references_for_lm.json"
PATH_TO_FILE_OUT = "results-on-dev-set-finetuned-reranked.json"

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


def compute_perplexity(generated_sequences): 
    generated_sequences_with_perplexity_plus_revised_collection = []
    for rank, sequence, insertion in generated_sequences:  
        # bereken de perplexity 
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
    print("================= reranked ===================")
    print("{0}\t{1}\t{2}\t{3}\t{4}".format("current pos", "prev pos", "full sequence", "generated referece", "perplexity"))
    for index, elem in enumerate(rerank_with_perplexity,1): 
        print("{0}\t{1}\t{2}\t{3}\t{4}".format(index, elem[0], elem[1], elem[2], elem[3], elem[-1]))
    return [elem[2] for elem in rerank_with_perplexity]


def main(): 
    # revised_afer_insertion 
    results_in_dict_format = convert_lines_to_dict_format(PATH_TO_FILE_IN_RESULTS)
    
    bar = Bar('Processing ..', max=len(results_in_dict_format.keys()))
    
    d = {}
    counter = 0 
    for key, _ in results_in_dict_format.items(): 
        if results_in_dict_format[key]['Split'] == 'DEV': 
            bar.next()
            counter +=1 
            generated_sequences = results_in_dict_format[key]['predictions']['generated_texts']
            revised_untill_insertion = results_in_dict_format[key]['revised_untill_insertion']
            if 'revised_after_insertion' not in results_in_dict_format[key].keys(): 
                revised_after_insertion = results_in_dict_format[key]['revised_afer_insertion']
            else: 
                revised_after_insertion = results_in_dict_format[key]['revised_after_insertion']
        
            reranked = rerank_using_perplexity(revised_untill_insertion, revised_after_insertion, generated_sequences)
            d[key] = results_in_dict_format[key]
            d[key].update({"generated_text_perplexity": reranked})
            print("======================================")
 
            
    bar.finish()

    with open(PATH_TO_FILE_OUT, 'w') as json_out: 
         json.dump(d, json_out)


main()
