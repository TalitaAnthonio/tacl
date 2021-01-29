import spacy 
from spacy.tokens import Doc
import json

path_to_file = '../data/trigram_atomic_edits_implicit.json'
nlp = spacy.load("en_core_web_sm")
nlp.tokenizer = nlp.tokenizer.tokens_from_list


with open(path_to_file, "r") as json_in: 
     data = json.load(json_in)


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



def first_step_filtering(data):
    """
        Remove the insertions from the data that have a VERB, AUX or a CONJUNCTION 
    """ 
    filtered_set = {}
    for key, _ in data.items(): 
        revised_tokenized = data[key]['revised_tokenized']
        insertion_index = data[key]['insertion_indexes'][0][0]

        revised_sentence = RevisedSentence(revised_tokenized, insertion_index)
        insertion_tagged = revised_sentence.insertion_tagged
        pos_tags_in_insertion = [pair[1] for pair in insertion_tagged]

        if 'VERB' not in pos_tags_in_insertion:
            if 'AUX' not in pos_tags_in_insertion:  
                if 'CCONJ' not in pos_tags_in_insertion: 
                    print(data[key]['base_tokenized'])
                    print(revised_tokenized)
                    print(insertion_tagged)
                    print(data[key]['insertion_phrases'])
                    print(data[key]['reference']) 
                    filtered_set[key] = data[key]
    return filtered_set



def main():
    print(len(data.keys()))

    filtered_set = first_step_filtering(data)
    print(len(filtered_set.keys()))

main()