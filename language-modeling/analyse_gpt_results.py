import json 
import random
import pandas as pd 
import torch 
from lm_scorer import GPTScorer
from transformers import OpenAIGPTTokenizer, OpenAIGPTLMHeadModel
from progress.bar import Bar 


# the file with the results 
PATH_TO_FILE_IN_RESULTS = ""
# the file with the other information 
PATH_TO_FILE_IN = ""


with open(PATH_TO_FILE_IN, 'r') as json_in: 
     data = json.load(json_in)

with open(PATH_TO_FILE_IN_RESULTS, 'r') as json_in: 
     results = json.load(json_in)

def compute_overlap(generated_sequences, correct_insertion, insertion, top_k=100): 
    "function toc heck if the reference is in the generated sequences"
    generated_sequences_stripped = [sequence.lstrip() for sequence in generated_sequences]
    generated_sequences_stripped = generated_sequences_stripped[:top_k]
    print('top 10', generated_sequences_stripped)
    if type(correct_insertion) == list: 
        correct_insertion = ' '.join(correct_insertion)
    
    matches = []
    for generated_sequence in generated_sequences_stripped: 
        if generated_sequence == correct_insertion or generated_sequence.lower() == correct_insertion.lower(): 
            matches.append(1)
        else:
            matches.append(0)
    if 1 in matches: 
       return 1 
    else: 
        return 0 



#TODO: remove everything with RERANKED 
#TODO: make sure that the correct insertion is the reference. 


def main(): 
    final_set = {}
    bigram_references.update(single_references)
    with open(path_to_file) as json_in: 
            for line in json_in: 
                line = json.loads(line)
                key = line['key']
                final_set[key] = line
                additional_info = {"index_of_reference": bigram_references[key]['index_of_reference'], "index_of_insertion": bigram_references[key]['index_of_insertion'], 'Split': split_info[key]['Split']}
                final_set[key].update(additional_info)



    counter = 0 
    total = 0 
    set_for_perplexity = {}
    total_insertion = 0 
    bar = Bar('Processing ...', max=len(final_set.keys()))
    for key, _ in final_set.items(): 
        if 'insertion' in final_set[key].keys():
            if final_set[key]['Split'] == 'TEST': 
                bar.next()
                #if final_set[key]['Split'] == 'TEST': 
                index_of_insertion = final_set[key]['index_of_insertion']
                index_of_reference = final_set[key]['index_of_reference']
                insertion = final_set[key]['insertion']
                if index_of_insertion == index_of_reference and type(index_of_insertion[0]) == list: 
                    correct_insertion = final_set[key]['revised_sentence'][index_of_reference[0][0]:index_of_reference[0][1]+1]
                    if not RERANK: 
                        res_with_perplex = final_set[key]['predictions']['generated_texts']
                    else: 
                        res_with_perplex = reranked[key]['generated_sequences_perplex']
                    #res_with_perplex = rerank_using_perplexity_bigrams(final_set[key]['revised_sentence'], final_set[key]['predictions']['generated_texts'],index_of_reference[0][0], index_of_reference[0][1]+1)
            
                                        
                else: 
                    if len(final_set[key]['insertion']) == 1: 
                        assert index_of_reference == index_of_insertion
                        assert len(index_of_insertion) == 1
                        correct_insertion = final_set[key]['revised_sentence'][index_of_insertion[0]]
                        if not RERANK: 
                            res_with_perplex = final_set[key]['predictions']['generated_texts']
                        else: 
                            #res_with_perplex = reranked[key]['generated_sequences_perplex']
                            res_with_perplex = rerank_using_perplexity(final_set[key]['revised_sentence'], final_set[key]['predictions']['generated_texts'], index_of_reference[0])                    
                    else: 
                        assert len(index_of_insertion[0]) == 2
                        correct_insertion = final_set[key]['revised_sentence'][index_of_insertion[0][index_of_reference]]
                        if not RERANK: 
                            res_with_perplex = final_set[key]['predictions']['generated_texts']
                        else: 
                            #res_with_perplex = reranked[key]['generated_sequences_perplex']
                            res_with_perplex = rerank_using_perplexity(final_set[key]['revised_sentence'], final_set[key]['predictions']['generated_texts'], index_of_insertion[0][index_of_reference]) 
                    
                
                #correct_or_not = compute_overlap(res_with_perplex, correct_insertion, insertion)
                #counter += correct_or_not
                total +=1 
                if total == 2: 
                   break 
                #print(counter)
                #print(total)

            set_for_perplexity[key] = final_set[key]
            set_for_perplexity[key].update({"generated_sequences_perplex": res_with_perplex})
            set_for_perplexity[key].update({"Split": final_set[key]['Split']})
    bar.finish()          
    #print(total)
    #print(counter)

    #print(len(set_for_perplexity))
    with open('references_reranked_dev_test_revised_context_finetuned_reranked.json', 'w') as json_out: 
          json.dump(set_for_perplexity, json_out)


main()