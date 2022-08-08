from collections import Counter
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords

j = open("./TextFile/wiki_java.txt","r")
h = open("./TextFile/wiki_html.txt","r")
p = open("./TextFile/wiki_python.txt","r")
m = open("./TextFile/wiki_mongodb.txt","r")
s = open("./TextFile/wiki_sql_injection.txt","r")

def main(f) : 
    article = f.read()

    #---Find tokens in tokenize---#
    tokens = word_tokenize(article)

    #---Counvert to LowerCase---#
    lower_tokens = [t.lower() for t in tokens]

    #---Count tokens---#
    bow_simple = Counter(lower_tokens)

    #---Filter the alphabet in tokens---#
    alpha_only = [t for t in lower_tokens if t.isalpha()]

    #---Filter the stopwords in alpha_only---#
    no_stops = [t for t in alpha_only if t not in stopwords.words('english')]

    wordnot_lemmatizer = WordNetLemmatizer()
    #---Use Lemmatizer in no_stops---#
    lemmatized = [wordnot_lemmatizer.lemmatize(t) for t in no_stops]

    bow = Counter(lemmatized)
    print(bow.most_common(10))

articles = []
for i in j,h,p,m,s :
    articles.append(main(i))
