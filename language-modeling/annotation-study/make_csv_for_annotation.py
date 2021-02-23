import json 

import json 
from collections import Counter 
import random
import pandas as pd 
from transformers import OpenAIGPTTokenizer


PATH_TO_FILE = "errors_in_dev.json"
PATH = "already_done.txt"
TOKENIZER = OpenAIGPTTokenizer.from_pretrained('../finetuned-model')



def read_file(path): 
    with open(path, 'r') as file_in: 
         content = file_in.readlines()
    return [elem.strip('\n') for elem in content]

already_done = read_file(PATH)

with open(PATH_TO_FILE, "r") as json_in: 
     data = json.load(json_in)


def format_title(title):
    title = title.replace("_", " ").strip('.txt')
    return "<i> How to {0} </i>".format(title)

def make_dict(generated_line, correct_line, context, filename, correct_seq, generated):
    # pick a number to decide which components will be mentioned first: 0 (base) or 1 (revised)
    element_that_will_be_presented_first = random.choice([0, 1])

    # means that the source is the first one:

 
    if element_that_will_be_presented_first == 0:
        elements = {"Line1": generated_line, "Answer1":generated, "Answer2": correct_seq, "Context1": context.rstrip('\n').replace('\n', '<br />'),
                    "Line2": correct_line, "Context2": context.rstrip('\n').replace('\n', '<br />'), "Info": "generated",
                    "Differences": get_differences(correct_seq, generated, "generated"), "Title": filename}
    else:

        elements = {"Line2": generated_line, "Answer1": correct_seq, "Answer2":  generated, "Context2": context.rstrip('\n').replace('\n', '<br />'),
                    "Line1": correct_line, "Context1":  context.rstrip('\n').replace('\n', '<br />') , "Info": "human-generated",
                    "Differences": get_differences(correct_seq, generated, "human_generated"), "Title": filename}
    return elements

def get_differences(correct_seq, generated, generation_type):
    if generation_type == 'human_generated': 
            output = "{0} <-> {1}".format(correct_seq, generated)
    else: 
            output = "{1} <-> {0}".format(correct_seq, generated)
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

    counter = 0 
    collection = []
    for key, _ in data.items(): 
        if key not in already_done: 
           counter +=1 


        correct_reference = data[key]['reference']
        filename = format_title(data[key]["filename"])
        if type(correct_reference) == list: 
            correct_reference = ' '.join(correct_reference)

        if 'revised_after_insertion' not in data[key].keys(): 
            revised_after_insertion = data[key]['revised_afer_insertion']
        else: 
            revised_after_insertion = data[key]['revised_after_insertion']

        
        correct_line = data[key]['revised_untill_insertion'] + ' ' + "<b>"  +  correct_reference + "</b>"  + ' ' + revised_after_insertion
        generated_sequences = [sequence.lstrip().lower() for sequence in data[key]['predictions']['generated_texts']] 
        first_generated_reference= generated_sequences[0]
        generated_line = data[key]['revised_untill_insertion'] + ' ' + "<b>" + first_generated_reference + "</b>" ' ' + revised_after_insertion

        print(data[key]['par'])
        print('correct line', correct_line)


        context = trunc_text(data[key]['par'].rstrip('\n'))
        row = make_dict(generated_line, correct_line, context, filename, correct_reference, first_generated_reference)
        collection.append(row)

    df = pd.DataFrame(collection)
    #print(df)
    df = df.replace('\n',' ', regex=True)
    df.to_csv('annotation-set-trial.csv', sep=',', index=False, line_terminator=None)
    
    #print(counter)
main()