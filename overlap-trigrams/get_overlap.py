import json 

#dict_keys(['filename', 'base_tokenized', 'id', 'revised_tokenized', 'revised_sentence', 'insertion_phrases', 'Base_Sentence', 'Base_Nr', 'Revised_Nr', 'parsed_revised_sentence', 'Base_Article', 'Base_Article_Clean', 'par', 'coref'])

with open('../data/trigrams_current_set.json', 'r') as json_in: 
     trigram_data = json.load(json_in)



for revision_id, _ in trigram_data.items():
    sents = trigram_data[key]['sents']
    insertion = trigram_data[key]['insertion_phrases']
    index_of_revised_sentence = len(sents)-1
    revised_tokenized = trigram_data[key]['revised_tokenized']
    base_tokenized = trigram_data[key]['base_tokenized']
    # -------- add all necessary variables --------------
