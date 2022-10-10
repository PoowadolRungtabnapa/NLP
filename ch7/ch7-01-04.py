import random

bot_template = "BOT : {0}"

name = "Bot"
weather = "Cloudy"

# Define a dictionary containing a list of responses for each message
responses = {
    "what's your name?" : [
        "my name is {0}".format(name),
        "they call me {0}".format(name),
        "I am {0}".format(name)
    ],
    "what's today's weather?" : [
        "the weather is {0}".format(weather),
        "it's {0}".format(weather)
    ],
    "default" : ["default message"]
}

# Use random.choice() to choose a matching response
def respond(message) :
    # Check if the message is in the responses
    if message in responses :
        # Return a random matching response
        bot_message = random.choice(responses[message])
    else :
        # Return a random "default" response
        bot_message = random.choice(responses["default"])
    return bot_template.format(bot_message)

y = input("Enter Y or y to chat with bot : ")

while y == "Y" or y == "y" :
    print(bot_template.format("HI!"))
    user_message = input("USER : ")
    print(respond(user_message))
    y = input("Enter Y or y to chat with bot : ")