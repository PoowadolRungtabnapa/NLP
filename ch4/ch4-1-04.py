from importlib import import_module


import spacy

nlp = spacy.load('en_core_web_sm')

f = open(r".\TextFile\tim_cook.txt","r")
article = f.read()

doc = nlp(article)

for ent in doc.ents :
    print(ent.label_, ent.text)