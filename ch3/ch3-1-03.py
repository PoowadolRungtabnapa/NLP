from typing import Counter
#---Download Stopwords Data---#
import nltk
nltk.download('stopwords')

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

text = """The cat is in the box. The cat likes the box. The box is 
over the cat."""
#---Find tokens, Split Word, Check a alphabet---#
tokens = [w for w in word_tokenize(text.lower()) if w.isalpha()]
#---Count with out stop word---#
no_stops = [t for t in tokens if t not in stopwords.words('english')]

print(Counter(no_stops).most_common(2))