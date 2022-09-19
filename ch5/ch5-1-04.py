import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# load the dataset
news_d = pd.read_csv("./fake-news/train.csv")

txt_length =  news_d.text.str.split().str.len()
print(txt_length.describe())

sns.countplot(x="label", data=news_d)
print("1: Unreliable")
print("0: Reliable")
print("Distribution of labels:")
print(news_d.label.value_counts())