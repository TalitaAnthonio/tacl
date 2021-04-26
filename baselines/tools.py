
import spacy 
from collections import Counter 
import pdb 

tokenizer = spacy.load('en_core_web_sm')

def make_bow(context, predictions): 
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
    """
        Used to tokenize the context (to check later how often a word occurs)
    """
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


def add_pos_tagging_to_predictions(list_with_predictions): 
    """
        Returns the predictions [[filler, pos tag], but POS tagged]
    """
    tagged_filler_collection = []
    for filler in list_with_predictions: 
        tagged = tokenizer(filler)
        tagged_filler = [token.tag_ for token in tagged]
        tagged_filler_collection.append(tagged_filler)
    return tagged_filler_collection


class Predictions: 

    def __init__(self, predictions, return_value): 
        self.token_predictions = predictions 
        self.tagged_predictions = add_pos_tagging_to_predictions(self.token_predictions)
        self.return_value = return_value
    
    @property 
    def filtered_set(self): 
        if self.return_value == "all": 
           print("use all.")
           return self.token_predictions
        else: 
            noun_fillers = []
            other_fillers = []
            for filler, post_tags_from_filler in zip(self.token_predictions, self.tagged_predictions): 
                if 'NN' in post_tags_from_filler or 'PRP' in post_tags_from_filler or 'PRP$' in post_tags_from_filler or 'NNS' in post_tags_from_filler or 'NNP' in post_tags_from_filler: 
                    noun_fillers.append(filler)
                else: 
                    other_fillers.append(filler)
            return noun_fillers, other_fillers


class RerankedBaselineNounFreq: 

    
    def __init__(self, token_predictions, tagged_predictions): 
        self.token_predictions = token_predictions
        self.tagged_predictions = tagged_predictions