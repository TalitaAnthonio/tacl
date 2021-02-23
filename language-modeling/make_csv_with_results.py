import json 
import random
import pandas as pd 
import torch 
from lm_scorer import GPTScorer
from transformers import OpenAIGPTTokenizer, OpenAIGPTLMHeadModel
from progress.bar import Bar 
import pandas as pd 


# the file with the results 
PATH_TO_FILE_IN_RESULTS = "results-on-dev-set-finetuned.json"
# the file with the other information 
PATH_TO_FILE_IN =  "../data/references_for_lm.json"
PATH_TO_OTHER = "results-on-dev-set.json"

with open(PATH_TO_FILE_IN, 'r') as json_in: 
     data = json.load(json_in)


def compute_overlap(generated_sequences, correct_insertion, top_k=100): 
    "function to check if the reference is in the generated sequences"
    generated_sequences_stripped = [sequence.lstrip().lower() for sequence in generated_sequences]
    generated_sequences_stripped = generated_sequences_stripped[:top_k]
    #print("Top {0}: {1}".format(top_k, generated_sequences_stripped))
    matches = []
    if correct_insertion.lower() in generated_sequences_stripped: 
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

def check_correctness(PATH_TO_RESULTS_FILE, model_name, key): 
    d = {"{0}Pred".format(model_name): [], "{0}Correct".format(model_name):[]}
    results_in_dict_format = convert_lines_to_dict_format(PATH_TO_RESULTS_FILE)
    correct_reference = results_in_dict_format[key]['reference']
    if type(correct_reference) != str: 
        correct_reference = ' '.join(correct_reference)

    top100_predictions = results_in_dict_format[key]['predictions']['generated_texts']

    correct_or_not = compute_overlap(top100_predictions, correct_reference, top_k=1)

    d["{0}Pred".format(model_name)] = top100_predictions[0].lstrip()

    if correct_or_not == 1:     
         d["{0}Correct".format(model_name)] = True 

    else: 

        d["{0}Correct".format(model_name)] = False 
    return d 


def main(): 

    results_in_dict_format = convert_lines_to_dict_format(PATH_TO_FILE_IN_RESULTS)

    errors = {}
    correct_cases = {}
    counter = 0 
    total = 0 
    data_for_prediction_csv = {}

    bar = Bar('Processing ...', max=len(results_in_dict_format.keys()))
    for key, _ in results_in_dict_format.items(): 
        if results_in_dict_format[key]['Split'] == 'DEV': 
            total +=1 
            #bar.next()
            top100_predictions = results_in_dict_format[key]['predictions']['generated_texts']
            # do the extra step here 
            correct_reference = results_in_dict_format[key]['reference']

            if type(correct_reference) != str: 
               correct_reference = ' '.join(correct_reference)


            # compute 
            correct_or_not = compute_overlap(top100_predictions, correct_reference, top_k=1)

            if correct_or_not == 1: 
                print(correct_reference, '\t', results_in_dict_format[key]['predictions']['generated_texts'])
                correct_cases[key] = results_in_dict_format[key]

                data_for_prediction_csv[key] = {"GPT+FinetuningCorrect": True}
            
            else: 
                errors[key] = results_in_dict_format[key]

                data_for_prediction_csv[key] = {"GPT+FinetuningCorrect": False}

            # other info that needs to be added 


            if "tokenized_in_model" in results_in_dict_format[key].keys(): 
                par = results_in_dict_format[key]["tokenized_in_model"]
            else: 
                par = results_in_dict_format[key]["language_model_text"]

            counter += correct_or_not

            gpt_results = check_correctness(PATH_TO_OTHER, "GPT", key)
            if type(results_in_dict_format[key]["revised_sentence"]) == list: 
               revised_sentence = ' '.join(results_in_dict_format[key]["revised_sentence"])
            else: 
                revised_sentence  = results_in_dict_format[key]["revised_sentence"]

            data_for_prediction_csv[key].update({"CorrectReference": correct_reference, 
            "LeftContext": par, "GPTPred": gpt_results["GPTPred"], "GPTCorrect": gpt_results["GPTCorrect"], 
            "key": key, "GPT+FinetuningPred": top100_predictions[0].lstrip().lower(), "RevisedSentence": revised_sentence})


    #bar.finish()
    print("total correct", counter)          
    print("total in data", total)
    print("percentage", counter/total)

    print(len(correct_cases.keys()))
    #with open('correct_cases_dev_finetuned.json', 'w') as json_out: 
    #     json.dump(correct_cases, json_out)

    with open("GPTandFinetuning.json", 'w') as json_out: 
         json.dump(data_for_prediction_csv, json_out)

    #df = pd.DataFrame.from_dict(data_for_prediction_csv)
    #df.to_csv("GPTplusfinetuning.csv", sep='\t', index=False)
    #print(df)
main()