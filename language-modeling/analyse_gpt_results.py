import json 
import random
import pandas as pd 
import torch 
from lm_scorer import GPTScorer
from transformers import OpenAIGPTTokenizer, OpenAIGPTLMHeadModel
from progress.bar import Bar 


# the file with the results 
PATH_TO_FILE_IN_RESULTS = "results-on-test-dev-finetuned.json"
# the file with the other information 
PATH_TO_FILE_IN =  "../data/references_for_lm.json"


with open(PATH_TO_FILE_IN, 'r') as json_in: 
     data = json.load(json_in)


def compute_overlap(generated_sequences, correct_insertion, top_k=100): 
    "function to check if the reference is in the generated sequences"
    generated_sequences_stripped = [sequence.lstrip() for sequence in generated_sequences]
    generated_sequences_stripped = generated_sequences_stripped[:top_k]
    #print("Top {0}: {1}".format(top_k, generated_sequences_stripped))
    matches = []
    if correct_insertion in generated_sequences_stripped: 
        return 1 
    else: 
        return 0 

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


def main(): 

    results_in_dict_format = convert_lines_to_dict_format(PATH_TO_FILE_IN_RESULTS)

    counter = 0 
    total = 0 
    bar = Bar('Processing ...', max=len(results_in_dict_format.keys()))
    for key, _ in results_in_dict_format.items(): 
        if results_in_dict_format[key]['Split'] == 'TEST': 
            total +=1 
            #bar.next()
            top100_predictions = results_in_dict_format[key]['predictions']['generated_texts']
            # do the extra step here 
            correct_reference = results_in_dict_format[key]['reference']
            if type(correct_reference) != str: 
               correct_reference = ' '.join(correct_reference)


            # compute 
            correct_or_not = compute_overlap(top100_predictions, correct_reference, top_k=100)
            if correct_or_not == 1: 
                print(correct_reference, '\t', results_in_dict_format[key]['predictions']['generated_texts'])
            counter += correct_or_not

    #bar.finish()
    print("total correct", counter)          
    print("total in data", total)
    print("percentage", counter/total)


main()