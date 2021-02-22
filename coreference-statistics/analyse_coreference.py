import json 
import pdb 
from objects import CorefChain
from collections import Counter 
import numpy as np 

PATH_TO_BIGRAMS = "../data/bigram_atomic_edits_coref.json"
PATH_TO_TRIGRAMS = "../data/trigram_atomic_edits_coref_info_filtered.json"
PATH_TO_UNIGRAMS = "../data/unigram_atomic_edits_coref.json" 
KEYS_TO_EXCLUDE = ["Answer_Common_Atheists_Questions_About_Christianity23", 
"Celebrate_Thanksgiving62", 
"Dress_in_American_1940s_Fashion12",
"Know_That_You_Are_Going_to_Heaven_As_a_Christian47"]

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
    # how often the entities are mentioned 
    chain_length = []
    for key, _ in data.items(): 
        if key in KEYS_TO_EXCLUDE: 
           print(data[key]['reference-type'], data[key]['reference'], data[key]['insertion'])

    """
    for key, _ in data.items(): 
        if key not in KEYS_TO_EXCLUDE: 
            corefchain_object = CorefChain(data[key]['CorefChain'])
            distances.append(corefchain_object.distance_to_reference)
            # minus 1 to exclude the implicit reference itself 
            chain_length.append(corefchain_object.chainlength-1)

    
    print("COREF DISTANCE FREQUENCIES .....")
    freq_dict = build_freq_dict(distances)
    print(freq_dict)
    total = np.sum([value for key, value in  dict(freq_dict).items()])
    calculate_percentage(freq_dict, total)
    print(total)

    print("chain length")
    freq_dict_chains = build_freq_dict(chain_length)
    print(freq_dict_chains)
    # divide by the total number of 
    calculate_percentage(freq_dict_chains, total)
    print(np.sum([value for key, value in  dict(freq_dict_chains).items()]))
    """


main()