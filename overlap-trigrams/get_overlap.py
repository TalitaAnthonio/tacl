import json 

#dict_keys(['filename', 'base_tokenized', 'id', 'revised_tokenized', 'revised_sentence', 'insertion_phrases', 'Base_Sentence', 'Base_Nr', 'Revised_Nr', 'parsed_revised_sentence', 'Base_Article', 'Base_Article_Clean', 'par', 'coref'])

with open('../data/trigrams_current_set.json', 'r') as json_in: 
     trigram_data = json.load(json_in)



for key, _ in trigram_data.items():
    print(trigram_data[key].keys())

    print(trigram_data[key]['base_tokenized'])
    print(trigram_data[key]['revised_tokenized'])
    print(trigram_data[key]['parsed_revised_sentence'])
    if trigram_data[key]['parsed_revised_sentence'] != "EMPTY": 
        print(trigram_data[key]['parsed_revised_sentence']['insertion_parsed'])
    print(trigram_data[key]['insertion_phrases'])
    print(trigram_data[key]['insertion_indexes'])
    print('------------------------------------')
