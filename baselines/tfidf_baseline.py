import pandas as pd
from sklearn.feature_extraction.text import TfidfTransformer, TfidfVectorizer
import pdb 
import json 
import spacy 
import pickle 


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
    return [token.text for token in tokenized_text]


dataset = [
    "I enjoy reading about Machine Learning and Machine Learning is my PhD subject",
    "I would enjoy a walk in the park",
    "I was reading in the library"
]


class TfIdf: 

    def __init__(self, data, ngram_value=(2,2)):
        self.vectorizer = TfidfVectorizer(ngram_range=ngram_value, tokenizer=tokenize, smooth_idf=True, sublinear_tf=True)
        self.data = data 
        self.ngram_value = ngram_value 
    
    def vectorize(self): 
        transformed_doc = self.vectorizer.fit_transform(self.data)
        df = pd.DataFrame(transformed_doc[0].T.todense(), index=self.vectorizer.get_feature_names(), columns=["TF-IDF"])
        df = df.sort_values('TF-IDF', ascending=False)
        df_in_dict_format = df.to_dict()
        bow_in_dict_format = {key:value for key, value in df_in_dict_format["TF-IDF"].items()}
        return bow_in_dict_format


def main(): 


    # dict_keys(['GPT+Finetuning+P-perplexityPred', 'GPT+Finetuning+P-perplexityCorr', 'GPT+FinetuningCorrect', 'CorrectReference', 'LeftContext', 'GPTPred', 'GPTCorrect', 'key', 'GPT+FinetuningPred', 'RevisedSentence', 'revised_untill_insertion', 'revised_after_insertion', 'reference-type', 'par', 'index_of_reference'])
    
    # vectorize the development set 
    dev_documents = [development_set[key]["language_model_text"] for key, _ in development_set.items()]
    
    print("Make bow for unigrams ..... ")
    bow_unigrams = TfIdf(dev_documents, ngram_value=(1,1)).vectorize()
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
    
    #print(dev_documents[0])

    #for key, _ in development_set.items(): 


        
    


main()