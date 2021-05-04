import json 


PATH5 = "GPT+P-perplexitytop100.json"


with open("GPTandFinetuning100.json", "r") as json_in: 
     other_info = json.load(json_in)

with open("GPT+P-perplexitytop100.json", "r") as json_in: 
     data = json.load(json_in)




def check_matches(correct_reference, predictions): 
    if correct_reference.lower() in predictions: 
       return 1 
    else: 
        return 0 


def main(): 
    counter = 0
    # total length = 313 
    fifty_instances_with_human_inserted = {}

    # total length = 137 
    fifty_instances_without_human_inserted = {}
    for key, _ in data.items():
        predictions = [prediction.strip() for prediction in data[key]["GPT+P-perplexityPred"]]
        correct_or_not = data[key]["GPT+P-perplexityCorr"]
        if correct_or_not: 
            counter +=1

            # take the top 1 (here: human-inserted) and the second best one. 
            fifty_instances_with_human_inserted[key] = {"Answer1": predictions[0], "Answer2": predictions[1], "OtherInfo": "human-inserted", "CorrectRef": other_info[key]["CorrectReference"] }
        else: 
            # TODO: check the position of the correct answer. 

            # take the top 1 and the second best one 
            occurs_in_top_10 = check_matches(other_info[key]["CorrectReference"], predictions[0:10])
            if occurs_in_top_10 == 1: 
                
                fifty_instances_without_human_inserted[key] = {"Answer 1": predictions[0], "Answer2": predictions[1], "OtherInfo": "not-human-inserted"}
            

   
    print(len(fifty_instances_with_human_inserted.keys()))
    print(len(fifty_instances_without_human_inserted.keys()))


    with open("with_human_inserted.json", "w") as json_out: 
         json.dump(fifty_instances_with_human_inserted, json_out)
    
    with open("without_human_inserted.json", "w") as json_out: 
         json.dump(fifty_instances_with_human_inserted, json_out)
main()