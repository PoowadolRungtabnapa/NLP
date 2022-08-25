from collections import Counter
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from gensim.corpora.dictionary import Dictionary
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

dictionary = Dictionary(articles)

corpus = [dictionary.doc2bow(a) for a in articles]

doc = corpus[1]

bow_doc = sorted(doc, key=lambda w: w[1], reverse=True)

for word_id, word_count in bow_doc[:5] :
    print(dictionary.get(word_id), word_count)

tfidf = TfidfModel(corpus)

tfidf_weights = tfidf[doc]

sorted_tfidf_weights = sorted(tfidf_weights, key=lambda w: w[1], reverse=True)

for term_id, weight in sorted_tfidf_weights[:5] :
    print(dictionary.get(term_id), weight)