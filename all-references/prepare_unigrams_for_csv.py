import json

path_to_file = "/Users/talita/Documents/PhD/corpora/rulebook_diffs/2019-09-23/boardgame_scripts/wikihow/annotation-study/single_implicit_references_atomic.json" 

with open(path_to_file, "r") as json_in: 
     data = json.load(json_in)


d = {}
for key, _ in data.items(): 
    d[key] = data[key]
    to_add = {"reference": data[key]['insertion'], "reference-type": "unigram", "position-of-ref-in-insertion": "unigram"}
    d[key].update(to_add)

with open('unigram_edits_implicit.json', 'w') as json_out: 
     json.dump(d, json_out)