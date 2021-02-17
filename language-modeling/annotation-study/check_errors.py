import json 


# dict_keys(['predictions', 'key', 'revised_sentence', 'insertion', 
# 'coref', 'sents', 'filename', 'base_tokenized', 'id', 'revised_tokenized', 
# 'insertion_phrases', 'Base_Sentence', 'Base_Nr', 'Revised_Nr', 'parsed_revised_sentence', 
# 'Base_Article', 'Base_Article_Clean', 'par', 'index_of_insertion', 'index_of_reference', 
# 'bigram', 'stats', 'reference', 'reference-type', 'position-of-ref-in-insertion', 'Split', 'insertion-type', 'language_model_text', 'revised_afer_insertion', 'revised_untill_insertion'])


PATH_TO_FILE = "errors_in_dev.json"

with open(PATH_TO_FILE, "r") as json_in: 
     data = json.load(json_in)


def main(): 
    for key, _ in data.items(): 
        print(data[key].keys())
        print(data[key]['base_tokenized'])
        print(data[key]['revised_sentence'])
        print(data[key]['reference'])
        print(data[key]['predictions'])
        print("========================")

main() 