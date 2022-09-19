import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# load the dataset
news_d = pd.read_csv("./fake-news/train.csv")

# by using df.head(), we can immediately familiarize ourselves with the dataset.
print(news_d.head())