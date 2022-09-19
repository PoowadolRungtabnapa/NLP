from locale import normalize
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# load the dataset
news_d = pd.read_csv("./fake-news/train.csv")

print(round(news_d.label.value_counts(normalize=True),2)*100)