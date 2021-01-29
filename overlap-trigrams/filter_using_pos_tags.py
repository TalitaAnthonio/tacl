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
                    filtered_set[key] = data[key]
    return filtered_set


def filter_unigrams(filtered_set): 
    revised_sentence_object = RevisedSentence(filtered_set['revised_tokenized'], filtered_set['insertion_indexes'][0][0]) 
    insertion_tagged = revised_sentence_object.insertion_tagged
    pos_tags_in_insertion = [pair[1] for pair in revised_sentence_object.insertion_tagged]
    # trigram-second-token, trigram-third-token
    reference_type = filtered_set['position-of-ref-in-insertion']
    # only keep them when there is punctuation twice (only 3 remain)
    if reference_type == 'trigram-first-token': 
       if pos_tags_in_insertion[1] == 'PUNCT' and pos_tags_in_insertion[2] == 'PUNCT': 
            print(insertion_tagged, filtered_set['reference'])
    
        



def main():

    #TOADD: make similar rules for trigram-second-token, trigram-third-token
    print(len(data.keys()))
    print('make filtered set')
    filtered_set = first_step_filtering(data)
    
    for key, _ in filtered_set.items(): 
        if filtered_set[key]['reference-type'] == 'unigram': 
           filter_unigrams(filtered_set[key])
           

main()