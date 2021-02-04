import json 
from collections import Counter
import pdb 

DEV_FILES_PATH = "/Users/talita/Documents/PhD/corpora/rulebook_diffs/2019-09-23/boardgame_scripts/wikihow/language-models/dev_files.txt"
TRAIN_FILES_PATH = "/Users/talita/Documents/PhD/corpora/rulebook_diffs/2019-09-23/boardgame_scripts/wikihow/language-models/train_files.txt"
TEST_FILES_PATH = "/Users/talita/Documents/PhD/corpora/rulebook_diffs/2019-09-23/boardgame_scripts/wikihow/language-models/test_files.txt"

def read_file_with_filenames(path_to_file): 
    with open(path_to_file, "r") as file_in: 
         content = file_in.readlines()
         list_of_files = [filename.strip('\n') for filename in content]
         return list_of_files


DEV_FILES = read_file_with_filenames(DEV_FILES_PATH)
TEST_FILES = read_file_with_filenames(TEST_FILES_PATH)
TRAIN_FILES = read_file_with_filenames(TRAIN_FILES_PATH)
KEYS_TO_DELETE = read_file_with_filenames("keys_to_delete.txt")


def check_splits(filename):
    if filename in DEV_FILES: 
       return {'Split': 'DEV'}
    elif filename in TEST_FILES: 
        return {'Split': 'TEST'} 
    else: 
        return {'Split': 'TRAIN'}

def add_split_info(path_to_file): 
    with open(path_to_file, "r") as json_in: 
         data = json.load(json_in)
        
    
    data_with_filename_info = {}
    for key, _ in data.items(): 
        data_with_filename_info[key] = data[key]
        split_info = check_splits(data[key]['filename'])
        data_with_filename_info[key].update(split_info)
        # add also the info about the type of insertion. 
        data_with_filename_info[key].update({'insertion-type': len(data[key]['insertion'])})
        
    
    return data_with_filename_info

def delete_cases(complete_set): 
    filtered = {}
    for key, _ in complete_set.items(): 
        if key not in KEYS_TO_DELETE: 
           filtered[key] = complete_set[key]
    return filtered

def main(): 

    path_to_bigram_file = "../bigrams/bigram_edits_final.json"
    path_to_trigram_file = "../data/trigram_atomic_edits_implicit_filtered.json"
    path_to_unigram_file = "unigram_edits_final.json"

    data = add_split_info(path_to_bigram_file)
    trigrams = add_split_info(path_to_trigram_file) 
    unigrams = add_split_info(path_to_unigram_file)
    
    data.update(trigrams)
    data.update(unigrams)

    print("current set length")
    print(len(data.keys()))

    filtered = delete_cases(data)
    
    print("after filtering")
    print(len(filtered))

    splits = []
    for key, _  in filtered.items(): 
        splits.append(filtered[key]['Split'])
    
    freq_dict = Counter()
    for elem in splits: 
        freq_dict[elem] +=1 
    print(freq_dict)


    with open('implicit_references.json', 'w') as json_out: 
         json.dump(filtered, json_out)
         

main()