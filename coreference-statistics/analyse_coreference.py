import json 
import pdb 

PATH_TO_BIGRAMS = "../data/bigram_atomic_edits_coref.json" 
PATH_TO_TRIGRAMS = "../data/trigram_atomic_edits_coref_info.json" 
PATH_TO_UNIGRAMS = "../data/unigram_atomic_edits_coref.json" 

def read_file(path_to_file): 
    with open(path_to_file, 'r') as json_in: 
         data = json.load(json_in)
    return data 

def main(): 
    data = read_file(PATH_TO_BIGRAMS)

    counter = 0 
    for key, _ in data.items(): 
        if len(data[key]['CorefChain']) == 1: 
           print(data[key]['CorefChain'])
           pdb.set_trace()
           print(data[key]['coref'])
           counter +=1 
    print(counter)
        #print(data[key]['CorefChain'])
        #print('\n')
        #print(data[key]['coref']) 
        #print("=====================================")

main()