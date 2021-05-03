import json 
from collections import OrderedDict
import pdb 

path_to_file_with_predictions = '../analyse-predictions/bestmodels_predictions.json'
coref_chain_info_unigrams_path = "../data/unigram_atomic_edits_coref.json"
coref_chain_info_bigrams_path = "../data/bigram_atomic_edits_coref.json"
coref_chain_info_trigrams_path = "../data/trigram_atomic_edits_coref_info.json"



with open(path_to_file_with_predictions, 'r') as json_in: 
     data = json.load(json_in)



with open(coref_chain_info_unigrams_path, 'r') as json_in: 
     coref_data = json.load(json_in)


with open(coref_chain_info_bigrams_path, 'r') as json_in: 
     bigrams = json.load(json_in)


with open(coref_chain_info_trigrams_path, 'r') as json_in: 
     trigrams = json.load(json_in)




# add everything together 
coref_data.update(bigrams)
coref_data.update(trigrams)


remaining_corefs = "/Users/talita/Documents/PhD/corpora/rulebook_diffs/2019-09-23/boardgame_scripts/wikihow/data/unigrams/SingleInsertions_coreferenced.json"

with open(remaining_corefs, "r") as json_in: 
     other_unigrams = json.load(json_in)




def check_pos_of_filler(predictions, correct_filler, topk=10): 
    if correct_filler.lower() in predictions[:topk]: 
       return 1 
    else: 
        return 0 




def get_ref_per_sent(coref_info): 
    reference_index_list = {}
    for coref_id, _ in coref_info.items(): 
        for mention in coref_info[coref_id]["mentions"]: 
            sentence_index = mention["sentenceIndex"]
            begin_index = mention["beginIndex"]
            reference = mention["ref"]
            sent = mention["tokenized_sent"]


            if sentence_index not in reference_index_list.keys(): 
                reference_index_list[sentence_index] = {}
                reference_index_list[sentence_index]["reference"] = []
                reference_index_list[sentence_index]["reference"].append([reference, begin_index])
                reference_index_list[sentence_index]["sentlength"] = len(sent)
            else: 
                reference_index_list[sentence_index]["reference"].append([reference, begin_index])
                reference_index_list[sentence_index]["sentlength"] = len(sent)
    return reference_index_list


def main(): 
    counter = 0 
    for key, _ in data.items():
        
        if "coref" in coref_data[key].keys(): 
            reference_index_list = get_ref_per_sent(coref_data[key]["coref"])
        else: 
            reference_index_list = get_ref_per_sent(other_unigrams[key]["coref"])


        sentence_indexes = sorted(reference_index_list.keys()) 
        sentence_indexes.reverse()
        
        # just used for printing 
        for sentence_index in sentence_indexes:
            sorted_references = sorted(reference_index_list[sentence_index]["reference"], key=lambda x:x[-1], reverse=True) 
            indexes = [elem[-1] for elem in sorted_references]

            print(sentence_index, sorted_references, "sentence length", reference_index_list[sentence_index]["sentlength"])
        
        # just used for printing 
        
        print(sentence_indexes)

        # take the reference and the correct index 
        if "reference" in data[key].keys():
            correct_reference = data[key]["reference"]
        else: 
            correct_reference = data[key]["CorrectReference"]
        index_of_reference = data[key]["index_of_reference"]
        correct_reference_index_pair = [correct_reference.split(), index_of_reference]

        # print all the referring expressions of the revised sentence. 
        referring_expressions_in_revised_pairs = sorted(reference_index_list[sentence_indexes[0]]["reference"], key=lambda x:x[-1], reverse=True)
        try: 
            position_of_correct_reference = referring_expressions_in_revised_pairs.index(correct_reference_index_pair)
            print("nr of references in revised", len(referring_expressions_in_revised_pairs))
            counter +=1 

            # if there is just one refererring expression in the revised sentence (which should be the human-inserted one), take the closest referring expression of the previous sentence. 
            if len(referring_expressions_in_revised_pairs) == 1: 
               referring_expressions_in_previous_sentence = sorted(reference_index_list[sentence_indexes[1]]["reference"], key=lambda x:x[-1], reverse=True)[0][0]
               print("The nearest reference is", referring_expressions_in_previous_sentence)
            else: 
               # check the cataphors with one sentence 
               if len(sentence_indexes) == 1: 
                  print("Cataphoric")
                  print(referring_expressions_in_revised_pairs)
               
               else: 
                    # check the closest referring expression in the previous sentence 
                    closest_referring_expression_in_the_previous_sentence = sorted(reference_index_list[sentence_indexes[1]]["reference"], key=lambda x:x[-1], reverse=True)[0]
                    sentence_length_of_previous_sentence = reference_index_list[sentence_indexes[1]]["sentlength"]
                    print("the closest referring expression in the previous sentence", closest_referring_expression_in_the_previous_sentence)
                    if position_of_correct_reference == 0: 
                       next_referring_expression_in_revised_sentence = sorted(reference_index_list[sentence_indexes[0]]["reference"], key=lambda x:x[-1], reverse=True)[1]
                       absolute_distance_between_ref_in_same = abs(correct_reference_index_pair[-1] - next_referring_expression_in_revised_sentence[-1])

                       absolute_distance_between_ref_in_prev = abs(abs(sentence_length_of_previous_sentence - closest_referring_expression_in_the_previous_sentence[-1]) + (correct_reference_index_pair[-1])) 
                       
                       print(absolute_distance_between_ref_in_same, "same sent")
                       print(absolute_distance_between_ref_in_prev, "prev sent")

                       print("closest referring expression", next_referring_expression_in_revised_sentence)
                       print("correct reference", correct_reference_index_pair)


                       if absolute_distance_between_ref_in_same > absolute_distance_between_ref_in_prev: 
                          print("closest reference", closest_referring_expression_in_the_previous_sentence)
                       else: 
                          print("closest reference", next_referring_expression_in_revised_sentence)
            # de lengte is 1 
            # de lengte is langer dan 1 
        except ValueError: 
            print(referring_expressions_in_revised_pairs)
            print(correct_reference_index_pair)
            print(key)
            print("============to check ==================")


            

        print("======================")
    
    print(counter)
main()