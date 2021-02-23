import json 

MODEL_NAME = "GPT+P-perplexity"

PATH_TO_RERANKED_FILE = "results-on-dev-reranked-context-test.json"
#PATH_TO_RERANKED_FILE = "results-on-test-set-reranked-context-finetuned.json"


#with open(PATH_TO_RERANKED_FILE, 'r') as json_in: 
#     results_in_dict_format = json.load(json_in)


def convert_lines_to_dict_format(path_to_json_lines):
    results_in_dict_format = {}
    with open(path_to_json_lines) as json_in: 
            for line in json_in: 
                line = json.loads(line)
                key = line['key']
                results_in_dict_format[key] = line 
                # add data from other file 
                #results_in_dict_format[key].update(data[key)
    return results_in_dict_format

results_in_dict_format = convert_lines_to_dict_format(PATH_TO_RERANKED_FILE)

def compute_overlap(generated_sequences, correct_insertion, top_k=100): 
    "function to check if the reference is in the generated sequences"
    generated_sequences_stripped = [sequence.lstrip().lower() for sequence in generated_sequences]
    generated_sequences_stripped = generated_sequences_stripped[:top_k]

    #print("Top {0}: {1}".format(top_k, generated_sequences_stripped))
    if correct_insertion.lower() in  generated_sequences_stripped: 
       return 1 
    else: 
        return 0 

def main():
    total_correct = 0 
    total = 0  
    d = {}
    for key, _ in results_in_dict_format.items(): 
        if results_in_dict_format[key]['Split'] == 'DEV': 
            #print(results_in_dict_format[key].keys())
            total +=1 
            top100_predictions = results_in_dict_format[key]['generated_text_perplexity_context']
            # do the extra step here 
            correct_reference = results_in_dict_format[key]['reference']
            if type(correct_reference) != str: 
               correct_reference = ' '.join(correct_reference)


            # compute 
            correct_or_not = compute_overlap(top100_predictions, correct_reference, top_k=1)
            if correct_or_not == 1: 
                correct_or_not_value = True 
            else: 
                correct_or_not_value = False 

                #correct_cases[key] = results_in_dict_format[key]

            total_correct += correct_or_not 
            d[key] = {"{0}Pred".format(MODEL_NAME): top100_predictions[0].lstrip().lower(), "{0}Corr".format(MODEL_NAME): correct_or_not_value}
            print(d[key])
    
    print(total_correct)
    print(total)
    print(total_correct/total)

    print(len(d.keys()))

    #with open("correct_cases_dev_finetuned_context.json", "w") as json_out: 
    #    json.dump(correct_cases, json_out)
    
    path_to_file_out = "{0}.json".format(MODEL_NAME)

    with open(path_to_file_out, "w") as json_out: 
         json.dump(d, json_out)




main()
