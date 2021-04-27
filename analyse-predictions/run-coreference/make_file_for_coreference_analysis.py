import json 
from collections import Counter
import pdb 
  
def most_frequent(List):
    occurence_count = Counter(List)
    return occurence_count.most_common(1)[0][0]


path_to_file = "../../data/references_for_lm.json"

path_to_other = "/Users/talita/Documents/PhD/corpora/rulebook_diffs/2019-09-23/boardgame_scripts/wikihow/data/unigrams/SingleInsertions_coreferenced.json"

coref_chain_info = "../../data/unigram_atomic_edits_coref.json"

coref_chain_info_bigrams = "../../data/bigram_atomic_edits_coref.json"


with open(coref_chain_info_bigrams, 'r') as json_in: 
     coref_bigrams = json.load(json_in)

with open(path_to_file, 'r') as json_in: 
     data = json.load(json_in)


with open(path_to_other, 'r') as json_in: 
     coref_info_unigrams = json.load(json_in)

with open(coref_chain_info, 'r') as json_in: 
     second_part = json.load(json_in)


def main(): 
    d = {}
    counter = 0 
    for key, _ in data.items(): 
        #corefs = data[key]['coref']
        #except KeyError: 
        #    pdb.set_trace()
        total_referring_expressions = 0 

        #if "coref" in data[key].keys(): 
        #    corefs = data[key]['coref']

        if "coref" not in data[key].keys(): 
            #corefs = second_part[key]['coref']
            sents = coref_info_unigrams[key]["sents"]
            for sent in sents: 
                print(sent )
            corefs = second_part[key].keys()
            coref_info = second_part[key]["CorefChain"]


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

            print("new sents")
            for sent in new_sents: 
                print(sent)
            
            print('references', [' '.join(elem['ref']) for elem in coref_info])
            print(data[key]["revised_sentence"])
            print(data[key]["insertion"])
            print("============================")
        

main()
