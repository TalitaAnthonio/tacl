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
            print("correct reference", correct_reference_index_pair)

            # if there is just one refererring expression in the revised sentence (which should be the human-inserted one), take the closest referring expression of the previous sentence. 
            if len(referring_expressions_in_revised_pairs) == 1: 
               referring_expressions_in_previous_sentence = sorted(reference_index_list[sentence_indexes[1]]["reference"], key=lambda x:x[-1], reverse=True)[0][0]
               print("closest_reference", referring_expressions_in_previous_sentence)
               closest_reference = referring_expressions_in_previous_sentence
            else: 
               # TODO: if there is only the revised sentence 
               if len(sentence_indexes) == 1: 
                  # if it's at the end 
                  if position_of_correct_reference == len(referring_expressions_in_revised_pairs) - 1: 
                     print("closest reference", referring_expressions_in_revised_pairs[position_of_correct_reference-1])
                     closest_reference = referring_expressions_in_revised_pairs[position_of_correct_reference-1]
                  elif position_of_correct_reference == 0: 
                     print("closest reference", referring_expressions_in_revised_pairs[position_of_correct_reference+1])
                     closest_reference = referring_expressions_in_revised_pairs[position_of_correct_reference+1]
                  else: 
                     right_most = referring_expressions_in_revised_pairs[position_of_correct_reference+1]
                     left_most = referring_expressions_in_revised_pairs[position_of_correct_reference-1]
                     right_most_distance = abs(position_of_correct_reference - (right_most[-1]) )
                     left_most_distance = abs(position_of_correct_reference - (left_most[-1]) )
                     if right_most > left_most: 
                        print("closest reference", left_most)
                        closest_reference = left_most
                     else: 
                        print("closest reference", right_most)
                        closest_reference = right_most

               else: 
                    # check the closest referring expression in the previous sentence 
                    closest_referring_expression_in_the_previous_sentence = sorted(reference_index_list[sentence_indexes[1]]["reference"], key=lambda x:x[-1], reverse=True)[0]
                    sentence_length_of_previous_sentence = reference_index_list[sentence_indexes[1]]["sentlength"]
                    # ---------------------------------------- if the position of the reference is 0 ----------------------------------------------------------
                    if position_of_correct_reference == 0: 
                       next_referring_expression_in_revised_sentence = sorted(reference_index_list[sentence_indexes[0]]["reference"], key=lambda x:x[-1], reverse=True)[1]
                       absolute_distance_between_ref_in_same = abs(correct_reference_index_pair[-1] - next_referring_expression_in_revised_sentence[-1])
    
                       absolute_distance_between_ref_in_prev = abs(abs(sentence_length_of_previous_sentence - closest_referring_expression_in_the_previous_sentence[-1]) + (correct_reference_index_pair[-1])) 
                       


                       if absolute_distance_between_ref_in_same > absolute_distance_between_ref_in_prev: 
                          print("closest reference", closest_referring_expression_in_the_previous_sentence)
                          closest_reference = closest_referring_expression_in_the_previous_sentence
                       else: 
                          print("closest reference", next_referring_expression_in_revised_sentence)
                          closest_reference = next_referring_expression_in_revised_sentence
                    
                    # ---------------------------------------- if the position of the reference is at the end, just take the previous one ----------------------------------------------------------
                    elif position_of_correct_reference == len(referring_expressions_in_revised_pairs)-1: 
                        print("closest reference", referring_expressions_in_revised_pairs[position_of_correct_reference-1])
                        closest_reference = referring_expressions_in_revised_pairs[position_of_correct_reference-1]
                    
                    # if the reference is in the middle, take the left and rightmost 
                    else: 
                        left_most_expression = referring_expressions_in_revised_pairs[position_of_correct_reference-1]
                        right_most_expression = referring_expressions_in_revised_pairs[position_of_correct_reference+1]
                        distance_to_left = abs(correct_reference_index_pair[-1] - left_most_expression[-1])
                        distance_to_right = abs(correct_reference_index_pair[-1] - right_most_expression[-1])
                        if distance_to_left > distance_to_right: 
                           print("closest reference", distance_to_right, right_most_expression)
                           closest_reference = right_most_expression[0]
                        else: 
                           print("closest reference", distance_to_left, left_most_expression)
                           closest_reference = left_most_expression[0]


            #if closest_reference[0]
            if type(closest_reference[0]) == list: 
               closest_reference = closest_reference[0] 
            
            print(" ".join(closest_reference).lower(), correct_reference)
            if " ".join(closest_reference).lower() == correct_reference: 
               counter +=1
               print("the same! ") 

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