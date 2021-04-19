import pandas as pd 
import numpy as np 
from sklearn.model_selection import train_test_split


df = pd.read_csv('news.csv')
train, val_and_test = train_test_split(df, test_size=0.4)
val, test = train_test_split(val_and_test, test_size=0.5)
print(train)
print(val)
print(test)