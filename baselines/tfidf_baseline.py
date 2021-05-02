import pandas as pd
from sklearn.feature_extraction.text import TfidfTransformer, TfidfVectorizer
import pdb 
import json 
import spacy 
import pickle 
from nltk.corpus import stopwords

stop_words_list = list(set(stopwords.words('english'))) 

punctuation = [",", ".", "!", "*", "?", "#"]

spacy_model = spacy.load('en_core_web_sm')



path_to_file_with_corefs = "../analyse-predictions/run-coreference/most_frequent_reference_baseline.json"

path_to_file_with_predictions = '../analyse-predictions/bestmodels_predictions.json'

with open(path_to_file_with_predictions, 'r') as json_in: 
     development_set = json.load(json_in)

with open(path_to_file_with_corefs, "r") as json_in: 
     corefs = json.load(json_in)

def check_pos_of_filler(predictions, correct_filler, topk=10): 
    if correct_filler.lower() in predictions[:topk]: 
       return 1 
    else: 
        return 0 


def tokenize(text_to_tokenize): 
    tokenized_text = spacy_model(text_to_tokenize)
    tokens_to_exclude = [",", ".", "!", "*", "?", "#", ":"]

    tokenized = []
    for token in tokenized_text: 
        if token.text not in tokens_to_exclude: 
            tokenized.append(token.text.lower())
    return tokenized




with open("bow_trigrams.pickle", "rb") as pickle_in: 
     trigrams_bow = pickle.load(pickle_in)

with open("bow_bigrams.pickle", "rb") as pickle_in: 
     bigrams_bow = pickle.load(pickle_in)

with open("bow_unigrams.pickle", "rb") as pickle_in: 
     unigrams_bow = pickle.load(pickle_in)


class TfIdf: 

    def __init__(self, data, ngram_value=(2,2), stop_words_value=None):
        self.vectorizer = TfidfVectorizer(ngram_range=ngram_value, tokenizer=tokenize, lowercase=True, use_idf=True, stop_words=stop_words_value)
        self.data = data 
        self.ngram_value = ngram_value 
    
    def vectorize(self): 
        transformed_doc = self.vectorizer.fit_transform(self.data)
        df = pd.DataFrame(transformed_doc[0].T.todense(), index=self.vectorizer.get_feature_names(), columns=["TF-IDF"])
        df = df.sort_values('TF-IDF', ascending=False)
        df_in_dict_format = df.to_dict()
        bow_in_dict_format = {key:value for key, value in df_in_dict_format["TF-IDF"].items()}
        return bow_in_dict_format


def vectorize_data(): 
    """ 
        Used to vectorize the documents again 
    """

    dev_documents = [development_set[key]["language_model_text"] for key, _ in development_set.items()]
    
    print("Make bow for unigrams ..... ")
    bow_unigrams = TfIdf(dev_documents, ngram_value=(1,1), stop_words_value=["the", "a", "to", "and", "or", "of", "and", "in", "if", "on", "can", "be"]).vectorize()
    print(bow_unigrams)

    print("save to file ... ")
    with open("bow_unigrams.pickle", "wb") as pickle_in: 
         pickle.dump(bow_unigrams, pickle_in )
    
    print("Make bow for bigrams")
    bow_bigrams = TfIdf(dev_documents, ngram_value=(2,2)).vectorize()
    with open("bow_bigrams.pickle", "wb") as pickle_in: 
         pickle.dump(bow_bigrams, pickle_in )

    print("Make bow for trigrams ")
    bow_trigrams = TfIdf(dev_documents, ngram_value=(3,3)).vectorize()
    with open("bow_trigrams.pickle", "wb") as pickle_in: 
         pickle.dump(bow_trigrams, pickle_in )



class Tokenizer: 


    def __init__(self, text_to_tokenize, ngram_range=1):
        self.text_to_tokenize = text_to_tokenize 
        self.ngram_range = ngram_range
        self.tokenized_text = tokenize(self.text_to_tokenize) 



    def tokenize(self): 
        if self.ngram_range == 1: 
            return self.tokenized_text 
        else: 
            tokenized_by_ngram = []
            if self.ngram_range == 2: 
                for i in range(len(self.tokenized_text)-1): 
                    bigram = self.tokenized_text[i] + ' ' + self.tokenized_text[i+1]
                    tokenized_by_ngram.append(bigram)
            else: 
                for i in range(len(self.tokenized_text)-2): 
                    trigram = self.tokenized_text[i] + ' ' + self.tokenized_text[i+1] + ' ' + self.tokenized_text[i+2]
                    tokenized_by_ngram.append(trigram)
            return tokenized_by_ngram            


class BowForContext: 

    def __init__(self, tokenized_context, ngram_range):
        self.tokenized_context = tokenized_context
        self.ngram_range = ngram_range 
        if self.ngram_range == 1: 
           self.bow = unigrams_bow
        elif self.ngram_range == 2: 
           self.bow = bigrams_bow
        else: 
           self.bow = trigrams_bow 
    

    def top_instances(self): 
        tf_idf_values_from_context = {token: self.bow[token] for token in self.tokenized_context if token in self.bow.keys()} 
        sorted_values = sorted(tf_idf_values_from_context.items(), key=lambda x: x[1], reverse=True)
        print(sorted_values)
        top_words = [token_freq[0] for token_freq in sorted_values][0:10]
        return top_words



def check_pos_of_filler(predictions, correct_filler, topk=10): 
    if correct_filler.lower() in predictions[:topk]: 
       return 1 
    else: 
        return 0 


def main(): 

    # dict_keys(['GPT+Finetuning+P-perplexityPred', 'GPT+Finetuning+P-perplexityCorr', 'GPT+FinetuningCorrect', 'CorrectReference', 'LeftContext', 'GPTPred', 'GPTCorrect', 'key', 'GPT+FinetuningPred', 'RevisedSentence', 'revised_untill_insertion', 'revised_after_insertion', 'reference-type', 'par', 'index_of_reference'])
    #vectorize_data()
    
    total_correct = 0 

    counter = 0 
    
    for key, _ in development_set.items(): 
        counter +=1 
        print("=========== counter {0} =====================".format(counter))
        correct_ref = tokenize(development_set[key]["CorrectReference"])
        print("tokenize context ... ")
        tokenized_context = Tokenizer(development_set[key]["language_model_text"], ngram_range=len(correct_ref)).tokenize()

        print("make top bow ")
        top_based_on_bow =  BowForContext(tokenized_context, len(correct_ref)).top_instances()
        print(top_based_on_bow)
       
        
        print("check if occurs in baseline ... ") 
        occurs_in_baseline = check_pos_of_filler(top_based_on_bow, development_set[key]["CorrectReference"])
        print("occurs {0}".format(occurs_in_baseline))
        total_correct += occurs_in_baseline

    print(total_correct)
    

main()