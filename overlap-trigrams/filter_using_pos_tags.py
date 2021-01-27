import spacy 
from spacy.tokens import Doc
import json

path_to_file = '../data/trigram_atomic_edits_implicit.json'
nlp = spacy.load("en_core_web_sm")
nlp.tokenizer = nlp.tokenizer.tokens_from_list


class RevisedSentence: 

    def __init__(self, revised_sentence, insertion_index): 
        self.revised_sentence = revised_sentence
        self.insertion_index = insertion_index


    @property 
    def sent_tagged(self): 
        parsed = []
        for doc in nlp.pipe([self.revised_sentence]):
            for token in doc:
                parsed.append([token, token.pos_])
        return parsed
    
    @property 
    def insertion_tagged(self): 
        return self.sent_tagged[self.insertion_index:self.insertion_index+3]


def tag_text(revised_sentence): 
    parsed = []
    for doc in nlp.pipe([revised_sentence]):
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
    revised_sent_tagged = tag_text(revised_sent)
    insertion_tagged = tag_insertion(revised_sent, insertion_index)
    print('----------------------------------------')

    sent = RevisedSentence(revised_sent, insertion_index)
    res1 = sent.insertion_tagged
    res2 = insertion_tagged
    print(res1)
    print(res2)