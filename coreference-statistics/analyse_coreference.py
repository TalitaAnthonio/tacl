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

def calculate_percentage(freq_dict, total): 
    freq_dict = dict(freq_dict)
    new_d = {}
    for key, _ in freq_dict.items(): 
        new_d[key] = freq_dict[key]/total 
    sorted_d = sorted((distance, freq) for distance, freq in new_d.items())
    print(sorted_d)

def main(): 
    data = read_file(PATH_TO_TRIGRAMS)
    unigrams = read_file(PATH_TO_UNIGRAMS)
    bigrams = read_file(PATH_TO_BIGRAMS)
    print(len(data))
    print(len(unigrams))
    print(len(bigrams))

    counter = 0 
    distances = []
    data.update(unigrams)
    data.update(bigrams)
    for key, _ in data.items(): 
        corefchain_object = CorefChain(data[key]['CorefChain'])
        distances.append(corefchain_object.distance_to_reference)
    
    freq_dict = build_freq_dict(distances)
    print(freq_dict)
    total = np.sum([value for key, value in  dict(freq_dict).items()])
    calculate_percentage(freq_dict, total)
    print(total)


main()