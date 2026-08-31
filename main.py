import os
import eel
from engine.features import *
from engine.command import *
from engine.db import init_db

eel.init('www')

init_db()
playAssistantSound()
eel.start('index.html', mode='edge', host='localhost', port=8000, block=True)

# os.system('start chrome.exe --app="http://localhost:8000/index.html"')
# eel.start('index.html', mode='chrome', host='localhost', port=8000, block=True)


# os.system('start opera.exe --app="http://localhost:8000/index.html"')
# eel.start('index.html', mode=None, host='localhost', port=8000, block=True)