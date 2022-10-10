bot_template = "BOT : {0}"
user_template = "USER : {0}"

# Define variables
name = "Bot"
weather = "Cloudy"

# Define a dictionary with the predefined responses
responses = {
    "what's your name?" : "my name is {0}".format(name),
    "what's today's weather?" : "the weather is {0}".format(weather),
    "default" : "default message"
}

# Return the matching response if there is one, default otherwise
def send_message(message) :
    # Check if the message is in the responses
    if message in responses :
        # Return the matching message
        bot_message = responses[message]
    else :
        # Return the "default" message
        bot_message = responses["default"]
    return bot_template.format(bot_message)

print(bot_template.format("HI!"))

user_message = input("USER : ")

print(send_message(user_message))