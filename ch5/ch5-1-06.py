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

#Import WordCloud
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt

# load the dataset
news_d = pd.read_csv("ch5/dataset/train.csv")

column_n = ['id', 'title', 'author', 'text', 'label']
remove_c = ['id', 'author']
categorical_features = []
target_col = ['label']
text_f = ['title', 'text']

ps = PorterStemmer()
wnl = nltk.stem.WordNetLemmatizer()

stop_words = stopwords.words('english')
stopwords_dict = Counter(stop_words)

# Removed unused columns
def remove_unused_c(df, column_n=remove_c) :
    df = df.drop(column_n, axis=1)
    return df

# Impute null values with None
def null_process(feature_df) :
    for col in text_f :
        feature_df.loc[feature_df[col].isnull(), col] = "None"
    return feature_df

# Clean Dataset
def clean_dataset(df) :
    # Remove unusd columns
    df = remove_unused_c(df)

    # Impute null values
    df = null_process(df)

    return df

# Cleaning text from unused characters
def clean_text(text) :
    # Removing urls
    text = str(text.replace(r'http[\w:/\.]+', ' '))
    # Remove everything except characters and punctuation
    text = str(text).replace(r'[^\.\w\s]', ' ')
    text = str(text).replace(r'[^a-zA-Z]', ' ')
    text = str(text).replace(r'\s\s+', ' ')
    text = text.lower().strip()
    return text

## NLTK Prerocessing include:
# Stopwords, Stemming and Lemmatization
# For our project we use only Stopwords remove
def nltk_preprocess(text):
    text = clean_text(text)
    wordlist = re.sub(r'[^\w\s]','', text).split()
    text = ' '.join([wnl.lemmatize(word) for word in wordlist if word not in stopwords_dict])

    return text

# Perform data cleaning on train and test dataset by calling clean_dataset function
df = clean_dataset(news_d)

# Apply preprocessing on text through apply method by calling nltk_preprocess function
df["text"] = df.text.apply(nltk_preprocess)

# Apply preprocessing on title through apply method by calling nltk_preprocess
df["title"] = df.title.apply(nltk_preprocess)

# Dataset after cleaning and preprocessing step
print(df.head())

# Initialize the WordCloud
wordcloud = WordCloud(background_color='black', width=800, height=600)

# Generate the word cloud by passing the corpus
text_cloud = wordcloud.generate(' '.join(df['text']))

# Plotting the WordCloud
'''
plt.figure(figsize=(20,30))
plt.imshow(text_cloud)
plt.axis('off')
plt.show()
'''

# Plotting Reliable news only
true_n = ' '.join(df[df['label']==0]['text'])
'''
wc = wordcloud.generate(true_n)
plt.figure(figsize=(20,30))
plt.imshow(wc)
plt.axis('off')
plt.show()
'''

# Plotting Fake news only
fake_n = ' '.join(df[df['label']==1]['text'])
'''
wc = wordcloud.generate(fake_n)
plt.figure(figsize=(20,30))
plt.imshow(wc)
plt.axis('off')
plt.show()
'''

# Function Plot the Most Common Bigram 
def plot_top_ngrams(corpus, title, ylabel, xlabel="Number of Occurences", n=2) :
    #Utility function to plot top n-grams
    true_b = (pd.Series(nltk.ngrams(corpus.split(), n)).value_counts())[:20]
    true_b.sort_values().plot.barh(color='blue', width=.9, figsize=(12, 8))
    plt.title(title)
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    plt.show()

# Plotting the Most Common Bigram on the reliable news

# plot_top_ngrams(true_n, 'Top 20 Frequebtly Occuring True news Bigram', "Bigram", n=2)

# Plotting the Most Common Bigram on the fake news

# plot_top_ngrams(fake_n, 'Top 20 Frequebtly Occuring True news Bigram', "Bigram", n=2)

# Plotting the Most Common Trigram on the fake news

# plot_top_ngrams(fake_n, 'Top 20 Frequebtly Occuring True news Bigram', "Trigram", n=2)

# Plotting the Most Common Trigram on the fake news

# plot_top_ngrams(true_n, 'Top 20 Frequebtly Occuring True news Bigram', "Trigram", n=2)


