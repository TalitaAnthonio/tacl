import json 

DIR = '../language-modeling/'

PATH1 = DIR + "GPT+Finetuning+P-perplexity100.json"
PATH2 = DIR + "GPTandFinetuning100.json"

def read_dict(path_to_dict): 
    with open(path_to_dict, 'r') as json_in: 
         data = json.load(json_in)
    return data 

model1 = read_dict(PATH1)
model2 = read_dict(PATH2)

# dict_keys(['GPT+Finetuning+P-perplexityPred', 'GPT+Finetuning+P-perplexityCorr'])
#dict_keys(['GPT+FinetuningCorrect', 'CorrectReference', 'LeftContext', 'GPTPred', 'GPTCorrect', 'key', 'GPT+FinetuningPred', 'RevisedSentence'])

merged_dict = {}
for key, _ in model1.items(): 
    merged_dict[key] = model1[key]
    merged_dict[key].update(model2[key])

with open('bestmodels_predictions.json', 'w') as json_out: 
     json.dump(merged_dict, json_out)