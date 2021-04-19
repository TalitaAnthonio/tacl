import pandas as pd 
import numpy as np 
from sklearn.model_selection import train_test_split
import torch 
from torchtext.legacy.data import Field, TabularDataset, BucketIterator, Iterator
import torch.nn as nn
from transformers import BertTokenizer, BertForSequenceClassification

PATH_TO_TRAIN = 'train_news.csv'
PATH_TO_VAL = 'val_news.csv'
PATH_TO_TEST = 'test_news.csv'
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

# set model parameters 
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
MAX_SEQ_LEN = 128
PAD_INDEX = tokenizer.convert_tokens_to_ids(tokenizer.pad_token)
UNK_INDEX = tokenizer.convert_tokens_to_ids(tokenizer.unk_token)


# preprocess data 
# Fields

label_field = Field(sequential=False, use_vocab=False, batch_first=True, dtype=torch.float)
text_field = Field(use_vocab=False, tokenize=tokenizer.encode, lower=False, include_lengths=False, batch_first=True,
                   fix_length=MAX_SEQ_LEN, pad_token=PAD_INDEX, unk_token=UNK_INDEX)
fields = [('label', label_field), ('title', text_field), ('text', text_field)]


train, valid, test = TabularDataset.splits(path='.', train=PATH_TO_TRAIN, validation=PATH_TO_VAL,
                                           test=PATH_TO_TEST, format='CSV', fields=fields, skip_header=True)

train_iter = BucketIterator(train, batch_size=16, sort_key=lambda x: len(x.text),
                            device=device, train=True, sort=True, sort_within_batch=True)


print(vars(train.examples[0]))
# Iterators