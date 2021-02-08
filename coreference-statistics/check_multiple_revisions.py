import json 
from collections import Counter 


BIGGER_FILE = "/Users/talita/Documents/PhD/corpora/rulebook_diffs/2019-09-23/boardgame_scripts/wikihow/data/wikihow-with-line-numbers.json"

with open('../all-references/implicit_references.json', 'r') as json_in: 
     data = json.load(json_in)


with open(BIGGER_FILE, "r") as json_in: 
     all_revisions = json.load(json_in)


counter = 0 
revision_lengths = []
for key, _ in data.items(): 
    revision_length = all_revisions[key]['Revision_Length']
    if revision_length > 1: 
       #print(revision_length)
       #counter +=1 
       print(all_revisions[key]['All_Versions'])


freq_dict = Counter()
for elem in revision_lengths: 
    freq_dict[elem] +=1 

print(freq_dict)

print(counter)