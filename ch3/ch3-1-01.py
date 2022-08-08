#Use word_tokenize to split word
#Use counter to count word
from nltk.tokenize import word_tokenize
from collections import Counter
counter = Counter(word_tokenize("""The cat is in the box.
The cat likes the box. the box is over the cat."""))
print(counter)

count = counter.most_common(2)
print(count)