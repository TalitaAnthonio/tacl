import json 

PATH_TO_RERANKED_FILE = "results-on-dev-set-reranked-context-finetuned.json"

with open(PATH_TO_RERANKED_FILE, 'r') as json_in: 
     results_in_dict_format = json.load(json_in)


def compute_overlap(generated_sequences, correct_insertion, top_k=100): 
    "function to check if the reference is in the generated sequences"
    generated_sequences_stripped = [sequence.lstrip() for sequence in generated_sequences]
    generated_sequences_stripped = generated_sequences_stripped[:top_k]

    #print("Top {0}: {1}".format(top_k, generated_sequences_stripped))
    if correct_insertion in  generated_sequences_stripped: 
       return 1 
    else: 
        return 0 

def main():
    total_correct = 0 
    total = 0  
    for key, _ in results_in_dict_format.items(): 
        if results_in_dict_format[key]['Split'] == 'DEV': 
            total +=1 
            top100_predictions = results_in_dict_format[key]['generated_text_perplexity_context']
            # do the extra step here 
            correct_reference = results_in_dict_format[key]['reference']
            if type(correct_reference) != str: 
               correct_reference = ' '.join(correct_reference)


            # compute 
            correct_or_not = compute_overlap(top100_predictions, correct_reference, top_k=1)
            total_correct += correct_or_not 
    
    print(total_correct)
    print(total)
    print(total_correct/total)
    





main()
