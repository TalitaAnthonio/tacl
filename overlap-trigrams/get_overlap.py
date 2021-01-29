import json 
from helpers import check_if_revised_in_mentions
from collections import Counter

#(['filename', 'base_tokenized', 'id', 'revised_tokenized', 'revised_sentence', 'insertion_phrases', 'Base_Sentence', 'Base_Nr', 'Revised_Nr', 'parsed_revised_sentence', 'Base_Article', 'Base_Article_Clean', 'par', 'coref', 'insertion_indexes', 'sents'])


with open('../data/trigrams_atomic_edits_coref.json', 'r') as json_in: 
     trigram_data = json.load(json_in)

def select_biggest_reference(coreferences_in_revision_dict): 
    ref_ids = ["2", "1"]
    item_to_return = {}
    for ref_id in ref_ids: 
        if coreferences_in_revision_dict[ref_id] != []: 
           item_to_return = coreferences_in_revision_dict[ref_id][0]
           break # use to stop iterating (do not look for references that are smaller than the current one)
    return item_to_return
           

def get_distribution_info(data):
    """
     Params: 
     -------------------
     data {}: the final dataset of the form {key: {implicit reference}} 

     returns
     ---------------
     a dict of form Counter()
    """ 
    freqs = [data[key]['position-of-ref-in-insertion']for key, _ in data.items()] 
    freq_dist = Counter()
    for freq in freqs: 
         freq_dist[freq] +=1 
    return freq_dist


def check_for_multiple_references(coreferences_in_revision_dict): 
    """
       params 
       ----------
       coreferences_in_revision_dict {}: of the form {"2": [references], "1": [references] }

       returns a dict with coreference info for the longest entity among the found references. 
    """
    all_references = []
    for key, _ in coreferences_in_revision_dict.items(): 
        if coreferences_in_revision_dict[key] != []: 
           all_references += coreferences_in_revision_dict[key]
    # return the coreference info (there is only one possible ref)
    if len(all_references) == 1 and all_references != []: 
       return all_references[0]
    else: 
       biggest_ref = select_biggest_reference(coreferences_in_revision_dict) 
       return biggest_ref



def main(): 
     counter = 0 
     implicit_references = {}
     function_words = 0 
     list_of_function_words = ['or', 'and']
     for revision_id, _ in trigram_data.items():
          sents = trigram_data[revision_id]['sents']
          coreference_dict = trigram_data[revision_id]['coref']
          insertion = trigram_data[revision_id]['insertion_phrases'][0]
          index_of_revised_sentence = len(sents)-1
          revised_tokenized = trigram_data[revision_id]['revised_tokenized']
          base_tokenized = trigram_data[revision_id]['base_tokenized']
          # [[5, 8]]
          indexes = trigram_data[revision_id]['insertion_indexes']
          # Check if the revised sentence is in the coreference dict and obtain all the chains that have the revised sentence.  
          if coreference_dict != "empty" and coreference_dict != None: 
               corefs_with_revised_sentence = check_if_revised_in_mentions(coreference_dict, index_of_revised_sentence)
               # check if the insertion is in the reference. 
               coreferences_in_revision = {"1": [], "2": []}
               for coreference_id, _ in corefs_with_revised_sentence.items():
                    for mention in corefs_with_revised_sentence[coreference_id]: 
                         #if mention["ref"] == insertion: 
                         if mention['ref'] == insertion and mention["beginIndex"] == indexes[0][0]: 
                              implicit_references[revision_id] = trigram_data[revision_id]
                              implicit_references[revision_id].update({"insertion": insertion,  "reference-type": "trigram", "beginindex": indexes[0][0], "position-of-ref-in-insertion": "trigram", "reference": insertion})
                              
                              break 
                         # -------------------  check for bigrams -------------------------------
                         # check for the bigrams: ex: [in the box] -> the box (type1)
                         elif mention['ref'] == insertion[1:] and mention["beginIndex"] == indexes[0][0]+1: 
                              info_to_add = {"insertion": insertion, "reference-type": "bigram", "beginindex": indexes[0][0]+1, "position-of-ref-in-insertion": "trigram-last-two-tokens", "reference": insertion[1:]}
                              coreferences_in_revision["2"].append(info_to_add)
                         # ex: in the box -> in the (type2)
                         elif mention['ref'] == insertion[0:2] and mention["beginIndex"] == indexes[0][0]:
                              info_to_add = {"insertion": insertion, "reference-type": "bigram", "beginindex": indexes[0][0], "position-of-ref-in-insertion": "trigram-first-two-tokens", "reference": insertion[0:2]}
                              coreferences_in_revision["2"].append(info_to_add)
                         # -------------------  check for bigrams -------------------------------
                         # ---------------------check for single insertions--------------------------------
                         elif mention['ref'] == [insertion[0]] and mention["beginIndex"] == indexes[0][0]: 
                              info_to_add = {"insertion": insertion, "reference-type": "unigram", "beginindex": indexes[0][0], "position-of-ref-in-insertion": "trigram-first-token", "reference": [insertion[0]]}
                              coreferences_in_revision["1"].append(info_to_add)
                         elif mention['ref'] == [insertion[1]] and mention["beginIndex"] == indexes[0][0]+1: 
                              info_to_add = {"insertion": insertion, "reference-type": "unigram", "beginindex": indexes[0][0]+1, "position-of-ref-in-insertion": "trigram-second-token", "reference": [insertion[1]] }
                              coreferences_in_revision["1"].append(info_to_add)
                         elif mention['ref'] == [insertion[2]] and mention["beginIndex"] == indexes[0][0]+2: 
                              counter +=1 
                              info_to_add = {"insertion": insertion, "reference-type": "unigram", "beginindex": indexes[0][0]+2, "position-of-ref-in-insertion": "trigram-third-token", "reference": [insertion[2]]}
                              coreferences_in_revision["1"].append(info_to_add)
          
          info_from_coreference = check_for_multiple_references(coreferences_in_revision)
          if info_from_coreference != {} and revision_id not in implicit_references.keys(): 
             implicit_references[revision_id] = trigram_data[revision_id]
             implicit_references[revision_id].update(info_from_coreference)

     print(counter)
     print(len(implicit_references.keys()))
     freqs = get_distribution_info(implicit_references)
     print(freqs)
main() 


with open("../data/trigram_atomic_edits_implicit.json", "w") as json_out: 
     json.dump(implicit_references, json_out)

# Counter({'trigram-second-token': 1841, 'trigram-last-two-tokens': 1362, 'trigram-third-token': 652, 'trigram-first-token': 483, 'trigram-first-two-tokens': 173, 'trigram': 133})