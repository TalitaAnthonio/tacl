import json 
import pandas as pd 
import pdb

PATH1 = "GPT+Finetuning+P-perplexity100.json"
PATH2 = "GPT+Finetuning+S-perplexity100.json"
PATH3 = "GPT+S-perplexity100.json"
PATH4 = "GPTandFinetuning100.json"
PATH5 = "GPT+P-perplexitytop100.json"

def read_dict(path_to_dict): 
    with open(path_to_dict, 'r') as json_in: 
         data = json.load(json_in)
    return data 



def make_dict_for_df(dict_with_results): 
    # GPT+Finetuning+P-perplexityPred
    #d = {'GPT+FinetuningCorrect': [], 'CorrectReference': [], 'LeftContext': [], 'GPTPred': [], 'GPTCorrect': [], 'key': [], 'GPT+FinetuningPred': [], 'GPT+Finetuning+P-perplexityPred': [], 'GPT+Finetuning+P-perplexityCorr': [], 'GPT+Finetuning+S-perplexityPred': [], 'GPT+Finetuning+S-perplexityCorr': [], 'GPT+S-perplexityPred': [], 'GPT+S-perplexityCorr': []}
    d =  {'key': [], 'CorrectReference': [], 'LeftContext': [], 'RevisedSentence': [], 'GPTPred': [], 'GPT+S-perplexityPred': [], "GPT+P-perplexityPred": [],  'GPT+FinetuningPred': [], 'GPT+Finetuning+P-perplexityPred': [], 'GPT+Finetuning+S-perplexityPred': []}
    
    for revision_id, _  in dict_with_results.items(): 
        for key in d.keys():
            d[key].append(dict_with_results[revision_id][key])

    return d 




def main(): 
    model1 = read_dict(PATH1)
    model2 = read_dict(PATH2)
    model3 = read_dict(PATH3)
    model4 = read_dict(PATH5)
    base_model = read_dict(PATH4)

    updated = {}
    # make the first dict 
    for key, _ in base_model.items(): 
        updated[key] = base_model[key]

   
        updated[key].update(model1[key])
        updated[key].update(model2[key])
        updated[key].update(model3[key])
        updated[key].update(model4[key])


    df_dict = make_dict_for_df(updated)

    
    df = pd.DataFrame.from_dict(df_dict)


    print(df)
    print(df.columns)
    df['GPT+S-perplexityPred'] = df['GPT+S-perplexityPred'].apply(lambda x:x[0:10])
    df['GPT+Finetuning+S-perplexityPred'] = df['GPT+Finetuning+S-perplexityPred'].apply(lambda x:x[0:10])
    df['GPT+Finetuning+P-perplexityPred'] = df['GPT+Finetuning+P-perplexityPred'].apply(lambda x:x[0:10])
    df['GPTPred'] = df['GPTPred'].apply(lambda x:x[0:10])
    df['GPT+P-perplexityPred'] = df['GPT+P-perplexityPred'].apply(lambda x:x[0:10])
    df['GPT+FinetuningPred'] = df['GPT+FinetuningPred'].apply(lambda x:x[0:10])
    print(df)
    df.to_csv("test100.csv", sep='\t', index=False)


main()