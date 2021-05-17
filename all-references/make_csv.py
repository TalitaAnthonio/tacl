import pandas as pd 
import json 

insertion_type = "trigram"

if insertion_type == "bigram": 
    path_to_file = "../data/bigram_atomic_edits_final.json"
    path_to_file_out = "bigram_edits_new.tsv"

elif insertion_type == 'trigram': 
    path_to_file = "../data/trigram_atomic_edits_coref_info_filtered.json"
    path_to_file_out = "trigram_edits.tsv"
else: 
    path_to_file = "./unigram_edits_final.json"
    path_to_file_out = "unigram_edits_new.tsv"



def read_file_with_filenames(path_to_file): 
    with open(path_to_file, "r") as file_in: 
         content = file_in.readlines()
         list_of_files = [filename.strip('\n') for filename in content]
         return list_of_files

KEYS_TO_DELETE = read_file_with_filenames("keys_to_delete.txt")


def remove_timestamps(text): 
    text = text.split('\n')
    formatted_text = ""
    for sentence in text: 
        if not "Timestamp" in sentence:
           sentence = sentence + '\n'
           formatted_text += sentence
    return formatted_text.strip('\n').strip('\n')

with open(path_to_file, "r") as json_in: 
     trigrams = json.load(json_in)


with open("keys_to_include.txt", "r") as file_in: 
     keys_to_inlude_file = file_in.readlines()

keys_to_include = [key.strip() for key in keys_to_inlude_file]

def main():
    #dataframe_dict = {"Base-Sentence": [], "Revised-Sentence": [], "Insertion": [], "reference": [], "reference-type": [], "position-of-ref-in-insertion": [], "par": [], "id": []}
    dataframe_dict = {"ArticleName": [], "RevisedSentence": [], "Reference": [], "Context": []}
    
    for key, _ in trigrams.items(): 
        #if key not in KEYS_TO_DELETE: 
        if key in keys_to_include: 
            #dataframe_dict["Insertion"].append(trigrams[key]['insertion'])
            #dataframe_dict["id"].append(key)
            #dataframe_dict["reference"].append(trigrams[key]['reference'])
            #dataframe_dict["reference-type"].append(trigrams[key]['reference-type'])
            #dataframe_dict["par"].append(trigrams[key]['par'])
            #dataframe_dict["position-of-ref-in-insertion"].append(trigrams[key]['position-of-ref-in-insertion'])
            dataframe_dict["ArticleName"].append(trigrams[key]["filename"])
            dataframe_dict["RevisedSentence"].append(trigrams[key]["revised_sentence"])
            dataframe_dict["Reference"].append(" ".join(trigrams[key]["reference"]))
            dataframe_dict["Context"].append(remove_timestamps(trigrams[key]["par"]))

    df = pd.DataFrame.from_dict(dataframe_dict)
    df.to_csv(path_to_file_out, index=False, sep='\t')

main()