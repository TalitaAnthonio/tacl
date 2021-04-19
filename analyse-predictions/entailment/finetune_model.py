import pandas as pd 
import numpy as np 
from sklearn.model_selection import train_test_split


df = pd.read_csv('news.csv')
train, val_and_test = train_test_split(df, test_size=0.4)
val, test = train_test_split(val_and_test, test_size=0.5)

train.to_csv("train_news.csv")
val.to_csv("val_news.csv")
test.to_csv("test_news.csv")