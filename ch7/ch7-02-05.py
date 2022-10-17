import pyttsx3
import speech_recognition as sr
import webbrowser
import datetime

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

def greeting() :
    # This is a simple greeting and
    # it informs the user that the
    # assistant has started

    assistant("Hello, I am your Virtual Assistant. How Can I Help You")

def core_code() :
    # First, we will call greeting
    # to mark the starting
    greeting()

core_code()
print("Success")