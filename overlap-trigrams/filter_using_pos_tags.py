import spacy 
from spacy.tokens import Doc
import json

path_to_file = '../data/trigram_atomic_edits_implicit.json'
nlp = spacy.load("en_core_web_sm")
nlp.tokenizer = nlp.tokenizer.tokens_from_list

def tag_text(revised_sentence_tokenized): 
    parsed = []
    for doc in nlp.pipe([revised_sentence_tokenized]):
        for token in doc:
            parsed.append([token, token.pos_])
    return parsed

def tag_insertion(revised_sentence_tokenized, index): 
    parsed = []
    for doc in nlp.pipe([revised_sentence_tokenized]):
        for token in doc:
            parsed.append([token, token.pos_])
    return parsed[index:index+3]



with open(path_to_file, "r") as json_in: 
     data = json.load(json_in)

print(len(data.keys()))
for key, _ in data.items(): 
    revised_sent = data[key]['revised_tokenized']
    insertion_index = data[key]['insertion_indexes'][0][0]
    print(revised_sent)
    revised_sent_tagged = tag_text(revised_sent)
    insertion_tagged = tag_insertion(revised_sent, insertion_index)
    print(revised_sent_tagged)
    print(insertion_index)
    print(insertion_tagged)
    print('----------------------------------------')