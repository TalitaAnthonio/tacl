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




# add everything together 
coref_data.update(bigrams)
coref_data.update(trigrams)
print(len(coref_data.keys()))


remaining_corefs = "/Users/talita/Documents/PhD/corpora/rulebook_diffs/2019-09-23/boardgame_scripts/wikihow/data/unigrams/SingleInsertions_coreferenced.json"

with open(remaining_corefs, "r") as json_in: 
     other_unigrams = json.load(json_in)




def check_pos_of_filler(predictions, correct_filler, topk=10): 
    if correct_filler.lower() in predictions[:topk]: 
       return 1 
    else: 
        return 0 




def get_ref_per_sent(coref_info): 
    reference_index_list = {}
    for coref_id, _ in coref_info.items(): 
        for mention in coref_info[coref_id]["mentions"]: 
            sentence_index = mention["sentenceIndex"]
            begin_index = mention["beginIndex"]
            reference = mention["ref"]
            sent = mention["tokenized_sent"]


            if sentence_index not in reference_index_list.keys(): 
                reference_index_list[sentence_index] = []
                reference_index_list[sentence_index].append([reference, begin_index, sent])
            else: 
                reference_index_list[sentence_index].append([reference, begin_index, sent])
    return reference_index_list


def main(): 
    counter = 0 
    for key, _ in data.items():
        
        if "coref" in coref_data[key].keys(): 
            reference_index_list = get_ref_per_sent(coref_data[key]["coref"])
        else: 
            reference_index_list = get_ref_per_sent(other_unigrams[key]["coref"])


        sentence_indexes = sorted(reference_index_list.keys()) 
        sentence_indexes.reverse()
        print(sentence_indexes)
     
        for sentence_index in sentence_indexes:
            sorted_references = sorted(reference_index_list[sentence_index], key=lambda x:x[-2], reverse=True) 

            print(sentence_index, sorted_references)
            references_per_sentence = [" ".join(elem[0]) for elem in sorted_references]
            indexes = [elem[1] for elem in sorted_references]

            if data[key]["CorrectReference"] in references_per_sentence: 
               print(references_per_sentence, "in data", data[key]["CorrectReference"])
               break 
           
        print("======================")
        break 
main()