import json 



KEYS_TO_EXCLUDE = ['Answer_Common_Atheists_Questions_About_Christianity23', 'Celebrate_Thanksgiving62', 'Dress_in_American_1940s_Fashion12', 'Know_That_You_Are_Going_to_Heaven_As_a_Christian47']
PATH_TO_FILE = '../all-references/implicit_references.json'
PATH_FOR_UNIGRAMS = '/Users/talita/Documents/PhD/corpora/rulebook_diffs/2019-09-23/boardgame_scripts/wikihow/overlap/unigrams_with_coref_info.json'
PATH_FOR_BIGRAMS = '/Users/talita/Documents/PhD/corpora/rulebook_diffs/2019-09-23/boardgame_scripts/wikihow/cloze-test/bigram_references_for_lm_generative_insertions_with_original_context_new.json'
PATH_TO_FILE_OUT = "../data/references_for_lm.json"

with open(PATH_FOR_UNIGRAMS, 'r') as json_in: 
     unigram_data_prev = json.load(json_in)

with open(PATH_TO_FILE, 'r') as json_in: 
     data = json.load(json_in)

with open(PATH_FOR_BIGRAMS, 'r') as json_in: 
     bigram_data_prev = json.load(json_in)

def get_context_for_trigrams(key, trigram_instance): 
    context = trigram_instance['par'].rstrip('\n').replace('\n', '')
    context = remove_timestamps(context)
    position_of_reference = trigram_instance['position-of-ref-in-insertion']
    index_of_reference = trigram_instance['insertion_indexes']
    begin_position = index_of_reference[0][0]

    if position_of_reference == 'trigram': 
       reference = trigram_instance['revised_tokenized'][begin_position:begin_position+3]
       revised_untill_insertion = trigram_instance['revised_tokenized'][:begin_position]
       revised_after_insertion = trigram_instance['revised_tokenized'][begin_position+3:]
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
    language_model_text = context + ' ' + ' '.join(revised_untill_insertion)

    return {"language_model_text": language_model_text, "revised_after_insertion": ' '.join(revised_after_insertion), "revised_untill_insertion": ' '.join(revised_untill_insertion), "reference": reference}




def remove_timestamps(context): 
    context = context.split()
    for elem in context: 
        if 'Timestamp' in elem: 
            context = context[2:]
            break 
    return ' '.join(context) 

def main(): 
    data_with_info = {}
    for key, _ in data.items(): 
        # double checked whether everything was correct. 
        # 254 in dev, 229 in test.  
        if data[key]['insertion-type'] == 1:          
            context_with_removed_timestamps = remove_timestamps(unigram_data_prev[key]['language_model_text'])
            lm_components = {"language_model_text": context_with_removed_timestamps, "revised_after_insertion": unigram_data_prev[key]['revised_after_insertion'], "revised_untill_insertion": unigram_data_prev[key]['revised_untill_insertion']}
            
            
            
        # 177 in dev, 178 in test 
        elif data[key]['insertion-type'] == 2:  
            context_with_removed_timestamps = remove_timestamps(bigram_data_prev[key]['language_model_text'])
            lm_components = {"language_model_text": context_with_removed_timestamps, "revised_afer_insertion": bigram_data_prev[key]['revised_after_insertion'], "revised_untill_insertion": bigram_data_prev[key]['revised_untill_insertion']}
        # 160 in dev, 140 in test 
        else: 
            # insertion-type = 3
            lm_components = get_context_for_trigrams(key, data[key])

        if key not in KEYS_TO_EXCLUDE: 
           data_with_info[key] = data[key]
           data_with_info[key].update(lm_components)
    
    with open(PATH_TO_FILE_OUT, 'w') as json_out: 
         json.dump(data_with_info, json_out)
            
main()