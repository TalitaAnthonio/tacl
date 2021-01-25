import json 
from helpers import check_if_revised_in_mentions
from collections import Counter

#(['filename', 'base_tokenized', 'id', 'revised_tokenized', 'revised_sentence', 'insertion_phrases', 'Base_Sentence', 'Base_Nr', 'Revised_Nr', 'parsed_revised_sentence', 'Base_Article', 'Base_Article_Clean', 'par', 'coref', 'insertion_indexes', 'sents'])


with open('../data/trigrams_atomic_edits_coref.json', 'r') as json_in: 
     trigram_data = json.load(json_in)



counter = 0 
implicit_references = {}
function_words = 0 
list_of_function_words = ['or', 'and']
for revision_id, _ in trigram_data.items():
    sents = trigram_data[revision_id]['sents']
    coreference_dict = trigram_data[revision_id]['coref']
    insertion = trigram_data[revision_id]['insertion_phrases'][0]
    index_of_revised_sentence = len(sents)-1
    revised_tokenized = trigram_data[revision_id]['revised_tokenized']
    base_tokenized = trigram_data[revision_id]['base_tokenized']
    # [[5, 8]]
    indexes = trigram_data[revision_id]['insertion_indexes']
    # Check if the revised sentence is in the coreference dict and obtain all the chains that have the revised sentence.  
    if coreference_dict != "empty" and coreference_dict != None: 
        corefs_with_revised_sentence = check_if_revised_in_mentions(coreference_dict, index_of_revised_sentence)
        # check if the insertion is in the reference. 
        for coreference_id, _ in corefs_with_revised_sentence.items():
            for mention in corefs_with_revised_sentence[coreference_id]: 
                #if mention["ref"] == insertion: 
                if mention['ref'] == insertion and mention["beginIndex"] == indexes[0][0]: 
                   implicit_references[revision_id] = trigram_data[revision_id]
                   implicit_references[revision_id].update({"type": "trigram", "beginindex": indexes[0][0], "category": "trigram"})
                   break 
                # -------------------  check for bigrams -------------------------------
                # check for the bigrams: ex: [in the box] -> the box (type1)
                elif mention['ref'] == insertion[1:] and mention["beginIndex"] == indexes[0][0]+1: 
                     #counter +=1
                     implicit_references[revision_id] = trigram_data[revision_id]
                     implicit_references[revision_id].update({"type": "bigram", "beginindex": indexes[0][0]+1, "category": "bigram-last-two"})
                     break 
                # ex: in the box -> in the (type2)
                elif mention['ref'] == insertion[0:2] and mention["beginIndex"] == indexes[0][0]:
                     implicit_references[revision_id] = trigram_data[revision_id] 
                     implicit_references[revision_id].update({"type": "bigram", "beginindex": indexes[0][0], "category": "bigram-first-two"})
                     break 
                # -------------------  check for bigrams -------------------------------
                # ---------------------check for single insertions--------------------------------
                elif mention['ref'] == [insertion[0]] and mention["beginIndex"] == indexes[0][0]: 
                     implicit_references[revision_id] = trigram_data[revision_id] 
                     implicit_references[revision_id].update({"type": "unigram", "beginindex": indexes[0][0], "category": "single-first"})
                     break 
                elif mention['ref'] == [insertion[1]] and mention["beginIndex"] == indexes[0][0]+1: 
                    implicit_references[revision_id] = trigram_data[revision_id] 
                    implicit_references[revision_id].update({"type": "unigram", "beginindex": indexes[0][0]+1, "category": "single-second"})
                    break 
                elif mention['ref'] == [insertion[2]] and mention["beginIndex"] == indexes[0][0]+2: 
                    implicit_references[revision_id] = trigram_data[revision_id] 
                    counter +=1 
                    implicit_references[revision_id].update({"type": "unigram", "beginindex": indexes[0][0]+2, "category":"single-third"})
                    break 


                
print(counter)
print(len(implicit_references.keys()))

elems = []
for key, _ in implicit_references.items(): 
    elems.append(implicit_references[key]['category'])

freq_dict = Counter()
for elem in elems: 
    freq_dict[elem] +=1 

print(freq_dict)