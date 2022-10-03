import pandas as pd

movies = pd.read_csv("ch6/data/Train.csv")

# find the number of positive and negative reviews
print("Number of positive and negative reviews : ", movies.label.value_counts())

# Find the proportion of positive and negative reviews
print("Proportion of positive and negative reviews : ", movies.label.value_counts() / len(movies))

length_reviews = movies.text.str.len()

# How long is the longest reviews
print(max(length_reviews))