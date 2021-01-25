import json 
from helpers import check_if_revised_in_mentions

#(['filename', 'base_tokenized', 'id', 'revised_tokenized', 'revised_sentence', 'insertion_phrases', 'Base_Sentence', 'Base_Nr', 'Revised_Nr', 'parsed_revised_sentence', 'Base_Article', 'Base_Article_Clean', 'par', 'coref', 'insertion_indexes', 'sents'])


with open('../data/trigrams_atomic_edits_coref.json', 'r') as json_in: 
     trigram_data = json.load(json_in)



counter = 0 
implicit_references = {}
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
                   counter +=1 
                   implicit_references[revision_id] = trigram_data[revision_id]
                   implicit_references[revision_id].update({"type": "trigram", "beginindex": indexes[0][0]})
                   print(base_tokenized)
                   print(revised_tokenized) 
                   print(insertion)
                   print('---------------------------------------------------------------------')
print(counter)
print(len(implicit_references.keys()))