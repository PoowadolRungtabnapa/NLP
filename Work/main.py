from flask import Flask, render_template, request, flash, redirect, url_for
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
   if request.method == "POST" :
      print(request.form["subject"])
      if request.form["subject"] == "Upload" :
         return render_template('upload.html')
      if request.form["subject"] == "Word" :
         return render_template('index.html')
   dir_path  = r"./Testupload"
   res = []
   for path in os.listdir(dir_path):
      if os.path.isfile(os.path.join(dir_path, path)):
         res.append(path)

   articles = []
   for i in res :
      f = open(f".\Testupload\{i}", "r")

      article = f.read()

      #Tokenize the article : tokens
      tokens = word_tokenize(article)

      #Convert the tokens into lowercase : lower_tokens
      lower_tokens = [t.lower() for t in tokens]

      bow_simple = Counter(lower_tokens)

      #Retain alphabetic words : alpha_only
      alpha_only = [t for t in lower_tokens if t.isalpha()]

      #Remove all stop words : no_stops
      no_stops = [t for t in alpha_only if t not in stopwords.words('english')]

      # Instantiate the WordNetLemmatizer
      wordnet_lemmatizer = WordNetLemmatizer()

      #Lemmatize all tokens into a new list : lemmatized
      lemmatized = [wordnet_lemmatizer.lemmatize(t) for t in no_stops]

      bow = Counter(lemmatized)
      print(bow.most_common(5))
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
   tfidf_word = []
   #Print the top weighted words
   for term_id, weight in sorted_tfidf_weight[:5] :
      tfidf_word.append(dictionary.get(term_id))

    

   return render_template('index.html', file=res, word=tfidf_word , bow=bow.most_common(5))
   
@app.route('/upload')
def upload_file():
   return render_template('upload.html')

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_files():
   if request.method == 'POST':
      f = request.files['file']
      f.save(os.path.join(uploads_dir, secure_filename(f.filename)))
      return render_template('index.html')
		
if __name__ == '__main__':
   app.run(debug = True,host="localhost", port="8080")