from cmath import phase
import pyttsx3
import speech_recognition as sr
import webbrowser
import datetime
import wikipedia

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

def theDay() :
    # This function is for the day
    day = datetime.datetime.today().weekday() + 1

    # assigning a number makes it a bit cleaner

    Day_dict = {
        1 : "Monday", 2 : "Tuesday",
        3 : "Wednesday", 4 : "Thursday",
        5 : "Friday", 6: "Saturday",
        7 : 'Sunday'
    }

    if day in Day_dict.keys() :
        weekday = Day_dict[day]
        print(weekday)
    
    assistant("it's " + weekday)

def theTime() :
    # This function is for time
    time = str(datetime.datetime.now())
    # time needs to be sliced for
    # better audio comprehension
    print(time)
    hour = time[11:13]
    min = time[14:16]
    assistant("The time right now is" + hour + "Hours and" + min + "Minutes")

def core_code() :

    while (True) :
        # changing the query to lowercase
        # ensures it works most of the time
        
        # phrase = audioinput().lower()
        phrase = input("Enter : ").lower()

        if "what is your name" in phrase :
            assistant("I am your nameless virtural assistant")
            continue

        elif "what Day is it" in phrase :
            theDay()
            continue

        elif "what time is it" in phrase :
            theTime()
            continue
            
        elif "open google" in phrase :
            assistant("Opening Google")
            webbrowser.open("www.google.com")
            continue
        
        elif "wikipedia" in phrase :
            # to pull information from Wiki
            assistant("checking the wikipedia")
            phrase = phrase.replace("wikipedia", "computer network")

            # it will limit the summary to four lines
            result = wikipedia.summary(phrase, sentences = 4)
            print(result)
            # assistant("As per wikipedia")
            # assistant(result)
            continue

        elif "search" in phrase :

            word = phrase.split(" ")
            print(word.index('search'))
            webbrowser.open("www.google.com/search?q=" + word[word.index('search') + 1])
            continue

        # trigger/condition to exit the program
        elif "bye" in phrase :
            assistant("Exiting. Have a Good Day")
            exit()

        else :
            assistant("I can't find it")
core_code()