import re
import random

bot_template = "BOT : {0}"

rules = {
    "do you think (.*)" : [
        "if {0}? Absolutely.",
        "No chance"],
    "do you remember (.*)" : [
        "Did you think I would forget {0}",
        "Why haven't you been able to forget {0}",
        "What about {0}",
        "Yes .. and?"],
    "I want (.*)" :[
        "What would it mean if you get {0}",
        "Why do you want {0}",
        "What's stopping you from getting {0}"],
    "if (.*)" : [
        "Do you really think it's likely that {0}",
        "Do you wish that {0}",
        "What do you think about {0}",
        "Really--if {0}"]
}

def send_message(message) :
    # Check if the message is in the responses
    bot_message = respond(message)
    return bot_template.format(bot_message)


# Define respond()
def respond(message) :

    response = match_rule(rules, message)
    phrase = match_rule(rules, message)
    
    if "{0}" in response :
        # Replace the pronouns in the phrase
        phrase = replace_pronouns(phrase)

        # Include the phrase in the response
        response = response.format(phrase)
    return print(bot_template.format(response))

# Define match_rule()
def match_rule(rules, message) :
    response, phrase = "default", None

    # Iterate over the rules dictionary
    for i, j in rules.items() :
        # Create a match object
        match = re.search(i, message)
        if match is not None :
            # Choose a random response
            response = random.choice(j)
            if '{0}' in response :
                phrase = match.group(1)
    
    # Return the response and phrase
    return response.format(phrase)

# Define replace_pronouns()
def replace_pronouns(message) :
    message = message.lower()
    if 'me' in message :
        # Replace 'me' with 'you'
        return re.sub("me", "you", message)
    if 'my' in message :
        # Replace 'my' with 'your'
        return re.sub("my", "your", message)
    if 'your' in message :
        # Replace 'your' with 'my'
        return re.sub("your", "my", message)
    if 'you' in message :
        # Replace 'you' with 'me'
        return re.sub("you", "me", message)
    return message

# Send the messages
for i in range(0,4) :
    send_message(input("USER : "))