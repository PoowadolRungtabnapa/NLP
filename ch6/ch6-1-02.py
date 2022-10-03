# Import the required packages
from typing import Text
from textblob import TextBlob

text = "You are not beautiful"

# Create a textblob object
blob_two_cities = TextBlob(text)

# Print out the sentiment
print(blob_two_cities.sentiment)