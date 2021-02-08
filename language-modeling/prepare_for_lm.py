import json 

PATH_TO_FILE = '../all-references/implicit_references.json'
PATH_FOR_UNIGRAMS = '/Users/talita/Documents/PhD/corpora/rulebook_diffs/2019-09-23/boardgame_scripts/wikihow/overlap/unigrams_with_coref_info.json'
PATH_FOR_BIGRAMS = '/Users/talita/Documents/PhD/corpora/rulebook_diffs/2019-09-23/boardgame_scripts/wikihow/cloze-test/bigram_references_for_lm_generative_insertions_with_original_context_new.json'

with open(PATH_FOR_UNIGRAMS, 'r') as json_in: 
     unigram_data_prev = json.load(json_in)

with open(PATH_TO_FILE, 'r') as json_in: 
     data = json.load(json_in)

with open(PATH_FOR_BIGRAMS, 'r') as json_in: 
     bigram_data_prev = json.load(json_in)

def get_index_from_revised_sent(): 
    pass 


def remove_timestamps(context): 
    context = context.split()
    for elem in context: 
        if 'Timestamp' in elem: 
            context = context[2:]
            break 
    return ' '.join(context) 

def main(): 
    counter = 0 
    for key, _ in data.items(): 
        # double checked whether everything was correct. 
        # 254 in dev, 229 in test.  
        if data[key]['insertion-type'] == 1:          
            context_with_removed_timestamps = remove_timestamps(unigram_data_prev[key]['language_model_text'])
            split = data[key]['Split']
        # 117 in dev, 178 in test 
        elif data[key]['insertion-type'] == 2:  
            print(data[key].keys())
            context_with_removed_timestamps = remove_timestamps(bigram_data_prev[key]['language_model_text'])
            split = data[key]['Split']
        else: 
            # do it for the trigrams 


    print(counter)

            #assert data[key]['revised_sentence'][data[key]['index_of_insertion'][0]] == data[key]['insertion'][0]
            #print(unigram_data_prev[key]['language_model_text'])
        #   print(data[key]['revised_untill_insertion'])
           
main()