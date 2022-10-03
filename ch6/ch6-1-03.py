# Import the required packages
from textblob import TextBlob
import pandas as pd

# Read TXT file
f = open("ch6/data/titanic.txt")
titanic = f.read()

# Create a textblob object
blob_titanic = TextBlob(titanic)

# Print out its sentiment
print(blob_titanic.sentiment)