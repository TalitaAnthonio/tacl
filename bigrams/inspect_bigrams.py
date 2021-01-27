import json 

path_to_file = "/Users/talita/Documents/PhD/corpora/rulebook_diffs/2019-09-23/boardgame_scripts/wikihow/annotation-study/bigram_implicit_references_atomic.json"

with open(path_to_file, "r") as file_in: 
     data = json.load(file_in)

print(len(data.keys()))