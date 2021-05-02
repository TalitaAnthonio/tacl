import json 
from collections import OrderedDict
import pdb 

path_to_file_with_predictions = '../analyse-predictions/bestmodels_predictions.json'
coref_chain_info_unigrams_path = "../data/unigram_atomic_edits_coref.json"
coref_chain_info_bigrams_path = "../data/bigram_atomic_edits_coref.json"
coref_chain_info_trigrams_path = "../data/trigram_atomic_edits_coref_info.json"



with open(path_to_file_with_predictions, 'r') as json_in: 
     data = json.load(json_in)



with open(coref_chain_info_unigrams_path, 'r') as json_in: 
     coref_data = json.load(json_in)


with open(coref_chain_info_bigrams_path, 'r') as json_in: 
     bigrams = json.load(json_in)


with open(coref_chain_info_trigrams_path, 'r') as json_in: 
     trigrams = json.load(json_in)

with open("../data/references_for_lm.json", "r") as json_in: 
     references = json.load(json_in)



# add everything together 

all_data_keys = references.keys()

coref_data.update(bigrams)
coref_data.update(trigrams)
print(len(coref_data.keys()))


remaining_corefs = "/Users/talita/Documents/PhD/corpora/rulebook_diffs/2019-09-23/boardgame_scripts/wikihow/data/unigrams/SingleInsertions_coreferenced.json"

with open(remaining_corefs, "r") as json_in: 
     other_unigrams = json.load(json_in)

with open("dict_with_correct_references.json", "r") as json_in: 
     corrected_references = json.load(json_in)


def get_ref_per_sent(coref_info): 
    reference_index_list = {}
    for mention in coref_info: 
        sentence_index = mention["sentenceIndex"]
        begin_index = mention["beginIndex"]
        reference = mention["ref"]
        reference_info = [reference, begin_index, sentence_index]

        if sentence_index not in reference_index_list.keys(): 
            reference_index_list[sentence_index] = []
            reference_index_list[sentence_index].append([reference, begin_index])
        else: 
            reference_index_list[sentence_index].append([reference, begin_index])
    return reference_index_list



counter = 0 
for key in all_data_keys: 
    if key not in corrected_references.keys(): 
        indexes = [mention["beginIndex"] for mention in coref_data[key]["CorefChain"]]
        sent_refs = get_ref_per_sent(coref_data[key]["CorefChain"])
        if len(sent_refs.keys()) == 1: 
            try: 
                if coref_data[key]["index_of_reference"] in indexes: 
                    if indexes.index(coref_data[key]["index_of_reference"]) == len(indexes)-1:
                        continue
            except KeyError: 
     
                for sentnr, _ in sent_refs.items(): 
                    #sent_refs = sorted(sent_refs[sentnr], key=lambda x:x[-1], reverse=True) 
                    references_blabla = [" ".join(elem[0]) for elem in sorted(sent_refs[sentnr], key=lambda x:x[-1], reverse=True)]
                    if references_blabla.index(" ".join(coref_data[key]["reference"])) == len(indexes)-1: 
                       print("correct reference", coref_data[key]["reference"])
                       print(sent_refs)
                       print(key)
                       print("============================")
                       counter +=1 
            
print(counter)