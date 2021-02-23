import json 
import pandas as pd 

PATH1 = "GPT+finetuning+P-perplexity.json"
PATH2 = "GPT+finetuning+S-perplexity.json"
PATH3 = "GPT+S-perplexity.json"
PATH4 = "GPTandFinetuning.json"


def read_dict(path_to_dict): 
    with open(path_to_dict, 'r') as json_in: 
         data = json.load(json_in)
    return data 



def make_dict_for_df(dict_with_results): 
    d = {'GPT+FinetuningCorrect': [], 'CorrectReference': [], 'LeftContext': [], 'GPTPred': [], 'GPTCorrect': [], 'key': [], 'GPT+FinetuningPred': [], 'GPT+finetuning+P-perplexityPred': [], 'GPT+finetuning+P-perplexityCorr': [], 'GPT+Finetuning+S-perplexityPred': [], 'GPT+Finetuning+S-perplexityCorr': [], 'GPT+S-perplexityPred': [], 'GPT+S-perplexityCorr': []}
    for revision_id, _  in dict_with_results.items(): 
        for key in dict_with_results[revision_id].keys():
            d[key].append(dict_with_results[revision_id][key])

    return d 




def main(): 
    model1 = read_dict(PATH1)
    model2 = read_dict(PATH2)
    model3 = read_dict(PATH3)
    base_model = read_dict(PATH4)

    updated = {}
    # make the first dict 
    for key, _ in base_model.items(): 
        updated[key] = base_model[key]

        # update using the other models 

        updated[key].update(model1[key])
        updated[key].update(model2[key])
        updated[key].update(model3[key])


    print(updated[key].keys())
    df_dict = make_dict_for_df(updated)

    
    df = pd.DataFrame.from_dict(df_dict)
    df.to_csv("test.csv", sep='\t', index=False)


main()