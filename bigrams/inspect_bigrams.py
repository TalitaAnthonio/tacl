import json 
import spacy 
from spacy.tokens import Doc

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
        return self.sent_tagged[self.insertion_index:self.insertion_index+2]


# dict_keys(['coref', 'sents', 'filename', 'base_tokenized', 'id', 'revised_tokenized', 'revised_sentence', 'insertion_phrases', 'Base_Sentence', 'Base_Nr', 'Revised_Nr', 'parsed_revised_sentence', 'Base_Article', 'Base_Article_Clean', 'par', 'index_of_insertion', 'index_of_reference', 'bigram', 'stats'])
path_to_file = "/Users/talita/Documents/PhD/corpora/rulebook_diffs/2019-09-23/boardgame_scripts/wikihow/annotation-study/bigram_implicit_references_atomic.json"

with open(path_to_file, "r") as file_in: 
     data = json.load(file_in)


def main(): 
    counter = 0 
    for key, _ in data.items(): 
        #print(data[key]['base_tokenized']) 
        #print(data[key]['revised_sentence'])
        #print(data[key]['insertion_phrases'][0])
        #print(data[key]['index_of_insertion'][0])

        revised_sentence_object = RevisedSentence(data[key]['revised_tokenized'], data[key]['index_of_insertion'][0][0])

        insertion_tagged = revised_sentence_object.insertion_tagged
        pos_tags_in_insertion = [pair[1] for pair in insertion_tagged]
        print('---------------------------------')
        if 'VERB' not in pos_tags_in_insertion:
            if 'AUX' not in pos_tags_in_insertion:  
                if 'CCONJ' not in pos_tags_in_insertion: 
                    counter +=1 
                    print(insertion_tagged)
        
    print(counter)
    print(len(data.keys()))

main() 