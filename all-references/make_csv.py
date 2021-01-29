import pandas as pd 
import json 

insertion_type = "bigram"


if insertion_type == "bigram": 
    path_to_file = "../bigrams/bigram_atomic_edits_implicit_pos_filtered.json"
    path_to_file_out = "bigrams_filtered.tsv"

elif insertion_type == 'trigram': 
    path_to_file = "../overlap-trigrams/trigram_atomic_edits_implicit_pos_filtered.json"
    path_to_file_out = "trigrams_filtered.tsv"
else: 
    path_to_file = "unigram_edits_implicit.json"
    path_to_file_out = "unigrams.tsv"


with open(path_to_file, "r") as json_in: 
     trigrams = json.load(json_in)



def main():
    dataframe_dict = {"Base-Sentence": [], "Revised-Sentence": [], "Insertion": [], "reference": [], "reference-type": [], "position-of-ref-in-insertion": []}
    for key, _ in trigrams.items(): 
        print(trigrams[key].keys())
        
        dataframe_dict["Base-Sentence"].append(trigrams[key]['base_tokenized'])
        if not insertion_type == 'unigram': 
            dataframe_dict["Revised-Sentence"].append(trigrams[key]['revised_tokenized'])
        else: 
            dataframe_dict["Revised-Sentence"].append(trigrams[key]['revised_sentence'])
        dataframe_dict["Insertion"].append(trigrams[key]['insertion'])
        dataframe_dict["reference"].append(trigrams[key]['reference'])
        dataframe_dict["reference-type"].append(trigrams[key]['reference-type'])
        dataframe_dict["position-of-ref-in-insertion"].append(trigrams[key]['position-of-ref-in-insertion'])


    df = pd.DataFrame.from_dict(dataframe_dict)
    df.to_csv(path_to_file_out, index=False, sep='\t')

main()