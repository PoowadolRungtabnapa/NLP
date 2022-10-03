import re
import pandas as pd
import matplotlib.pyplot as plt
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
nltk.download("vader_lexicon")

df = pd.read_excel("ch6/data/TeamHealthRawDataForDemo.xlsx")

# Adding an row_id field to the dataframe, which will be useful for joining later
df["row_id"] = df.index + 1

# Create a new data frame with "id" and "comment" fields
df_subnset = df[["row_id", "Response"]].copy()

# Data clean-up
# Remove all non-aphabet characters
df_subnset["Response"] = df_subnset["Response"].str.replace("[^a-zA-Z#]", " ")

# Convert to lower-case
df_subnset["Response"] = df_subnset["Response"].str.casefold()

print(df_subnset.head(10))