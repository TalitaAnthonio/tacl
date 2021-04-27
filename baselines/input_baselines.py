
import json 
import numpy as np 

path_to_file_with_corefs = "../analyse-predictions/run-coreference/most_frequent_reference_baseline.json"
path_to_file_with_predictions = '../analyse-predictions/bestmodels_predictions.json'

with open(path_to_file_with_predictions, 'r') as json_in: 
     data = json.load(json_in)

with open(path_to_file_with_corefs, "r") as json_in: 
     corefs = json.load(json_in)

def check_pos_of_filler(predictions, correct_filler, topk=10): 
    if correct_filler.lower() in predictions[:topk]: 
       return 1 
    else: 
        return 0 


def main(): 
    total = 0 
    
    t = []
    for key, _ in data.items(): 

        correct_reference = data[key]["CorrectReference"]
        most_frequent_filler = corefs[key]["most_frequent"]
        print(correct_reference)
        print(most_frequent_filler)

        if correct_reference.lower() == most_frequent_filler.lower(): 
           total +=1 
        
        t.append(corefs[key]["total_referring_expressions"])
    print(total)
    print(np.mean(t))
    print(np.std(t))
main()