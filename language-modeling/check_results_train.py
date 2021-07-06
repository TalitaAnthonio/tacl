import json
import pdb 


def read_json_lines(path_to_json_lines):
    d = {} 
    with open(path_to_json_lines) as json_lines_file: 
         for line in json_lines_file: 
             line = json.loads(line)
             d[line['key']] = line

    return d 


def check_matches(correct_ref, generated_list): 
    if correct_ref.lower() in generated_list[0:10]: 
        return 1 
    else: 
        return 0 


with open("../data/references_for_lm.json", "r") as json_in: 
     all_data = json.load(json_in)


def main():
    total = 0 
    all_total = 0 
    data = read_json_lines("test_train.json")
    for key, _ in data.items(): 
        reference = all_data[key]['reference']
        if type(reference) == list: 
           reference = " ".join(reference)
        
        if type(data[key]["predictions"]) == dict: 
            predictions = data[key]["predictions"]["generated_texts"]
            predictions = [elem.strip().lower() for elem in predictions]
            res = check_matches(reference, predictions)
            print(predictions, reference, res)
            all_total +=1 
            total += res 
    
    print(total)
    print(all_total)
            
    
main()