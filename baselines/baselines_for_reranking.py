import json 
import pdb 
from tools import * 
import numpy as np 


path_to_file = '../analyse-predictions/bestmodels_predictions.json'

with open(path_to_file, 'r') as json_in: 
     data = json.load(json_in)


def check_pos_of_filler(predictions, correct_filler, topk=10): 
    if correct_filler.lower() in predictions[:topk]: 
       return 1 
    else: 
        return 0 


def main(): 
    lens_of_nouns = []
    total_found = 0 
    total_found_other_ranking = 0 

    counter = 0 
    total_to_include_total = [] 
    number_of_nouns_total = []

    data_for_coreference = {}
    for key, _ in data.items(): 
        counter +=1 
        print("=========================={0}".format(counter))

        total_to_include = 0 
        number_of_nouns = 0 

        best_model_pred = [elem.strip().lower() for elem in data[key]['GPT+Finetuning+P-perplexityPred']]
        finetuned_only_model_predictions = [elem.strip() for elem in data[key]['GPT+FinetuningPred']]

        # check if we can increase the position based on saliency 

        context = data[key]['LeftContext']
        context = tokenize(context, ngrams=data[key]['reference-type'])

        #tagged = add_pos_tagging_to_predictions(finetuned_only_model_predictions)
        predictions = Predictions(finetuned_only_model_predictions, return_value="all")
        finetuned_only_model_predictions = predictions.token_predictions
        tagged = predictions.tagged_predictions
        #noun_fillers = predictions.filtered_set
        noun_fillers = predictions.filtered_set
        
        print(noun_fillers)

        bow_nouns = make_bow(context, noun_fillers)
        #sorted_d: sort the bow 
        sorted_d = dict(sorted(bow_nouns.items(), key=lambda item: item[1], reverse=True))
        
        #print(finetuned_only_model_predictions)
        print(sorted_d)
        print("correct reference {0}".format(data[key]['CorrectReference']))
        print('=====================================')
        lens_of_nouns.append(len(sorted_d))

        # check if the correct filler is among them. 
        occurs_or_not = check_pos_of_filler(list(sorted_d.keys()), data[key]['CorrectReference'])
        total_found_other_ranking += occurs_or_not

    
    print(total_found_other_ranking)
    print(np.mean(lens_of_nouns))


main()