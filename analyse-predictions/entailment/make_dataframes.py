import pandas as pd 
from sklearn.model_selection import train_test_split


USE_IMDB = False 


def main(): 
    if USE_IMDB: 
        df = pd.read_csv('news.csv')
        df = df.drop(['Unnamed: 0'], axis='columns')
        df['titletext'] = df['title'].astype(str)+' '+ df['text'].astype(str)
        train, val_and_test = train_test_split(df, test_size=0.4)
        val, test = train_test_split(val_and_test, test_size=0.5)


        print(val.columns)
        print(df['label'])

        train.to_csv("train_news.csv")
        val.to_csv("val_news.csv")
        test.to_csv("test_news.csv")
    else: 
        df_train = pd.read_csv("./context-dataset/train.csv")
        df_val = pd.read_csv("./context-dataset/validation.csv")
        df_test = pd.read_csv("./context-dataset/test.csv")

        print(df_val)
        print(df_train)
        # om de data te converteren
        print(df_test['semantic_rel'].tolist())

main()