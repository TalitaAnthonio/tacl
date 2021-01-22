# Used to check whether the atomic insertions file really contains atomic insertions 
# And used to extract trigrams and unigrams that are indeed atomic insertions. 

import json 


path_to_wiki_atomic_insertions = '../../../PhD/corpora/rulebook_diffs/2019-09-23/boardgame_scripts/wikihow/data/WikiAtomicInsertions.json'

with open(path_to_wiki_atomic_insertions, 'r') as json_in:
    wikihow_atomic_insertions = json.load(json_in)

# Sneak_Out_of_Your_House41

to_ignore = ['Sneak_Out_of_Your_House41']

def get_insertion_index(base_tokenized, revised_tokenized, insertion, key): 
    first_token_from_insertion = insertion[0][0] 
    length_of_insertion = len(insertion[0])
    indexes = []
    for index, token in enumerate(revised_tokenized,0):
        if token == first_token_from_insertion: 
           possible_insertion = revised_tokenized[index:index+length_of_insertion]
           if possible_insertion == insertion[0]: 
              #print("the same", possible_insertion, insertion[0])  
              indexes.append([index, index+length_of_insertion])
    # if the list of indexes > 1, it means that there are multiple choices 
    if len(indexes) > 1:
       indexes_in_base = [i for i in range(len(base_tokenized))]

       for index_pair in indexes: 
            if index_pair[0] not in indexes_in_base: 
               indexes = index_pair
            else: 
                if base_tokenized[index_pair[0]] != revised_tokenized[index_pair[0]]: 
                    indexes = [index_pair]
                    #print('final index', indexes)
                    break 
       return indexes
    else: 
        indexes = indexes 
    return indexes
           



def main(): 
    print("read")
    total = 0 
    counter = 0 
    trigram_insertions = {}
    for key, _ in wikihow_atomic_insertions.items(): 
        if key not in to_ignore: 
            total +=1 
            revised_tokenized = wikihow_atomic_insertions[key]['revised_tokenized']
            base_tokenized = wikihow_atomic_insertions[key]['base_tokenized']
            insertion = wikihow_atomic_insertions[key]['insertion_phrases']
            assert len(insertion) == 1
            if len(insertion[0]) == 4: 
                indexes = get_insertion_index(base_tokenized, revised_tokenized, insertion, key)
                if indexes: 
                    if type(indexes[0]) == int: 
                        indexes = [indexes]
        
                    merged_without_insertion = revised_tokenized[:indexes[0][0]]
                    second_part = revised_tokenized[indexes[0][1]:]
                    revised_without_insertion = merged_without_insertion + second_part 
                    if ' '.join(revised_without_insertion).lower() == ' '.join(base_tokenized).lower(): 
                        print(revised_tokenized)
                        print(insertion)
                        print(base_tokenized)
                        counter +=1 
                        print('=======================================')
                        trigram_insertions[key] = wikihow_atomic_insertions[key]
    print(counter)
    print(total)
    
    with open("../data/four-gram_atomic_edits.json", 'w') as json_out: 
         json.dump(trigram_insertions, json_out)
main()
