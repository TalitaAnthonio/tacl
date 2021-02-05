import pandas as pd 
import json 

insertion_type = "trigram"
if insertion_type == "bigram": 
    path_to_file = "../data/bigram_atomic_edits_final.json"
    path_to_file_out = "bigram_edits.tsv"

elif insertion_type == 'trigram': 
    path_to_file = "../data/trigram_atomic_edits_coref_info_filtered.json"
    path_to_file_out = "trigram_edits.tsv"
else: 
    path_to_file = "./unigram_edits_final.json"
    path_to_file_out = "unigram_edits.tsv"



def read_file_with_filenames(path_to_file): 
    with open(path_to_file, "r") as file_in: 
         content = file_in.readlines()
         list_of_files = [filename.strip('\n') for filename in content]
         return list_of_files

KEYS_TO_DELETE = read_file_with_filenames("keys_to_delete.txt")


with open(path_to_file, "r") as json_in: 
     trigrams = json.load(json_in)


def main():
    dataframe_dict = {"Base-Sentence": [], "Revised-Sentence": [], "Insertion": [], "reference": [], "reference-type": [], "position-of-ref-in-insertion": [], "par": [], "id": []}
    for key, _ in trigrams.items(): 
        if key not in KEYS_TO_DELETE: 
            
            dataframe_dict["Base-Sentence"].append(trigrams[key]['base_tokenized'])
            if not insertion_type == 'unigram': 
                dataframe_dict["Revised-Sentence"].append(trigrams[key]['revised_tokenized'])
            else: 
                dataframe_dict["Revised-Sentence"].append(trigrams[key]['revised_sentence'])
            dataframe_dict["Insertion"].append(trigrams[key]['insertion'])
            dataframe_dict["id"].append(key)
            dataframe_dict["reference"].append(trigrams[key]['reference'])
            dataframe_dict["reference-type"].append(trigrams[key]['reference-type'])
            dataframe_dict["par"].append(trigrams[key]['par'])
            dataframe_dict["position-of-ref-in-insertion"].append(trigrams[key]['position-of-ref-in-insertion'])


    df = pd.DataFrame.from_dict(dataframe_dict)
    df.to_csv(path_to_file_out, index=False, sep='\t')

main()