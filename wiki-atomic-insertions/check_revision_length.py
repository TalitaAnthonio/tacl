# This file was used to check the revision length of the insertions and especially those with more than one revision. 


import json 

path_to_all = '../../../PhD/corpora/rulebook_diffs/2019-09-23/boardgame_scripts/wikihow/data/wikihow-with-line-numbers.json'

with open(path_to_all, 'r') as json_in:
    wikihow_all = json.load(json_in)

path_to_other = "../../../PhD/corpora/rulebook_diffs/2019-09-23/boardgame_scripts/wikihow/data/single_insertions_for_lm_generative_implicit_insertion.json"

with open(path_to_other, "r") as json_in: 
     single_insertions = json.load(json_in)


counter = 0 
for key in single_insertions.keys(): 
    if wikihow_all[key]['Revision_Length'] > 1: 
        print(key) 
        print(wikihow_all[key]['All_Versions'])
        counter +=1 

print(counter)