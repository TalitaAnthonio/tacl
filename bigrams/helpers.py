from collections import defaultdict

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

