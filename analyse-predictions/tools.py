
import spacy 
from collections import Counter 

tokenizer = spacy.load('en_core_web_sm')

def check_if_filler_occurs(context, predictions): 
    d = Counter()
 
    # make a dict with tokens     
    tokens_in_context = [token for token in context]
    for token in tokens_in_context: 
        d[token] += 1
    
    d = dict(d)


    # make a dict that indicates how often the filler occurs in the previous context. 
    dict_with_frequencies_per_prediction = {}
    for prediction in predictions: 
        if prediction in d.keys(): 
           dict_with_frequencies_per_prediction[prediction] = d[prediction]
        else: 
            dict_with_frequencies_per_prediction[prediction] = 0 
           
    return dict_with_frequencies_per_prediction
        


def tokenize(text_to_tokenize, ngrams='unigram'): 
    tokenized = [token.text.lower() for token in tokenizer(text_to_tokenize)]
    if ngrams == 'unigram': 
       return tokenized 
    else: 
        tokenized_by_ngram = []
        if ngrams == 'bigram': 
           for i in range(len(tokenized)-1): 
               bigram = tokenized[i] + ' ' + tokenized[i+1]
               tokenized_by_ngram.append(bigram)
        else: 
            for i in range(len(tokenized)-2): 
               trigram = tokenized[i] + ' ' + tokenized[i+1] + ' ' + tokenized[i+2]
               tokenized_by_ngram.append(trigram)
        return tokenized_by_ngram            


def add_pos_tagging(before_reference, filler, after_reference): 
    # add pos tags to the sentence + the reference
    # should return: the pos_tag of the filler 

    sent_to_tag = before_reference + ' ' + filler + ' ' +  after_reference 
    tagged = tokenizer(sent_to_tag)
    return [[token.text, token.tag_] for token in tagged]



if __name__ == "__main__":
   main()