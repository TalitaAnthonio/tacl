from lm_scorer import GPTScorer
from transformers import OpenAIGPTLMHeadModel, OpenAIGPTTokenizer

tokenizer = OpenAIGPTTokenizer.from_pretrained('openai-gpt')
model = OpenAIGPTLMHeadModel.from_pretrained('openai-gpt', return_dict=True).eval()

PATH_TO_FILE_IN = ""
PATH_TO_FILE_OUT = ""

with open(PATH_TO_FILE_IN, "r") as json_in: 
     data = json.load(json_in)


def compute_perplexity(generated_sequences): 
    generated_sequences_with_perplexity_plus_revised_collection = []
    for rank, sequence, insertion in generated_sequences:  
        # bereken de perplexity 
        perplexity_for_sentence = GPTScorer(tokenizer, model, sequence=sequence).get_perplexity()
        generated_sequences_with_perplexity_plus_revised_collection.append([rank, sequence, insertion, perplexity_for_sentence])
    generated_sequences_with_perplexity_plus_revised_collection.sort(key=lambda x: x[-1], reverse=False)
    return generated_sequences_with_perplexity_plus_revised_collection 


def rerank_using_perplexity(sequences, revised_untill_insertion, revised_afer_insertion): 
    # everything up to the insertion 
    revised_untill_insertion = revised_sentence[:index]
    revised_sentence_right = revised_sentence[index+1:]
    generated_sequences_within_sentence = []
    for position, generated_sequence in enumerate(sequences, 1): 
        full_sequence_with_generated_insertion = "{0} {1} {2}".format(' '.join(revised_untill_insertion), generated_sequence.lstrip(), ' '.join(revised_sentence_right))
        generated_sequences_within_sentence.append([position, full_sequence_with_generated_insertion, generated_sequence])
    
    rerank_with_perplexity = compute_perplexity(generated_sequences_within_sentence)
    return [elem[2] for elem in rerank_with_perplexity]

def main(): 

    data_with_ranked_results = {}
    for key, _ in data.items(): 
        reranked = rerank_using_perplexity(data[key]['generated_sequences'], data[key]['revised_untill_insertion'], data[key]['revised_after_insertion']) 
        data_with_ranked_results[key] = data[key]
        data_with_ranked_results[key]['generated_sequences_reranked'] = reranked
    

    #with open(PATH_TO_FILE_OUT, 'w') as json_out: 
    #    json.dump(data_with_ranked_results, json_out)
    

main()