import random
bot_template = "BOT : {0}"

responses = {
    "question" : [
        "I don't know :(",
        "you tell me!"
        ],
    "statement" : [
        "tell me more!",
        "why do you think that?",
        "how long have you felt this way?",
        "I find that extremely interesting",
        "can you back that up?",
        "oh wow!",
        ":)"
    ]
        }

def send_message(message) :
    # Check if the message is in the responses
    bot_message = respond(message)
    return bot_template.format(bot_message)

def respond(message) :
    # Check for a question mark
    if message.endswith("?") :
        # Return a random question
        return random.choice(responses["question"])
    # Return a random statement
    return random.choice(responses["statement"])

# Send messages ending in a question mark
print(send_message("what's today's weather?"))
print(send_message("what's today's weather?"))
# Send message which don't end with a question mark
print(send_message("I love building chatbots"))
print(send_message("I love building chatbots"))