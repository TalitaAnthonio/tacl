import json 
import pdb 
from objects import CorefChain
from collections import Counter 
import numpy as np 

PATH_TO_BIGRAMS = "../data/bigram_atomic_edits_coref.json" 
PATH_TO_TRIGRAMS = "../data/trigram_atomic_edits_coref_info_filtered.json"
PATH_TO_UNIGRAMS = "../data/unigram_atomic_edits_coref.json" 

def read_file(path_to_file): 
    with open(path_to_file, 'r') as json_in: 
         data = json.load(json_in)
    return data 

def build_freq_dict(list_with_frequencies): 
    freq_dict = Counter()
    for elem in list_with_frequencies: 
        freq_dict[elem] +=1 
    return freq_dict

def main(): 
    data = read_file(PATH_TO_TRIGRAMS)
    unigrams = read_file(PATH_TO_UNIGRAMS)
    print(len(data))

    counter = 0 
    distances = []
    data.update(unigrams)
    for key, _ in data.items(): 
        corefchain_object = CorefChain(data[key]['CorefChain'])
        distances.append(corefchain_object.distance_to_reference)
    
    freq_dict = build_freq_dict(distances)
    print(freq_dict)
    print(np.sum([value for key, value in  dict(freq_dict).items()])) 
    

main()