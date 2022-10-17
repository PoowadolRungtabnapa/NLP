import re

# Define a dictionary 'keywords'.
keywords = {'greet' : ['hello', 'hi', 'hey'], 
            'goodbye' : ['bye', 'farewell'], 
            'thankyou' : ['thank', 'thx']}

# Define a dictionary fo patterns
patterns = {}

# Iterate over the keywords dictionary

for i, k in keywords.items() :
    # Create regular expressions and compile them into pattern objects
    patterns[i] = re.compile('|'.join(k))

# Print the patterns
print(patterns)
