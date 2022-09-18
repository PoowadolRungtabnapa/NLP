from importlib import import_module
from spacy import displacy

import spacy

def main(x) :
    nlp = spacy.load('en_core_web_sm')

    f = open(r".\TextFile\tim_cook.txt","r")
    article = f.read()

    doc = nlp(article)

    displacy.serve(doc, style="ent")

    for ent in doc.ents :
        if x == ent.label_ :
            pass
    



x = "c"
while x != "x" :
    x = input("Enter : ")
    main(x)