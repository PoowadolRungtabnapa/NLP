# Import Dictionary
import itertools
from collections import Counter, defaultdict

from gensim.corpora.dictionary import Dictionary
from gensim.models.tfidfmodel import TfidfModel
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

    #Read TXT File
f = open(f".\TextFile\wiki\wiki_article_8.txt", "r")
article = f.read()

articles = [[]]

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
lemmatized = [wordnet_lemmatizer.lemmatize(t) for t in no_stops]

articles.append(lemmatized)

print(articles)

dictionary = Dictionary(articles)

print(dictionary)

corpus = [dictionary.doc2bow(a) for a in articles]

#Save the second document : doc
doc = corpus[1]

#Create a new TfidfModel using the corpus : tfidf
tfidf = TfidfModel(corpus)

#Calculate the tfidf weight of doc : tfidf_weights
tfidf_weight = tfidf[doc]

#Print the first five weights
#print(tfidf_weight[:5])

computer_id = dictionary.token2id.get("computer")
print(dictionary.get(computer_id))
#Sort the weights from highest to lowest : sorted_tfidf_weights
sorted_tfidf_weight = sorted(tfidf_weight, key=lambda w: w[1], reverse=True)

#Print the top weighted words
for term_id, weight in sorted_tfidf_weight[:5] :
    print(dictionary.get(term_id), weight)

