import json 
from helpers import check_if_revised_in_mentions

path_to_file = "../bigrams/bigram_atomic_edits_implicit_pos_filtered.json" 

with open(path_to_file, "r") as json_in: 
     bigrams = json.load(json_in)

counter = 0 
d = {}
for key, _ in bigrams.items(): 
    if bigrams[key]['bigram'] != True: 
        coreference_dict = bigrams[key]['coref']
        insertion = bigrams[key]['insertion_phrases'][0]
        index_of_revised_sentence = len(bigrams[key]['sents'])-1 
        corefs_with_revised_sentence = check_if_revised_in_mentions(coreference_dict, index_of_revised_sentence)

        #print(corefs_with_revised_sentence)
        refs = []
        current_reference = [bigrams[key]['insertion_phrases'][0][bigrams[key]['index_of_reference']]]
        possible_references = []
        for key2, mention_chain in dict(corefs_with_revised_sentence).items():
            for mention in corefs_with_revised_sentence[key2]: 
                if mention['ref'] == [insertion[0]]: 
                   possible_references += mention['ref']
        if possible_references != []: 
            print(set(possible_references))

print(counter)