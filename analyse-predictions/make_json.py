import json 
import pdb

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


# dict_keys(['coref', 'sents', 'filename', 'base_tokenized', 'id', 'revised_tokenized', 'revised_sentence', 
# 'insertion_phrases', 'Base_Sentence', 'Base_Nr', 'Revised_Nr', 'parsed_revised_sentence', 'Base_Article', 'Base_Article_Clean', 
# 'par', 'index_of_insertion', 'index_of_reference', 'bigram', 'stats', 'insertion', 'reference', 'reference-type', 'position-of-ref-in-insertion', 
# 'Split', 'insertion-type', 'language_model_text', 'revised_afer_insertion', 'revised_untill_insertion'])

PATH_TO_FILE_IN_RESULTS = "../data/references_for_lm.json"

with open(PATH_TO_FILE_IN_RESULTS, 'r') as json_in: 
     other_info = json.load(json_in)



merged_dict = {}
for key, _ in model1.items(): 
    merged_dict[key] = model1[key]
    merged_dict[key].update(model2[key])

    merged_dict[key]['revised_untill_insertion'] = other_info[key]['revised_untill_insertion'] 
    try: 
        revised_after_insertion = other_info[key]['revised_afer_insertion']
    except KeyError: 
        revised_after_insertion = other_info[key]['revised_after_insertion']
    
    merged_dict[key]['revised_after_insertion'] = revised_after_insertion
    merged_dict[key]['reference-type'] = other_info[key]['reference-type']


    if len(other_info[key]['insertion']) == 1: 
       merged_dict[key]['index_of_reference'] = other_info[key]['index_of_reference'][0]
    elif len(other_info[key]['insertion']) == 2: 
       if type(other_info[key]['index_of_reference']) == list:
           merged_dict[key]['index_of_reference'] = other_info[key]['index_of_reference'][0][0]
       else: 
           # when index of reference indicates the position of 
           merged_dict[key]['index_of_reference'] = other_info[key]['index_of_insertion'][0][other_info[key]['index_of_reference']] 
    else: 
       merged_dict[key]['index_of_reference'] = other_info[key]['beginindex']
    

with open('bestmodels_predictions.json', 'w') as json_out: 
     json.dump(merged_dict, json_out)
