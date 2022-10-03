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

# Set up empty dataframe for staging output
df1 = pd.DataFrame()
df1['row_id'] = ['99999999999']
df1["sentiment_type"] = "NA999NA"
df1["sentiment_score"] = 0

print("Processing sentiment analysis....")
sid = SentimentIntensityAnalyzer()
t_df = df1

for index, row in df_subnset.iterrows() :
    scores = sid.polarity_scores(row[1])

    for key, value in scores.items() : 
        temp = [key, value, row[0]]
        df1['row_id'] = row[0]
        df1["sentiment_type"] = key
        df1["sentiment_score"] = value
        t_df = pd.concat([t_df, df1])

# Remove dummy row with row_id = 9999999999
t_df_cleaned = t_df[t_df.row_id != "99999999999"]

# Remove duplicates if any exist
t_df_cleaned = t_df_cleaned.drop_duplicates()

# Only keep rows where sentiment_type = compound
t_df_cleaned = t_df[t_df.sentiment_type == "compound"]

# Merge Dataframes

df_output = pd.merge(df, t_df_cleaned, on="row_id", how="inner")
print(df_output.head(10))