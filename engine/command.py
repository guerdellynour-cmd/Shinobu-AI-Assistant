import time
import pyttsx3
import speech_recognition as sr
import eel

from engine.db import get_all_settings
from engine.config import ASSISTANT_NAME as DEFAULT_ASSISTANT_NAME


def speak(text):
    settings = get_all_settings()

    engine = pyttsx3.init()
    voices = engine.getProperty('voices')

    try:
        voice_index = int(settings.get('voice_index', 1))
        engine.setProperty('voice', voices[voice_index].id)
    except (IndexError, ValueError, TypeError):
        pass

    try:
        engine.setProperty('rate', int(settings.get('rate', 190)))
    except (ValueError, TypeError):
        engine.setProperty('rate', 190)

    eel.DisplayMessage(text)
    engine.say(text)
    engine.runAndWait()


@eel.expose
def get_available_voices():
    """Lists the TTS voices installed on this machine, for the Settings screen."""
    try:
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        return [{"index": i, "name": v.name} for i, v in enumerate(voices)]
    except Exception:
        return []


def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening...')
        eel.DisplayMessage('Listening...')
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source, timeout=10, phrase_time_limit=6)

    try:
        print('Recognizing...')
        eel.DisplayMessage('Recognizing...')
        query = r.recognize_google(audio, language='en')
        print(f'User said: {query}')
        time.sleep(1)
        eel.DisplayMessage(query)
    except Exception:
        return ""

    return query.lower()


@eel.expose
def takeCommand():
    return listen()


def routeQuery(query):
    """Shared command routing, used by both the mic and the typed chat box."""
    query = (query or "").strip().lower()

    if not query:
        speak("Sorry, I didn't catch that.")
        return

    if 'open' in query:
        from engine.features import openCommand
        openCommand(query)
    elif 'on youtube' in query:
        from engine.features import PlayYoutube
        PlayYoutube(query)
    else:
        speak("I'm not sure how to help with that yet.")


@eel.expose
def allCommands():
    """Entry point for the mic button: listens, then routes the result."""
    query = takeCommand()
    print(query)
    routeQuery(query)
    eel.ShowHood()


@eel.expose
def sendTextCommand(text):
    """Entry point for messages typed into the chat box."""
    routeQuery(text)
    eel.ShowHood()