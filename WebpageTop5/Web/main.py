from ast import Not
from flask import Flask, render_template, request, flash, redirect, url_for
from matplotlib import artist
from werkzeug.utils import secure_filename
import os

import itertools
from gensim.corpora.dictionary import Dictionary

from collections import Counter
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from collections import defaultdict

from gensim.models.tfidfmodel import TfidfModel

app = Flask(__name__)
app.secret_key = 'secret'

uploads_dir = "./Testupload"
app.config['UPLOAD_FOLDER'] = uploads_dir

@app.route('/', methods = ["GET", "POST"])
def index() :
   global filename, numberfile, articles
   dir_path  = r"./Testupload"
   res = []
   for path in os.listdir(dir_path):
      if os.path.isfile(os.path.join(dir_path, path)):
         res.append(path)

   articles = Articles(res)
   if len(res) != 0 :
      if request.method == "POST" and "subject" in request.form :
         if request.form["subject"] == "Back" :
            return render_template("index.html", file=res, Search="")
         else :
            filename = request.form.get("subject")
            numberfile = res.index(request.form.get("subject"))
            return topword()
      if request.method == "POST" and "delete" in request.form :
         if request.form["delete"] in res :
            os.remove(f"./Testupload/{request.form.get('delete')}")
            return redirect("/")
      return render_template('index.html', file=res, fl="")
   else :
      return render_template('index.html', file=res, fl="Not Have Any File")

def Articles(res) :
   articles = [[]]
   for i in res :
      f = open(f".\Testupload\{i}", "r")

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

@app.route('/topword', methods = ["GET", "POST"])
def topword() :
   global filename, numberfile, articles
   if request.method == "POST" and "Search" in request.form :
      word = str(request.form.get("Search"))
      return render_template('topword.html', word=tfidf_top_5(numberfile, articles), bow=bow_top_5(numberfile, articles), file=filename, search=Search(articles, numberfile, word))
   
   return render_template('topword.html', word=tfidf_top_5(numberfile, articles), bow=bow_top_5(numberfile, articles), file=filename, search="")

def Search(articles, numberfile, word) :
   article = []
   article.append(articles[numberfile + 1])
   dictionary = Dictionary(article)
   Word = dictionary.token2id.get(word.lower())
   return dictionary.get(Word)

def tfidf_top_5(numberfile, articles) :
   #Create a Dictionary from the articles : dictionary
   dictionary = Dictionary(articles)
   #Create a Corpus : corpus
   corpus = [dictionary.doc2bow(a) for a in articles]

   #Save the second document : doc
   doc = corpus[numberfile + 1]

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

def bow_top_5(numberfile, articles) :

   #Create a Dictionary from the articles : dictionary
   dictionary = Dictionary(articles)

   #Create a Corpus : corpus
   corpus = [dictionary.doc2bow(a) for a in articles]

   #Save the second document : doc
   doc = corpus[numberfile + 1]
   
   #sort the doc for frequency : bow_doc
   bow_doc = sorted(doc, key=lambda w: w[1], reverse=True)

   bow = []

   #Print the top 5 words of the document alongside the count
   for word_id, word_count in bow_doc[:5] :
      bow.append(dictionary.get(word_id))

   return bow

@app.route('/upload', methods = ['GET', 'POST'])
def upload_file():
   return render_template('upload.html')

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_files():
   if request.method == 'POST' and 'file' in request.files :
      f = request.files['file']
      f.save(os.path.join(uploads_dir, secure_filename(f.filename)))
      return redirect('/')
   else :
      return redirect('/')
		
if __name__ == '__main__':
   app.run(debug = True,host="localhost", port="8080")