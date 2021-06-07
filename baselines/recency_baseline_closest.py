
# To compute the top closest 

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
    collection = {}
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

            # if there is just one refererring expression in the revised sentence (which should be the human-inserted one), take the referring expressions of all the others 


            sentence_indexes_enumerated = [i for i in range(len(sentence_indexes))][1:] # excludes the revised sentence 
            all_previous_references = []
            if len(referring_expressions_in_revised_pairs) == 1: 
               print("======================================")
               for sentence_position in sentence_indexes_enumerated: 
                   referring_expressions_in_previous_sentence = sorted(reference_index_list[sentence_indexes[sentence_position]]["reference"], key=lambda x:x[-1], reverse=True)
                   reference_in_previous = [elem[0] for elem in referring_expressions_in_previous_sentence]
                   all_previous_references += reference_in_previous

            else: 
                  # if there is only the revised sentence 
                  if len(sentence_indexes) == 1: 
                    # if it's at the end 
                    if position_of_correct_reference == len(referring_expressions_in_revised_pairs) - 1: 
                        # take everything except the last one [[['its'], 16], [['the', 'room'], 12]] -> [[['its'], 16]
                        previous_referring_expressions = referring_expressions_in_revised_pairs[:-1]
                        previous_referring_expressions = [elem[0] for elem in previous_referring_expressions]
                        all_previous_references += reference_in_previous
                    
                    
                    # if it's at the beginning, then take everything up to there 
                    elif position_of_correct_reference == 0: 
                        next_referring_expressions = referring_expressions_in_revised_pairs[1:]
                        next_referring_expressions = [elem[0] for elem in referring_expressions_in_revised_pairs]
                        all_previous_references += next_referring_expressions
                    
                    # if its not in the first and not in the second position. 
                    else: 
                        right_instances = referring_expressions_in_revised_pairs[position_of_correct_reference+1:]
                        left_instances = referring_expressions_in_revised_pairs[:position_of_correct_reference]

                        # check for the right instances 
                        right_instances_sorted = []
                        for elem in right_instances: 
                            distance = abs(correct_reference_index_pair[-1] - (elem[-1]))
                            if distance != 0: 
                               right_instances_sorted.append([elem[0], distance])
                        
                        right_instances_sorted = sorted(right_instances_sorted, key=lambda x:x[-1])

                        # check for the left instances 
                        left_instances_sorted = []
                        for elem in left_instances: 
                            distance = abs(correct_reference_index_pair[-1] - (elem[-1]))
                            if distance != 0: 
                               left_instances_sorted.append([elem[0], distance])
                        
                        left_instances_sorted = sorted(left_instances_sorted, key=lambda x:x[-1])

                        all_sorted_instances = left_instances_sorted + right_instances_sorted
                        all_sorted_instances = sorted(all_sorted_instances, key=lambda x: x[-1])
                        previous_referring_expressions += [elem[0] for elem in all_sorted_instances]
                        
                  
                  
                  #TODO: if there are several 
                  else: 
                    
                    sorted_instances_same_and_previous_sentence = [] 

                    right_instances = referring_expressions_in_revised_pairs[position_of_correct_reference+1:]
                    left_instances = referring_expressions_in_revised_pairs[:position_of_correct_reference]

                    # check for the right instances 
                    right_instances_sorted = []
                    for elem in right_instances: 
                        distance = abs(correct_reference_index_pair[-1] - (elem[-1]))
                        if distance != 0: 
                            right_instances_sorted.append([elem[0], distance])
                    
                    right_instances_sorted = sorted(right_instances_sorted, key=lambda x:x[-1])
                    print("right instances", right_instances_sorted)

                    # check for the left instances 
                    left_instances_sorted = []
                    for elem in left_instances: 
                        distance = abs(correct_reference_index_pair[-1] - (elem[-1]))
                        if distance != 0: 
                            left_instances_sorted.append([elem[0], distance])
                    
                    left_instances_sorted = sorted(left_instances_sorted, key=lambda x:x[-1])
                    print("left instances", left_instances_sorted)

                    all_sorted_instances = left_instances_sorted + right_instances_sorted
                    all_sorted_instances = sorted(all_sorted_instances, key=lambda x: x[-1])
                    sorted_instances_same_and_previous_sentence += all_sorted_instances


                    # check the instances of the previous sentences 
                    sentence_indexes_enumerated = [i for i in range(len(sentence_indexes))][1:] # excludes the revised sentence 
                    
                    referring_expressions_in_previous_sentences = []
                    total_sentence_length = 0 
                    for sentence_position in sentence_indexes_enumerated: 
                        referring_expressions_in_previous_sentence = sorted(reference_index_list[sentence_indexes[sentence_position]]["reference"], key=lambda x:x[-1], reverse=True)
                        sentence_length_of_previous_sentence = reference_index_list[sentence_indexes[sentence_position]]["sentlength"]
                        total_sentence_length += sentence_length_of_previous_sentence
                        for referring_expression in referring_expressions_in_previous_sentence: 

                            # compute the distance to the previous sentence 
                            if sentence_position == 1: 
                               distance = abs(abs(sentence_length_of_previous_sentence - referring_expression[-1]) + (correct_reference_index_pair[-1])) 
                            else: 
                               distance = abs(abs(sentence_length_of_previous_sentence - referring_expression[-1]) + (correct_reference_index_pair[-1] +  total_sentence_length )) 
                            referring_expressions_in_previous_sentences.append([referring_expression[0], distance])
                    
                    print("others", referring_expressions_in_previous_sentences)
                    sorted_instances_same_and_previous_sentence_all = sorted_instances_same_and_previous_sentence + referring_expressions_in_previous_sentences
                    sorted_instances_same_and_previous_sentence_all_sorted = sorted(sorted_instances_same_and_previous_sentence_all, key=lambda x:x[-1])
                    
                    all_previous_references += [elem[0] for elem in sorted_instances_same_and_previous_sentence_all_sorted ]
                    
                      
                        

            top_previous_references = [" ".join(elem).lower() for elem in  all_previous_references]
            print("top previous references", top_previous_references)
            collection[key] = top_previous_references
            if correct_reference.lower() in top_previous_references: 
               counter +=1 


        except ValueError: 
            print(referring_expressions_in_revised_pairs)
            print(correct_reference_index_pair)
            print(key)
            print("============to check ==================")


            

        print("======================")
    
    print(counter)

    with open("recency_dev.json", "w") as json_out: 
         json.dump(collection, json_out)
main()