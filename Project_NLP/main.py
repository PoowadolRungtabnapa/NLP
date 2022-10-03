from fileinput import filename
from flask import Flask, render_template, request, flash, redirect, url_for
from werkzeug.utils import secure_filename
import os
from gensim.corpora.dictionary import Dictionary

from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords

from gensim.models.tfidfmodel import TfidfModel

import spacy
from spacy import displacy

from flaskext.markdown import Markdown

from transformers import AutoTokenizer, AutoModelForSequenceClassification


app = Flask(__name__)
Markdown(app)
app.secret_key = 'secret'

uploads_dir = "Project_NLP/Upload"
app.config['UPLOAD_FOLDER'] = uploads_dir

model_path = "ch5/fake-news-bert-base-uncased"

model = AutoModelForSequenceClassification.from_pretrained(model_path)
tokenizer = AutoTokenizer.from_pretrained(model_path)

nlp = spacy.load("en_core_web_sm")
status = 0
@app.route('/', methods = ["GET", "POST"])
def index() :
    global filename, Text
    res = Read_file()
    if len(res) != 0 :
        if request.method == "POST" :
            #Upload Function
            if "file" in request.files and request.files['file'].filename != "":
                uploader(request.files['file'])
                print(f"Upload Name : {request.files['file']} Done")
                return redirect('/')

            if "Search" in request.form and status == 0:
                return render_template('index.html', file=res, Text="!!!Select Your Text First!!!", word=["Select Your Text First"], bow=["Select Your Text First"], search="Select File First")

            #Select Function
            if "SF" in request.form :
                filename = request.form.get('SF')
                print('Selection File In Name :',request.form.get('SF'))
                Text = open(f"Project_NLP/Upload/{filename}", "r")
                return functionmenu()
            # Input Text
            if "Input_Text" in request.form :
                Text = request.form.get('Input_Text')
                filename = ""
                print('Input Text Success')
                return functionmenu()
            # Delete Function
            if "DF" in request.form :
                os.remove(f"Project_NLP/Upload/{request.form.get('DF')}")
                return redirect('/')

            if "Search" in request.form and status == 1:
                f = open(f"Project_NLP/Upload/{Text}", "r")
                text = f.read()
                doc = nlp(text)
                articles = Articles(Text)
                print("Pass")
                return render_template('index.html',FileName =f"FileName : {Text}", file=res, Text=displacy.render(doc, style="ent"), word=tfidf_top_5(articles), bow=bow_top_5(articles), search=Search(articles, request.form.get('Search')))
        return render_template('index.html', file=res, Text="!!!Select Your Text First!!!", word=["Select Your Text First"], bow=["Select Your Text First"])
    else :
        if request.method == "POST" :
            if "file" in request.files :
                print("Upload Done")
                uploader(request.files['file'])
                return redirect('/')
            if "Search" in request.form :
                return render_template('index.html', file=["!!!Not Have Any File Here!!!"], Text="!!!Select Your Text First!!!", word=["Select Your Text First"], bow=["Select Your Text First"], search="Upload File and Select File First")
        return render_template('index.html', file=["!!!Not Have Any File Here!!!"], Text="!!!Select Your Text First!!!", word=["Select Your Text First"], bow=["Select Your Text First"])

@app.route('/function', methods=["GET","POST"])
def functionmenu() :
    global filename, Text
     
    # Read File Content
    if filename != "" :
        filecontent = open(f"Project_NLP/Upload/{filename}", "r")
        Text = filecontent.read()
        doc = nlp(Text)
        articles = Articles()
        print(f"Read Content in File : {filename} Success")
        TFIDF = tfidf_top_5(articles)
        BOW = bow_top_5(articles)
        prediction = get_prediction(Text, convert_to_label=True)
        if request.method == "POST" :
            if "checkbox" in request.form :
                options = {"ents": request.form.getlist('checkbox')}
                return render_template('function.html', FileName=filename, TextContent=Text, TFIDF=TFIDF, Bow=BOW, TextContentNer=displacy.render(doc, style="ent", options=options), Prediction=prediction)
            if "search" in request.form :
                print(f"Search : {request.form.get('search')}")
                word = Search(articles,request.form.get('search'))
                return render_template('function.html', FileName=filename, TextContent=Text, TFIDF=TFIDF, Bow=BOW, TextContentNer=displacy.render(doc, style="ent"), searchword=word, Prediction=prediction)
            return render_template('function.html', FileName=filename, TextContent=Text, TFIDF=TFIDF, Bow=BOW, TextContentNer=displacy.render(doc, style="ent"), Prediction=prediction)
        else :
            return render_template('function.html', FileName=filename, TextContent=Text, TFIDF=TFIDF, Bow=BOW, TextContentNer=displacy.render(doc, style="ent"), Prediction=prediction)
    else :
        doc = nlp(Text)
        articles = Articles()
        print(f"Read Content in File : {filename} Success")
        TFIDF = tfidf_top_5(articles)
        BOW = bow_top_5(articles)
        prediction = get_prediction(Text, convert_to_label=True)
        if request.method == "POST" :
            if "checkbox" in request.form :
                options = {"ents": request.form.getlist('checkbox')}
                return render_template('function.html', FileName=filename, TextContent=Text, TFIDF=TFIDF, Bow=BOW, TextContentNer=displacy.render(doc, style="ent", options=options), Prediction=prediction)
            if "search" in request.form :
                print(f"Search : {request.form.get('search')}")
                word = Search(articles,request.form.get('search'))
                return render_template('function.html', FileName=filename, TextContent=Text, TFIDF=TFIDF, Bow=BOW, TextContentNer=displacy.render(doc, style="ent"), searchword=word, Prediction=prediction)
            return render_template('function.html', FileName=filename, TextContent=Text, TFIDF=TFIDF, Bow=BOW, TextContentNer=displacy.render(doc, style="ent"), Prediction=prediction)
        else :
            return render_template('function.html', FileName=filename, TextContent=Text, TFIDF=TFIDF, Bow=BOW, TextContentNer=displacy.render(doc, style="ent"), Prediction=prediction)

def get_prediction(text, convert_to_label=False):
    # prepare our text into tokenized sequence
    inputs = tokenizer(text, padding=True, truncation=True, max_length=512, return_tensors="pt")
    # perform inference to our model
    outputs = model(**inputs)
    # get output probabilities by doing softmax
    probs = outputs[0].softmax(1)
    # executing argmax function to get the candidate label
    d = {
        0: "reliable",
        1: "fake"
    }
    if convert_to_label:
        print("Prediction Success")
        return d[int(probs.argmax())]
    else:
        print("Prediction Success")
        return int(probs.argmax())

def Search(articles, word) :
    article = (articles[1])
    print(len(article))
    if word.lower() in article :
        return f"{word} have {article.count(word.lower())} word."
    return f"Not have {word} word in file."

def Articles() :
    global filename, Text
    articles = [[]]
    if filename != "" :
        f = open(f"Project_NLP/Upload/{filename}", "r")

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

        print(f'Find Word Tokens in File : {filename} Success')

        return articles
    else :

        article = Text

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

        print(f'Find Word Tokens in File : {filename} Success')

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

    print(f'Find Top 5 TF-IDF Success')

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

    print(f'Find Top 5 Bow Success')

    return bow

def Read_file() :
    dir_path  = "Project_NLP/Upload"
    res = []
    for path in os.listdir(dir_path):
        if os.path.isfile(os.path.join(dir_path, path)):
            res.append(path)
    return res

def uploader(f) :
    filename = secure_filename(f.filename)
    f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

if __name__ == '__main__':
    app.run(host="0.0.0.0")