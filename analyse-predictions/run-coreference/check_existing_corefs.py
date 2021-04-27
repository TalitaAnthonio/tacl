import json 
from collections import Counter
import pdb 
  
def most_frequent(List):
    occurence_count = Counter(List)
    return occurence_count.most_common(1)[0][0]


path_to_file = "../../data/references_for_lm.json"

path_to_other = "/Users/talita/Documents/PhD/corpora/rulebook_diffs/2019-09-23/boardgame_scripts/wikihow/data/unigrams/SingleInsertions_coreferenced.json"

with open(path_to_file, 'r') as json_in: 
     data = json.load(json_in)

with open(path_to_other, 'r') as json_in: 
     second_part = json.load(json_in)


d = {}
for key, _ in data.items(): 
    #corefs = data[key]['coref']
    #except KeyError: 
    #    pdb.set_trace()
    total_referring_expressions = 0 

    if "coref" in data[key].keys(): 
        corefs = data[key]['coref']
    else: 
        corefs = second_part[key]['coref']

    highest_num = 0 
    longest_chain = []
 
    for coref_id, _ in corefs.items():
        referring_expressions = [' '.join(mention['ref']) for mention in corefs[coref_id]['mentions']]
        total_referring_expressions += len(referring_expressions)
        print(referring_expressions)
        print(len(referring_expressions))
        
        if len(referring_expressions) > highest_num: 
            highest_num = len(referring_expressions)
            longest_chain = referring_expressions


    print("===========================")
    print(longest_chain)
    print(most_frequent(longest_chain))
    print()
    d[key] = {"highest_num": highest_num, "chain": longest_chain, "most_frequent": most_frequent(longest_chain), "total_referring_expressions": total_referring_expressions}
    

with open("most_frequent_reference_baseline.json", "w") as json_out: 
     json.dump(d, json_out)