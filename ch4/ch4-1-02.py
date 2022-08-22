from cProfile import label
from collections import defaultdict
from matplotlib import pyplot as plt
import nltk
from gensim.corpora.dictionary import Dictionary

f = open(r".\TextFile\tim_cook.txt","r")
article = f.read()

sentences = nltk.sent_tokenize(article)

token_sentences = [nltk.word_tokenize(sent) for sent in sentences]

pos_sentences = [nltk.pos_tag(sent) for sent in token_sentences]

#chunked_sentences = nltk.ne_chunk_sents(pos_sentences, binary=True)
chunked_sentences = nltk.ne_chunk_sents(pos_sentences)
#Create the defailtdict: ner_categories
ner_categories = defaultdict(int)

#Create the nested for loop
for sent in chunked_sentences :
    for chunk in sent :
        if hasattr(chunk, 'label') :
            ner_categories[chunk.label()] += 1

#Create a list from the dictionary keys for hte chart labels: lables
labels = list(ner_categories.keys())

#Create a list of the values: values

values = [ner_categories.get(v) for v in labels]

plt.pie(values, labels=labels, autopct="%1.1f%%", startangle=140)

plt.show()

'''for sent in chunked_sentences :
    for chunk in sent :
        if hasattr(chunk, "label") and chunk.label() == "NE" :
            print(chunk)'''
