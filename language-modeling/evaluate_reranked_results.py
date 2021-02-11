import json 

PATH_TO_RERANKED_FILE = "results-on-test-set-reranked.json"

with open(PATH_TO_RERANKED_FILE, 'r') as json_in: 
     reranked_results = json.load(json_in)


def compute_overlap(generated_sequences, correct_insertion, top_k=100): 
    "function to check if the reference is in the generated sequences"
    generated_sequences_stripped = [sequence.lstrip() for sequence in generated_sequences]
    generated_sequences_stripped = generated_sequences_stripped[:top_k]

    #print("Top {0}: {1}".format(top_k, generated_sequences_stripped))
    if correct_insertion in  generated_sequences_stripped: 
       return 1 
    else: 
        return 0 

def main():
    total_correct = 0 
    total = 0  
    for key, _ in reranked_results.items(): 
        if reranked_results[key]['Split'] == 'TEST': 
           total +=1 
           total_correct += correct_or_not 
    
    print(total_correct)
    print(total_correct/total)
    





main()
