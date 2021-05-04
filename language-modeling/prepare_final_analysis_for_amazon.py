import json 
import pdb
import random 
from collections import Counter 
import random
import pandas as pd 
from transformers import OpenAIGPTTokenizer

random.seed(10)


 #TODO: make sure that the csv is shuffled + that the info is kept. 

TOKENIZER = OpenAIGPTTokenizer.from_pretrained('../language-modeling/finetuned-model')

path_to_human_inserted = "with_human_inserted.json"
path_to_non_human_inserted = "without_human_inserted.json"




with open("../data/references_for_lm.json", "r") as json_in: 
     more_info = json.load(json_in)



with open(path_to_human_inserted, "r") as json_in: 
     data = json.load(json_in)

with open(path_to_non_human_inserted, "r") as json_in: 
     data_non_human_inserted = json.load(json_in)


def format_title(title):
    title = title.replace("_", " ").strip('.txt')
    return "<i> How to {0} </i>".format(title)

def make_dict(line1, line2, context, filename, answer1, answer2, human_inserted_or_not):
    """
        Line 1 -> the first one (with answer 1 )
        Line 2 -> the second one (with answer 2)
    """
    # pick a number to decide which components will be mentioned first: 0 (base) or 1 (revised)
    element_that_will_be_presented_first = random.choice([0, 1])

    # means that the source is the first one:

 
    if element_that_will_be_presented_first == 0:
        elements = {"Line1": line1, "Answer1":answer1, "Answer2": answer2, "Context1": context.rstrip('\n').replace('\n', '<br />'),
                    "Line2": line2, "Context2": context.rstrip('\n').replace('\n', '<br />'), "Info": "answer1-first",
                    "Differences": get_differences(answer1, answer2), "Title": filename, "human-inserted-or-not": human_inserted_or_not}
    else:

        elements = {"Line2": line1, "Answer1": answer2, "Answer2":  answer1, "Context2": context.rstrip('\n').replace('\n', '<br />'),
                    "Line1": line2, "Context1":  context.rstrip('\n').replace('\n', '<br />') , "Info": "answer2-first",
                    "Differences": get_differences(answer2, answer1), "Title": filename, "human-inserted-or-not": human_inserted_or_not}
    return elements

def get_differences(correct_seq, generated): 
    output = "{0} <-> {1}".format(correct_seq, generated)
    return output 


def trunc_text(text): 
    inputs = TOKENIZER.encode(text, add_special_tokens=False, return_tensors="pt") 
    inputs_truncated = inputs.tolist()[0]

    tokenized_text = []
    total_length = 0 
    if len(inputs_truncated) >= 512: 
       context_line_splitted = text.split('\n')
       context_line_splitted.reverse()
       for sent in context_line_splitted: 
           tokenized_sent = TOKENIZER.encode(sent, add_special_tokens=False, return_tensors="pt") 
           total_length += len(tokenized_sent.tolist()[0])
           #print(total_length)
           if total_length < 510: 
              tokenized_text.append(TOKENIZER.decode(tokenized_sent.tolist()[0]))
       tokenized_text.reverse()
       return ' '.join(tokenized_text)
    else: 
        return text



def main(): 
    # count how often together 
    keys_in_human_inserted = list(data.keys())[0:50]
    other_keys = list(data_non_human_inserted.keys())[0:50]
    random.shuffle(keys_in_human_inserted)
    random.shuffle(other_keys)

    sample_from_human_inserted = keys_in_human_inserted[0:50]
    sample_from_other = other_keys[0:50]
    all_keys = sample_from_human_inserted + sample_from_other


    data.update(data_non_human_inserted)
    filtered = {key: value for key, value in data.items() if key in all_keys}

    counter = 0 
    collection = []
    for key, _ in filtered.items(): 
        answer1 = filtered[key]['Answer1']
        answer2 =  filtered[key]['Answer2']
        # human-inserted or not-human-inserted
        info = filtered[key]['OtherInfo']
        filename = format_title(filtered[key]["filename"])


        revised_after_insertion = filtered[key]['revised_after_insertion']

        
        line1 = filtered[key]['revised_untill_insertion'] + ' ' + "<b>"  +  answer1 + "</b>"  + ' ' + revised_after_insertion
        line2 = filtered[key]['revised_untill_insertion'] + ' ' + "<b>"  +  answer2 + "</b>"  + ' ' + revised_after_insertion


        context = trunc_text(filtered[key]['par'].rstrip('\n'))
        if context == "": 
           context = data[key]['par'].rstrip('\n')

        row = make_dict(line1, line2, context, filename, answer1, answer2, info)
        collection.append(row)

    df = pd.DataFrame(collection)
    print(df)
    df = df.replace('\n',' ', regex=True)
    df.to_csv('annotation-set-trial-may.csv', sep=',', index=False, line_terminator=None)
    
    #print(counter)
main()