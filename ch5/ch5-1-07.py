from cProfile import label
from curses import nl
from locale import normalize
from turtle import color, width
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

#Import the essential libraries for analysis

import nltk
from nltk.corpus import stopwords
import re
from nltk.stem.porter import PorterStemmer
from collections import Counter

import torch
from transformers.file_utils import is_tf_available, is_torch_available, is_torch_tpu_available
from transformers import BertTokenizerFast, BertForSequenceClassification
from transformers import Trainer, TrainingArguments
from sklearn.model_selection import train_test_split

import random

#Import WordCloud
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt

# load the dataset
news_d = pd.read_csv("ch5/dataset/train.csv")

def set_seed(seed: int) :
    random.seed(seed)
    np.random.seed(seed)
    if is_torch_available() :
        torch.manual_seed(seed)
        torch.cuda.manual_seed_all(seed)
    
    if is_tf_available() :
        import tensorflow as tf
        tf.random.set_seed(seed)

set_seed(1)

# the model we gonna train, base uncased BERT
# check text classification models here : https://huggingface.co/models?filter=text-classification

model_name = "bert-base-uncased"

# max sequence length for each documnet/sentence sample
max_length = 512

# load the tokenizer
tokenizer = BertTokenizerFast.from_pretrained(model_name, do_lower_case=True)

# Data Preparation
news_df = news_d[news_d['text'].notna()]
news_df = news_d[news_d['author'].notna()]
news_df = news_d[news_d['title'].notna()]

def prepare_data(df, test_size=0.2, include_title=True, include_author=True) :
    texts = []
    labels = []
    for i in range(len(df)) :
        text = df['text'].iloc[i]
        label = df['label'].iloc[i]
        if include_title :
            text = df['title'].iloc[i] + " - " + text
        if include_author :
            text = df['author'].iloc[i] + " : " + text
        if text and label in [0, 1] :
            texts.append(text)
            labels.append(label)
    return train_test_split(texts, labels, test_size=test_size)

train_texts, valid_texts, train_labels, valid_labels = prepare_data(news_df)

print(len(train_texts), len(train_labels))
print(len(valid_texts), len(valid_labels))