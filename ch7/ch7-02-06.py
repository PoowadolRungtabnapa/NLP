import pyttsx3
import speech_recognition as sr
import webbrowser
import datetime

def audioinput() :
    # this function is all about taking the audio input from the user
    aud = sr.Recognizer()
    with sr.Microphone() as source :
        print('listening and processing')

        # The pause is optional here
        aud.pause_threshold = 0.7
        audio = aud.listen(source)

        # Using try (for valid commands) and exception for when the assistant
        # doesnt "catch" the command
        try :
            print("understanding")
            # en-eu is simply for the accent here english we can use 'en-GB' or 'en-au'
            # for UK and Australian accents
            phrase = aud.recognize_google(audio, language='en-us')
            print("you said : ", phrase)
        except Exception as exp :
            print(exp)
            print("Can you please repeat that")
            return "None"
        
        return phrase

def assistant(audio) :
    engine = pyttsx3.init()

    # getter : To get the current
    # engine property value

    voices = engine.getProperty('voices')

    # setter method
    # [0] for male voice
    # [1] for female voice

    engine.setProperty('voice', voices[1].id)

    # Method governing assistant's speech
    engine.say(audio)

    # Blocks/processes queued commands
    engine.runAndWait()

def core_code() :

    while (True) :
        # changing the query to lowercase
        # ensures it works most of the time
        
        phrase = audioinput().lower()

        if "what is your name" in phrase :
            assistant("I am your nameless virtural assistant")
            continue

        # trigger/condition to exit the program
        elif "bye" in phrase :
            assistant("Exiting. Have a Good Day")
            exit()

core_code()