from multiprocessing.spawn import import_main_path
from matplotlib import pyplot as plt
from nltk.tokenize import word_tokenize

words = word_tokenize("This is a pretty cool tool!")
word_lengths = [len(w) for w in words]
print(word_lengths)
plt.hist(word_lengths)

plt.show()