import re
import pandas as pd
import matplotlib.pyplot as plt
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
nltk.download("vader_lexicon")

df = pd.read_excel("ch6/data/TeamHealthRawDataForDemo.xlsx")

# Adding an row_id field to the dataframe, which will be useful for joining later
df["row_id"] = df.index + 1

# Print first 10 rows
print(df.head(10))