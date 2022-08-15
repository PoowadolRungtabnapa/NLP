# Import Dictionary
import itertools
from gensim.corpora.dictionary import Dictionary

from collections import Counter
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from collections import defaultdict

from gensim.models.tfidfmodel import TfidfModel

articles = []
for i in range(10) :

    #Read TXT File
    f = open(f".\TextFile\wiki\wiki_article_{i}.txt", "r")
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
    lemmatized = [wordnet_lemmatizer.lemmatize(t) for t in no_stops]

    articles.append(lemmatized)

#Create a Dictionary from the articles : dictionary
dictionary = Dictionary(articles)
'''computer_id = dictionary.token2id.get("computer")'''


#Create a Corpus : corpus
corpus = [dictionary.doc2bow(a) for a in articles]

#Save the second document : doc
doc = corpus[0]

#Create a new TfidfModel using the corpus : tfidf
tfidf = TfidfModel(corpus)

#Calculate the tfidf weight of doc : tfidf_weights
tfidf_weight = tfidf[doc]

#Print the first five weights
#print(tfidf_weight[:5])

#Sort the weights from highest to lowest : sorted_tfidf_weights
sorted_tfidf_weight = sorted(tfidf_weight, key=lambda w: w[1], reverse=True)

#Print the top weighted words
for term_id, weight in sorted_tfidf_weight[:5] :
    print(dictionary.get(term_id), weight)

'''
#sort the doc for frequency : bow_doc
bow_doc = sorted(doc, key=lambda w: w[1], reverse=True)

#Print the top 5 words of the document alongside the count
for word_id, word_count in bow_doc[:5] :
    print("dictionary.get(word_id), word_count")

#Create the defaultdict : total_word_count
total_word_count = defaultdict(int)
for word_id, word_count in itertools.chain.from_iterable(corpus) :
    total_word_count[word_id] += word_count

#Create a sorted list from the defaultdict: sorted_word_count
sorted_word_count = sorted(total_word_count.items(), key=lambda w: w[1],
                            reverse=True)

#Print the top 5 word across all documents alongside the count
for word_id, word_count in sorted_word_count[:5] :
    print(dictionary.get(word_id), word_count)'''