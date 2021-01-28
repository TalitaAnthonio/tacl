import json 
import spacy 
from spacy.tokens import Doc

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


def filter_using_pos_tags(data):
    counter = 0 
    filtered = {}
    for key, _ in data.items(): 
        #print(data[key]['base_tokenized']) 
        #print(data[key]['revised_sentence'])
        #print(data[key]['insertion_phrases'][0])
        #print(data[key]['index_of_insertion'][0])

        revised_sentence_object = RevisedSentence(data[key]['revised_tokenized'], data[key]['index_of_insertion'][0][0])

        insertion_tagged = revised_sentence_object.insertion_tagged
        pos_tags_in_insertion = [pair[1] for pair in insertion_tagged]
        if 'VERB' not in pos_tags_in_insertion:
            if 'AUX' not in pos_tags_in_insertion:  
                if 'CCONJ' not in pos_tags_in_insertion: 
                    counter +=1 
                    filtered[key] = data[key]
        
    return filtered



def main(): 
    counter = 0 
    filtered_set = filter_using_pos_tags(data)
    for key, _ in filtered_set.items(): 
        if type(filtered_set[key]) == list: 
           print(filtered_set[key])
           break 

    filtered_set_bigrams = {}
    for key, _ in filtered_set.items(): 
        if filtered_set[key]['bigram'] == True: 
            filtered_set_bigrams[key] = filtered_set[key]
            reference =  filtered_set[key]['insertion_phrases'][0]
            filtered_set_bigrams[key].update({"insertion":filtered_set[key]['insertion_phrases'][0], "reference": reference, "reference-type": "bigram", "position-of-ref-in-insertion": "bigram"})
        else:
            filtered_set_bigrams[key] = filtered_set[key] 
            reference = [filtered_set[key]['insertion_phrases'][0][filtered_set[key]['index_of_reference']]]

            if filtered_set[key]['index_of_reference'] == 0: 
                reference_type = "bigram-first-token"
            else: 
                reference_type = "bigram-second-token"
                filtered_set_bigrams[key].update({"insertion": filtered_set[key]['insertion_phrases'][0], "reference": reference, "reference-type": "unigram", "position-of-ref-in-insertion": reference})
    
    print(filtered_set_bigrams.keys())

    with open("bigram_atomic_edits_implicit_pos_filtered.json", "w") as json_out: 
         json.dump(filtered_set_bigrams, json_out)

main() 