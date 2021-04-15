import json 
import pdb 

path_to_file = 'bestmodels_predictions.json'


with open(path_to_file, 'r') as json_in: 
     data = json.load(json_in)

for key, _ in data.items(): 
    best_model_pred = [elem.strip() for elem in data[key]['GPT+Finetuning+P-perplexityPred']]
    second_best_model_pred = [elem.strip() for elem in data[key]['GPT+FinetuningPred']]
    context = data[key]['LeftContext']
    pdb.set_trace()
    break 
