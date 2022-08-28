from ast import Not
from re import search
from flask import Flask, render_template, request, flash, redirect, url_for
from matplotlib import artist
from werkzeug.utils import secure_filename
import os
import time
import itertools
from gensim.corpora.dictionary import Dictionary

from collections import Counter
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from collections import defaultdict

from gensim.models.tfidfmodel import TfidfModel

import spacy
from spacy import displacy

from flaskext.markdown import Markdown

app = Flask(__name__)
Markdown(app)
app.secret_key = 'secret'

uploads_dir = "Web_Ner/Upload"
app.config['UPLOAD_FOLDER'] = uploads_dir

nlp = spacy.load("en_core_web_sm")
status = 0
@app.route('/', methods = ["GET", "POST"])
def index() :
    global status, Text
    res = Read_file()
    if len(res) != 0 :
        if request.method == "POST" :
            if "file" in request.files and request.files['file'].filename != "":
                print(request.files['file'])
                uploader(request.files['file'])
                return redirect('/')
            if "Search" in request.form and status == 0:
                return render_template('index.html', file=res, Text="!!!Select Your Text First!!!", word=["Select Your Text First"], bow=["Select Your Text First"], search="Select File First")
            if "text" in request.form :
                status = 1
                Text = request.form.get('text')
                f = open(f"Web_Ner/Upload/{Text}", "r")
                text = f.read()
                doc = nlp(text)
                articles = Articles(Text)
                return render_template('index.html',FileName =f"FileName : {Text}", file=res, Text=displacy.render(doc, style="ent"), word=tfidf_top_5(articles), bow=bow_top_5(articles), search="No Word")
            if "Search" in request.form and status == 1:
                f = open(f"Web_Ner/Upload/{Text}", "r")
                text = f.read()
                doc = nlp(text)
                articles = Articles(Text)
                print("Pass")
                return render_template('index.html',FileName =f"FileName : {Text}", file=res, Text=displacy.render(doc, style="ent"), word=tfidf_top_5(articles), bow=bow_top_5(articles), search=Search(articles, request.form.get('Search')))
        return render_template('index.html', file=res, Text="!!!Select Your Text First!!!", word=["Select Your Text First"], bow=["Select Your Text First"])
    else :
        if request.method == "POST" :
            if "file" in request.files :
                print("Upload")
                uploader(request.files['file'])
                return redirect('/')
            if "Search" in request.form :
                return render_template('index.html', file=["!!!Not Have Any File Here!!!"], Text="!!!Select Your Text First!!!", word=["Select Your Text First"], bow=["Select Your Text First"], search="Upload File and Select File First")
        return render_template('index.html', file=["!!!Not Have Any File Here!!!"], Text="!!!Select Your Text First!!!", word=["Select Your Text First"], bow=["Select Your Text First"])

def Search(articles, word) :
    article = (articles[1])
    print(len(article))
    if word.lower() in article :
        return f"{word} have {article.count(word.lower())} word."
    return f"Not have {word} word in file."

def Articles(Filename) :
    articles = [[]]
    f = open(f"Web_Ner/Upload/{Filename}", "r")

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

    return articles

def tfidf_top_5(articles) :
   #Create a Dictionary from the articles : dictionary
   dictionary = Dictionary(articles)
   #Create a Corpus : corpus
   corpus = [dictionary.doc2bow(a) for a in articles]

   #Save the second document : doc
   doc = corpus[1]

   #Create a new TfidfModel using the corpus : tfidf
   tfidf = TfidfModel(corpus)

   #Calculate the tfidf weight of doc : tfidf_weights
   tfidf_weight = tfidf[doc]

   #Sort the weights from highest to lowest : sorted_tfidf_weights
   sorted_tfidf_weight = sorted(tfidf_weight, key=lambda w: w[1], reverse=True)

   tfidf_word = []

   for term_id, weight in sorted_tfidf_weight[:5] :
      tfidf_word.append(dictionary.get(term_id))
   return tfidf_word

def bow_top_5(articles) :

   #Create a Dictionary from the articles : dictionary
   dictionary = Dictionary(articles)

   #Create a Corpus : corpus
   corpus = [dictionary.doc2bow(a) for a in articles]

   #Save the second document : doc
   doc = corpus[1]
   
   #sort the doc for frequency : bow_doc
   bow_doc = sorted(doc, key=lambda w: w[1], reverse=True)

   bow = []

   #Print the top 5 words of the document alongside the count
   for word_id, word_count in bow_doc[:5] :
      bow.append(dictionary.get(word_id))

   return bow

def Read_file() :
    dir_path  = "Web_Ner/Upload"
    res = []
    for path in os.listdir(dir_path):
        if os.path.isfile(os.path.join(dir_path, path)):
            res.append(path)
    return res

def uploader(f) :
    filename = secure_filename(f.filename)
    f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

if __name__ == '__main__':
   app.run(debug = True,host="localhost", port="8080")