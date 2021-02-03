import json 


path_to_older_dir = "/Users/talita/Documents/PhD/corpora/rulebook_diffs/2019-09-23/boardgame_scripts/wikihow/data/"

with open("unigram_edits_implicit.json", "r") as json_in: 
     data = json.load(json_in)

with open(path_to_older_dir + "WikiAtomicInsertions.json", "r") as json_in: 
     bigger_set = json.load(json_in)

with open(path_to_older_dir + "unigrams/SingleInsertions_coreferenced.json", "r") as json_in: 
     par_info = json.load(json_in)

data_with_filename_info = {}
for key, _ in data.items(): 
    data_with_filename_info[key] = data[key]
    data_with_filename_info[key].update({"filename": bigger_set[key]['filename'], "par": par_info[key]['par']})

with open("unigram_edits_implicit_v2.json", "w") as json_out:  
     json.dump(data_with_filename_info, json_out) 