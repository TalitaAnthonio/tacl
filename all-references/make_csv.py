import pandas as pd 
import json 

with open("../overlap-trigrams/trigram_atomic_edits_implicit_pos_filtered.json", "r") as json_in: 
     trigrams = json.load(json_in)



def main():
    dataframe_dict = {"Base-Sentence": [], "Revised-Sentence": [], "Insertion": [], "reference": [], "reference-type": [], "position-of-ref-in-insertion": []}
    for key, _ in trigrams.items(): 
        
        dataframe_dict["Base-Sentence"].append(trigrams[key]['base_tokenized'])
        dataframe_dict["Revised-Sentence"].append(trigrams[key]['revised_tokenized'])
        dataframe_dict["Insertion"].append(trigrams[key]['insertion'])
        dataframe_dict["reference"].append(trigrams[key]['reference'])
        dataframe_dict["reference-type"].append(trigrams[key]['reference-type'])
        dataframe_dict["position-of-ref-in-insertion"].append(trigrams[key]['position-of-ref-in-insertion'])


    df = pd.DataFrame.from_dict(dataframe_dict)
    print(df)

main()