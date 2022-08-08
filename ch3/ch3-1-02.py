from collections import Counter
from nltk.tokenize import word_tokenize
f = open(".\wiki_article.txt","r")

article = f.read()

#---Find tokens in tokenize---#
tokens = word_tokenize(article)

#---Counvert to LowerCase---#
lower_tokens = [t.lower() for t in tokens]

#---Count tokens---#
bow_simple = Counter(lower_tokens)

#---Find 10 most common tokens---#
print(bow_simple.most_common(10))