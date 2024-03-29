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

    counter = 0 
    total_to_include_total = [] 
    number_of_nouns_total = []

    data_for_coreference = {}
    for key, _ in data.items(): 

        total_to_include = 0 
        number_of_nouns = 0 

        best_model_pred = [elem.strip().lower() for elem in data[key]['GPT+Finetuning+P-perplexityPred']]
        finetuned_only_model_predictions = [elem.strip() for elem in data[key]['GPT+FinetuningPred']]

        # check if we can increase the position based on saliency 

        context = data[key]['LeftContext']
        context = tokenize(context, ngrams=data[key]['reference-type'])

        tagged = add_pos_tagging_to_predictions(finetuned_only_model_predictions)
        noun_fillers = []
        other_fillers = []
        for filler, post_tags_from_filler in zip(finetuned_only_model_predictions, tagged): 
            if 'NN' in post_tags_from_filler or 'PRP' in post_tags_from_filler or 'PRP$' in post_tags_from_filler: 
                noun_fillers.append(filler)
            else: 
                other_fillers.append(filler)

        
        bow_nouns = check_if_filler_occurs(context, noun_fillers)
        # sorted_d: sort the bow 
        sorted_d = dict(sorted(bow_nouns.items(), key=lambda item: item[1], reverse=True))
        
        # check if the correct filler is among them. 
        occurs_or_not = check_pos_of_filler(list(sorted_d.keys()), data[key]['CorrectReference'])
        total_found_other_ranking += occurs_or_not
    
    print(total_found_other_ranking)


        
        
        # do something with  POS TAGS --------------
    '''
        tagged = add_pos_tagging_to_predictions(finetuned_only_model_predictions)
        # collect the fillers to include in a list 
        fillers_to_include_plus_sentence = []
        for filler, post_tags_from_filler in zip(finetuned_only_model_predictions, tagged): 
            print(filler, post_tags_from_filler, filtering_patterns(post_tags_from_filler))
            if filtering_patterns(post_tags_from_filler) == "include": 
               total_to_include +=1 


            if 'NN' in post_tags_from_filler or 'PRP' in post_tags_from_filler or 'PRP$' in post_tags_from_filler: 
                number_of_nouns +=1 
 

        # add necessary elements for data for coreference 


        print("---------------------------------------------")
        total_to_include_total.append(total_to_include) 
        number_of_nouns_total.append(number_of_nouns)
        counter +=1

    # compute statistics 
    print("--------------number total ------------------------------")
    print(np.mean(total_to_include_total))
    print(np.sum(total_to_include_total))
    print("total in data", counter)

    print("--------------number total ------------------------------")
    print(np.sum(number_of_nouns_total))
    print(np.mean(number_of_nouns_total))
    print(np.std(number_of_nouns_total))

    '''



main()

