import json 
from collections import Counter
import pdb 
import pandas as pd 
import numpy as np 

np.random.seed(1)
  
def most_frequent(List):
    occurence_count = Counter(List)
    return occurence_count.most_common(1)[0][0]


path_to_file = "../../data/references_for_lm.json"

path_to_other = "/Users/talita/Documents/PhD/corpora/rulebook_diffs/2019-09-23/boardgame_scripts/wikihow/data/unigrams/SingleInsertions_coreferenced.json"


coref_chain_info = "../../data/unigram_atomic_edits_coref.json"
coref_chain_info_bigrams_path = "../../data/bigram_atomic_edits_coref.json"
coref_chain_info_trigrams_path = "../../data/trigram_atomic_edits_coref_info.json"


with open(coref_chain_info_bigrams_path, 'r') as json_in: 
     coref_bigrams_info = json.load(json_in)


with open(coref_chain_info_trigrams_path, 'r') as json_in: 
     coref_trigrams_info = json.load(json_in)


with open(path_to_file, 'r') as json_in: 
     data = json.load(json_in)


with open(path_to_other, 'r') as json_in: 
     coref_info_unigrams = json.load(json_in)

with open(coref_chain_info, 'r') as json_in: 
     second_part = json.load(json_in)





def mark_instances(sents, coref_info, correct_reference): 
    marked_sents = {}
    references = [' '.join(elem['ref']) for elem in coref_info]
    max_sent_index = np.max([elem['sentenceIndex'] for elem in coref_info])
    for elem in coref_info: 

        sentence_with_coref = sents[elem["sentenceIndex"]]
        begin_index = elem["beginIndex"]
        end_index = elem["endIndex"]
 
        if (' '.join(elem["ref"]) == correct_reference) and (elem["sentenceIndex"] == max_sent_index): 
            assert type(correct_reference) == str 
            first_tag = "*"
            second_tag = "*"
        else: 
            first_tag = "_"
            second_tag = "_"


        if len(elem["ref"]) == 1: 
            sentence_with_coref[begin_index] = first_tag + sentence_with_coref[begin_index] + second_tag
        
        else: 
            sentence_with_coref[begin_index] = first_tag +  sentence_with_coref[begin_index] 
            sentence_with_coref[end_index-1] = sentence_with_coref[end_index-1] + second_tag

        marked_sents[elem['sentenceIndex']] = sentence_with_coref
    
    new_sents = []
    for index, sent in enumerate(sents,0): 
        if index in marked_sents.keys(): 
            sent = marked_sents[index]
    
        new_sents.append(sent)


    
    return new_sents, references

#Enjoy_Life29


def main(): 
    d = {"last_sentence_in_context": [], "main_refferring_expression": [], "all_references_to_entity": [], "context": [], "revised_sentence": [], "id": [], "original_sentence": []}
    counter = 0 
    
    dev_set = dict((key,value) for key, value in data.items() if data[key]["Split"] == "DEV")    
    value_to_return = 0 
    for key, _ in dev_set.items():
        pdb.set_trace()
      
        if "coref" not in dev_set[key].keys(): 
            coref_info = second_part[key]["CorefChain"]
            sents = coref_info_unigrams[key]["sents"]
            new_sents, references = mark_instances(sents, coref_info, " ".join(dev_set[key]["reference"]))
            new_sents_formatted = ' '.join(' '.join(sent)+'\n' for sent in new_sents)

            d["id"].append(key)
            d["last_sentence_in_context"].append(' '.join(new_sents[-1]))
            d["revised_sentence"].append(dev_set[key]["revised_sentence"])
            d["main_refferring_expression"].append(" ".join(dev_set[key]["reference"]))
            d["context"].append(new_sents_formatted)
            d["all_references_to_entity"].append(references)

        else: 
            if len(dev_set[key]["insertion"])  == 2: 
                coref_info = coref_bigrams_info[key]["CorefChain"]
                sents = dev_set[key]["sents"]
                references =  [' '.join(elem['ref']) for elem in coref_info]

                if " ".join(dev_set[key]["reference"]) not in references: 
                    #print("===========================================")
                    #print(" ".join(dev_set[key]["reference"]), references)
                    for chain_id, _ in dev_set[key]["coref"].items(): 
                        i_references = [elem["ref"] for elem in dev_set[key]["coref"][chain_id]["mentions"]]
                        if dev_set[key]["reference"] in i_references: 
                            coref_info = dev_set[key]["coref"][chain_id]["mentions"]
                            break 
                new_sents, references  = mark_instances(sents, coref_info, " ".join(dev_set[key]["reference"]))
                new_sents_formatted = ' '.join(' '.join(sent)+'\n' for sent in new_sents)

                d["id"].append(key)
                d["last_sentence_in_context"].append(' '.join(new_sents[-1]))
                d["revised_sentence"].append(dev_set[key]["revised_sentence"])
                d["main_refferring_expression"].append(" ".join(dev_set[key]["reference"]))
                d["context"].append(new_sents_formatted)
                d["all_references_to_entity"].append(references)

    
                        
                   
            else: 
                coref_info = coref_trigrams_info[key]["CorefChain"]
                sents = dev_set[key]["sents"]
                if type(dev_set[key]["reference"]) == str: 
                   reference = dev_set[key]["reference"]
                else: 
                    reference = " ".join(dev_set[key]["reference"])
                new_sents, references = mark_instances(sents, coref_info, reference)
                new_sents_formatted = ' '.join(' '.join(sent)+'\n' for sent in new_sents)

            
        
                d["id"].append(key)
                d["last_sentence_in_context"].append(' '.join(new_sents[-1]))
                d["revised_sentence"].append(dev_set[key]["revised_sentence"])
                d["main_refferring_expression"].append(reference)
                d["context"].append(new_sents_formatted)
                d["all_references_to_entity"].append(references)
    
    #del d["revised_sentence"]
    df = pd.DataFrame.from_dict(d)
    df = df.sample(n=200)
    print(df)
    df.to_csv("dev_split.tsv", sep="\t", index=False)


main()

