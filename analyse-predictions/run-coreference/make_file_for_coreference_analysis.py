import json 
from collections import Counter
import pdb 
import pandas as pd 
  
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





def mark_instances(sents, coref_info): 
    for sent in sents: 
            print(sent)
    


    marked_sents = {}
    for elem in coref_info: 
        print(elem)

        sentence_with_coref = sents[elem["sentenceIndex"]]
        print("sentence with coref", sentence_with_coref)
        begin_index = elem["beginIndex"]
        end_index = elem["endIndex"]

        if len(elem["ref"]) == 1: 
            sentence_with_coref[begin_index] = "<REFERENCE>" + " " + sentence_with_coref[begin_index] + " " + "</REFERENCE>"
        
        else: 
            sentence_with_coref[begin_index] = "<REFERENCE>" + " " +  sentence_with_coref[begin_index] 
            sentence_with_coref[end_index-1] = sentence_with_coref[end_index-1] + " "+ "</REFERENCE>"

        marked_sents[elem['sentenceIndex']] = sentence_with_coref
    
    new_sents = []
    for index, sent in enumerate(sents,0): 
        if index in marked_sents.keys(): 
            sent = marked_sents[index]
    
        new_sents.append(sent)

    references =  [' '.join(elem['ref']) for elem in coref_info]

    
    return new_sents, references


def main(): 
    d = {"revised_sentence": [], "reference": [], "chain": [], "references": []}
    counter = 0 

    for key, _ in data.items():     
        if "coref" not in data[key].keys(): 
            coref_info = second_part[key]["CorefChain"]
            sents = coref_info_unigrams[key]["sents"]
            new_sents, references = mark_instances(sents, coref_info)
        else: 
            if len(data[key]["insertion"])  == 2: 
                coref_info = coref_bigrams_info[key]["CorefChain"]
                sents = data[key]["sents"]
                new_sents, references = mark_instances(sents, coref_info)

                print(data[key]["revised_sentence"])
                print(data[key]["insertion"])
                print("============================")
                new_sents = [' '.join(sent) for sent in new_sents]
                print(new_sents)

            
               
           
            
            else: 
                coref_info = coref_trigrams_info[key]["CorefChain"]
                sents = data[key]["sents"]
                new_sents, references = mark_instances(sents, coref_info)
                new_sents = [' '.join(sent) for sent in new_sents]
                print(new_sents)

                print(data[key]["revised_sentence"])
                print(data[key]["insertion"])
                print("============================")
            

        d["revised_sentence"].append(data[key]["revised_sentence"])
        d["reference"].append(data[key]["reference"])
        d["chain"].append(sents)
        d["references"].append(references)
        
    
    df = pd.DataFrame.from_dict(d)
    df.to_csv("test.tsv", sep="\t")

main()
