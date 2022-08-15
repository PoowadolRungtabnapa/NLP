from multiprocessing.spawn import import_main_path
#split line
from matplotlib import pyplot as plt
from nltk.tokenize import word_tokenize

f = open(".\TextFile\holy_grail.txt", "r")
holy_grail = f.read()

lines = holy_grail.split('\n')
