import json 

with open("../data/trigram_atomic_edits.json", 'r') as json_in: 
        trigram_atomic_edits = json.load(json_in)


path_to_insertions = "/Users/talita/Documents/PhD/corpora/rulebook_diffs/2019-09-23/boardgame_scripts/wikihow/data/trigrams/benepar_trigram_insertions_needs_coref.json"

with open(path_to_insertions, "r") as json_in: 
     to_be_parsed = json.load(json_in)


def read_json_lines(path_to_file): 
    d = {}
    with open(path_to_file) as json_in: 
         for line in json_in: 
             line = json.loads(line)
             d[line['id']] = line 
    return d 



def main(): 

    path_to_trigrams_part1 = "/Users/talita/Documents/PhD/corpora/rulebook_diffs/2019-09-23/boardgame_scripts/wikihow/data/trigrams/trigrams_coref_part1.json"
    path_to_trigrams_part2 = "/Users/talita/Documents/PhD/corpora/rulebook_diffs/2019-09-23/boardgame_scripts/wikihow/data/trigrams/trigrams_coref_part2.json"
    path_to_trigrams_part3 = "../data/trigrams_remaining_atomic_edits_out.json"


    part1 = read_json_lines(path_to_trigrams_part1)
    part2 = read_json_lines(path_to_trigrams_part2)
    part3 = read_json_lines(path_to_trigrams_part3) 
    part1.update(part2)
    part1.update(part3)

    counter = 0 
    needs_coref = {}
    for key, _ in trigram_atomic_edits.items(): 
        if key in part1.keys(): 
           needs_coref[key] = to_be_parsed[key]
           counter +=1 
           needs_coref[key].update({"parsed_revised_sentence": part1[key]['parsed_revised_sentence'], "coref": part1[key]['coref'], "insertion_indexes": trigram_atomic_edits[key]["indexes"], "sents": part1[key]['sents']})

    print(counter)
    print(len(trigram_atomic_edits.keys()))

    with open("../data/trigrams_current_set.json", "w") as json_out:
         json.dump(needs_coref, json_out)
main() 