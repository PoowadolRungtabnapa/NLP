import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# load the dataset
news_d = pd.read_csv("./fake-news/train.csv")

print("Shape of News data : ", news_d.shape)
print("News data columns", news_d.columns)