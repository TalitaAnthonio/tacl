import json 



KEYS_TO_EXCLUDE = ['Answer_Common_Atheists_Questions_About_Christianity23', 'Celebrate_Thanksgiving62', 'Dress_in_American_1940s_Fashion12', 'Know_That_You_Are_Going_to_Heaven_As_a_Christian47']
PATH_TO_FILE = '../all-references/implicit_references.json'
PATH_FOR_UNIGRAMS = '/Users/talita/Documents/PhD/corpora/rulebook_diffs/2019-09-23/boardgame_scripts/wikihow/overlap/unigrams_with_coref_info.json'
PATH_FOR_BIGRAMS = '/Users/talita/Documents/PhD/corpora/rulebook_diffs/2019-09-23/boardgame_scripts/wikihow/cloze-test/bigram_references_for_lm_generative_insertions_with_original_context_new.json'

with open(PATH_FOR_UNIGRAMS, 'r') as json_in: 
     unigram_data_prev = json.load(json_in)

with open(PATH_TO_FILE, 'r') as json_in: 
     data = json.load(json_in)

with open(PATH_FOR_BIGRAMS, 'r') as json_in: 
     bigram_data_prev = json.load(json_in)

def get_context_for_trigrams(key, trigram_instance): 
    context = trigram_instance['par'].rstrip('\n').replace('\n', '')
    position_of_reference = trigram_instance['position-of-ref-in-insertion']
    index_of_reference = trigram_instance['insertion_indexes']
    begin_position = index_of_reference[0][0]
    if position_of_reference == 'trigram': 
       reference = trigram_instance['revised_tokenized'][begin_position:begin_position+3]
  
    # add for bigrams 
    elif position_of_reference == 'trigram-last-two-tokens': 
       reference = trigram_instance['revised_tokenized'][begin_position+1:begin_position+3]
       revised_untill_insertion = trigram_instance['revised_tokenized'][:begin_position+1]
       revised_after_insertion = trigram_instance['revised_tokenized'][begin_position+3:]
    elif position_of_reference == 'trigram-first-two-tokens': 
        reference = trigram_instance['revised_tokenized'][begin_position:begin_position+2]
        revised_untill_insertion = trigram_instance['revised_tokenized'][:begin_position]
        revised_after_insertion = trigram_instance['revised_tokenized'][begin_position+2:]
    
    # add for unigrams 
    elif position_of_reference == 'trigram-first-token': 
        reference = trigram_instance['insertion_phrases'][0][0]
        revised_untill_insertion = trigram_instance['revised_tokenized'][:begin_position]
        revised_after_insertion = trigram_instance['revised_tokenized'][begin_position+1:]
    elif position_of_reference == 'trigram-second-token': 
        reference = trigram_instance['insertion_phrases'][0][1]
        revised_untill_insertion = trigram_instance['revised_tokenized'][:begin_position+1]
        revised_after_insertion = trigram_instance['revised_tokenized'][begin_position+2:]
    # check tomorrow 
    else: 
        reference = trigram_instance['insertion_phrases'][0][2]
        revised_untill_insertion = trigram_instance['revised_tokenized'][:begin_position+2]
        revised_after_insertion = trigram_instance['revised_tokenized'][begin_position+3:]
        print('----------------------------')
        print(revised_untill_insertion)
        print(reference)
        print(revised_after_insertion)
        print(trigram_instance['revised_tokenized'])
        



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
            context_with_removed_timestamps = remove_timestamps(bigram_data_prev[key]['language_model_text'])
            split = data[key]['Split']
        elif data[key]['insertion-type'] ==3: 
            get_context_for_trigrams(key, data[key])

            #assert data[key]['revised_sentence'][data[key]['index_of_insertion'][0]] == data[key]['insertion'][0]
            #print(unigram_data_prev[key]['language_model_text'])
        #   print(data[key]['revised_untill_insertion'])
           
main()