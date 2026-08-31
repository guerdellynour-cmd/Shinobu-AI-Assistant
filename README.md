# Shinobu-AI-Assistant

Shinobu is a voice assistant I built using Python and Eel, with a simple animated web UI on the front end. You talk to it, it listens, and it can open apps, open websites, or play something on YouTube.

## What it does

- Listens through your mic and converts speech to text using Google's speech recognition
- Talks back to you using text-to-speech (pyttsx3)
- Opens apps or sites by name - checks a local SQLite database first, falls back to the OS if it's not found
- Plays songs/videos on YouTube on command
- Has a simple animated loader UI with glowing text, built with Textillate.js

## Built with

Backend:
- Python
- Eel (connects the Python backend to the HTML/JS frontend)
- SpeechRecognition
- pyttsx3
- pywhatkit
- sqlite3

Frontend:
- HTML/CSS
- Bootstrap 5
- jQuery
- Textillate.js

## Project structure

Shinobu/
├── main.py
├── engine/
│ ├── command.py # listens and processes voice commands
│ ├── config.py # assistant config
│ ├── db.py # database setup for apps/websites
│ └── features.py # open apps/sites, play YouTube, etc.
└── www/
├── index.html
├── main.js
├── style.css
└── assets/ # icons, audio, and vendor libraries


## Setup

1. Clone this repo
```bash
git clone https://github.com/guerdellynour-cmd/Shinobu-AI-Assistant.git
cd Shinobu-AI-Assistant
```

2. Create a virtual environment
```bash
python -m venv envShinobu
envShinobu\Scripts\activate
```

3. Install what you need
```bash
pip install eel pyttsx3 SpeechRecognition pywhatkit playsound
```

4. Run it
```bash
python main.py
```

## Adding your own apps/sites

Open `engine/db.py` and add entries like this:
```python
query = "INSERT INTO sys_command VALUES (null,'AppName', 'C:\\path\\to\\App.exe')"
```

## How to use it

Click the mic and try things like:
- "open spotify"
- "open [some website]"
- "play [song name] on youtube"
