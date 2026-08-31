import os
import re
import webbrowser

import eel
from playsound import playsound

from engine.command import speak
from engine.config import ASSISTANT_NAME
from engine import db
import pywhatkit as kit


# Common sites that work out of the box, so "open youtube" etc. don't
# require adding a shortcut first. Add more here any time.
COMMON_SITES = {
    "youtube": "https://youtube.com",
    "google": "https://google.com",
    "gmail": "https://mail.google.com",
    "github": "https://github.com",
    "facebook": "https://facebook.com",
    "twitter": "https://twitter.com",
    "x": "https://x.com",
    "instagram": "https://instagram.com",
    "whatsapp": "https://web.whatsapp.com",
    "netflix": "https://netflix.com",
    "amazon": "https://amazon.com",
    "reddit": "https://reddit.com",
}


def playAssistantSound():
    music_dir = "www\\assets\\audio\\start_sound.mp3"
    playsound(music_dir)


@eel.expose
def playClickSound():
    music_dir = "www\\assets\\audio\\click_sound.mp3"
    playsound(music_dir)


def openCommand(query):
    query = query.lower().replace(ASSISTANT_NAME.lower(), "")
    query = query.replace("open", "").strip()

    if query == "":
        return

    try:
        path = db.get_sys_command_path(query)
        if path:
            speak("Opening " + query)
            os.startfile(path)
            return

        url = db.get_web_command_url(query)
        if url:
            speak("Opening " + query)
            webbrowser.open(url)
            return

        if query in COMMON_SITES:
            speak("Opening " + query)
            webbrowser.open(COMMON_SITES[query])
            return

        speak(f"I don't have a shortcut named {query} yet. You can add one from the Settings panel.")

    except Exception as e:
        speak(f"Something went wrong: {str(e)}")


def PlayYoutube(query):
    search_term = extract_yt_term(query)
    if search_term:
        speak("Playing " + search_term + " on YouTube")
        kit.playonyt(search_term)
    else:
        speak("Sorry, I couldn't find what to play on YouTube.")


def extract_yt_term(command):
    pattern = r'play\s+(.*?)\s+on\s+youtube'
    match = re.search(pattern, command, re.IGNORECASE)
    return match.group(1) if match else None


# ---------------- Settings tab API ----------------

@eel.expose
def get_settings():
    return db.get_all_settings()


@eel.expose
def save_settings(data):
    db.save_settings(data)
    return db.get_all_settings()


@eel.expose
def get_shortcuts():
    return {
        "apps": db.get_sys_commands(),
        "web": db.get_web_commands(),
    }


@eel.expose
def add_app_shortcut(name, path):
    if name and path:
        db.add_sys_command(name, path)
    return db.get_sys_commands()


@eel.expose
def add_web_shortcut(name, url):
    if name and url:
        db.add_web_command(name, url)
    return db.get_web_commands()


@eel.expose
def delete_app_shortcut(item_id):
    db.delete_sys_command(item_id)
    return db.get_sys_commands()


@eel.expose
def delete_web_shortcut(item_id):
    db.delete_web_command(item_id)
    return db.get_web_commands()