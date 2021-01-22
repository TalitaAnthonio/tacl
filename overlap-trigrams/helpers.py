def check_if_revised_in_mentions(coreference_dict, revised_sentence_index): 
    """
        Function used to check if the revised sentence is in the coreference chain. 

        Returns: 
        ------- 
        {key: sentence_indexes}, where the key is the   "coref": {"0"<-- this key
    """

    mentions_to_check = defaultdict(list)
    for key, _ in coreference_dict.items(): 
        mentions = coreference_dict[key]['mentions']
        for mention in mentions: 
            sentence_index = mention["sentenceIndex"]
            if sentence_index == revised_sentence_index: 
               mentions_to_check[key].append(mention)
    return mentions_to_check


def get_insertion_indexes(insertion, revised_tokenized):
    indexes_of_insertion = []
    for index, token in enumerate(revised_tokenized,0): 
        if token == insertion[0]: 
           possible_insertion = revised_tokenized[index:index+len(insertion)]
           if possible_insertion == insertion:
              list_with_insertions = [i for i in range(index, index+len(insertion))]
              indexes_of_insertion.append(list_with_insertions)
    return indexes_of_insertion
              
def correct_index_of_insertions(list_with_potential_indexes, base_tokenized, revised_tokenized): 
    if len(list_with_potential_indexes) == 1 or list_with_potential_indexes == []: 
        return list_with_potential_indexes
    else:
        # use this as initialisation 
        index_of_revised = []
        # [[9, 10], [28, 29]]
        for index_of_index, index in enumerate(list_with_potential_indexes,0): 
            print("index")
            print(index) 
            try: 
                # year = year (insertie = year after )
                if base_tokenized[index[0]: index[0]+2] != revised_tokenized[index[0]: index[0]+2]: 
                   index_of_revised = index 
                   break 
                   
            except IndexError: 
                index_of_revised = index 
                break 
        return [index_of_revised]



def compute_distance_frequencies(list_with_sentence_distances): 
    """
        Param: 
        --------------------------------
        list_with_sentence_distance {list}: list with the distance from revised sentence to the mention. 
    """
    freq_dict = Counter()
    for elem in list_with_sentence_distances: 
        freq_dict[elem] +=1 

    freq_dict_sorted = {k: v for k, v in sorted(freq_dict.items(), key=lambda item: item[1], reverse=True)}
    return freq_dict_sorted



if __name__ == '__main__':
   main()