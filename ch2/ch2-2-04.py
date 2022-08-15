#count frequency word
from multiprocessing.spawn import import_main_path
from matplotlib import pyplot as plt
from nltk.tokenize import word_tokenize, regexp_tokenize
import re
f = open(".\TextFile\holy_grail.txt", "r")
holy_grail = f.read()

lines = holy_grail.split('\n')

pattern = "[A-Z]{2,}(\s)?(#\d)?([A-Z]{2,})?:"
lines = [re.sub(pattern, '', l) for l in lines]

tokenized_lines = [regexp_tokenize(s,"\w+") for s in lines]

line_num_words = [len(t_line) for t_line in tokenized_lines]

plt.hist(line_num_words)
plt.show()