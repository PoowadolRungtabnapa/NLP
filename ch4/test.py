# Import Dictionary
import itertools
from math import comb
from gensim.corpora.dictionary import Dictionary

from collections import Counter
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from collections import defaultdict

from gensim.models.tfidfmodel import TfidfModel

articles = []
#Read TXT File
f = open(f".\TextFile\wiki\wiki_article_1.txt", "r")
article = f.read()

#Tokenize the article : tokens
tokens = word_tokenize(article)

#Convert the tokens into lowercase : lower_tokens
lower_tokens = [t.lower() for t in tokens]

#Retain alphabetic words : alpha_only
alpha_only = [t for t in lower_tokens if t.isalpha()]

#Remove all stop words : no_stops
no_stops = [t for t in alpha_only if t not in stopwords.words('english')]

# Instantiate the WordNetLemmatizer
wordnet_lemmatizer = WordNetLemmatizer()

#Lemmatize all tokens into a new list : lemmatized
articles = [wordnet_lemmatizer.lemmatize(t) for t in no_stops]

a = []

print(len(a))
#Create a Dictionary from the articles : dictionary
#dictionary = Dictionary(articles)
#computer_id = dictionary.token2id.get("computer")
word_counts = Counter(articles)

#print(computer_id)
print(word_counts["computer"])
#print(dictionary.get(computer_id))