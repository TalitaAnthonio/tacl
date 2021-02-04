import json 

path_to_subset = "../all-references/unigram_edits_final.json"
path_to_coref_info = "/Users/talita/Documents/PhD/corpora/rulebook_diffs/2019-09-23/boardgame_scripts/wikihow/overlap/unigrams_with_coref_info.json"


def read_file_with_filenames(path_to_file): 
    with open(path_to_file, "r") as file_in: 
         content = file_in.readlines()
         list_of_files = [filename.strip('\n') for filename in content]
         return list_of_files


KEYS_TO_DELETE = read_file_with_filenames("../all-references/keys_to_delete.txt")


with open(path_to_coref_info, "r") as json_in: 
     coref_info = json.load(json_in)

with open(path_to_subset, "r") as json_in: 
     unigrams = json.load(json_in)




def main(): 

    data_with_coref_info = {}
    for key, _ in unigrams.items(): 
        if key not in KEYS_TO_DELETE: 
          data_with_coref_info[key] = unigrams[key]
          data_with_coref_info[key].update({'CorefChain': coref_info[key]['chain-with-mention']})

    with open("../data/unigram_atomic_edits_coref.json", 'w') as json_out: 
         json.dump(data_with_coref_info, json_out)

main()