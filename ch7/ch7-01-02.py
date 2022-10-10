bot_template = "BOT : {0}"
user_template = "USER : {0}"

# Define a function that sends a message to the bot : send_message
def send_message(message) :
    # Print user_template including the user_message
    print(user_template.format(message))
    
    # Get th bot's response to the message
    response = respond(message)

    # Print the bot template including the bot's response.
    print(bot_template.format(response))

# Define a function that responds to a user's message : respond
def respond(message) :
    # Concatenate the user's message to the end of a standard bot response
    bot_message = "I can hear you! You said : " + message

    # Return the result
    return bot_message

# Send a message to the bot
send_message("hello")