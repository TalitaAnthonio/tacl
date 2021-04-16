import json 
import pdb 
from tools import * 
import numpy as np 
from filters import * 


path_to_file = 'bestmodels_predictions.json'


with open(path_to_file, 'r') as json_in: 
     data = json.load(json_in)


def check_pos_of_filler(predictions, correct_filler, topk=10): 
    if correct_filler.lower() in predictions[:topk]: 
       return 1 
    else: 
        return 0 




def main(): 
    total_found = 0 
    total_found_other_ranking = 0 
    index_errors = 0 
    counter = 0 
    for key, _ in data.items(): 
        best_model_pred = [elem.strip().lower() for elem in data[key]['GPT+Finetuning+P-perplexityPred']]
        second_best_model_pred = [elem.strip() for elem in data[key]['GPT+FinetuningPred']]
        context = data[key]['LeftContext']
        # check what the current position is 


        occurs_in_pred = check_pos_of_filler(best_model_pred, data[key]['CorrectReference'])
        total_found += occurs_in_pred

        best_model_pred = second_best_model_pred


        # check if we can increase the position based on saliency 
        #context = tokenize(context, ngrams=data[key]['reference-type'])
        d = check_if_filler_occurs(context, best_model_pred)
        sorted_d = dict(sorted(d.items(), key=lambda item: item[1], reverse=True))
        occurs_or_not = check_pos_of_filler(list(sorted_d.keys()), data[key]['CorrectReference'])
        total_found_other_ranking += occurs_or_not
        
        # do something with  POS TAGS --------------
 
        tagged = add_pos_tagging_to_predictions(second_best_model_pred)

        for filler, post_tags_from_filler in zip(second_best_model_pred, tagged): 
            print(filler, post_tags_from_filler, filtering_patterns(post_tags_from_filler)) 


        print("---------------------------------------------")

        counter +=1 
        if counter == 10: 
            break 


        

    
    print(total_found)
    print(total_found_other_ranking)





main()

