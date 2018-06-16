# sound.py - Play audio.

import playsound

from core import oa
from abilities.core import get, put

def _in():
    while not oa.core.finished.is_set():
        path = get()
        
        # Pause listening while talking. Mute STT.
        put('speech_recognition','mute')
        playsound.playsound(path)
   
        # Audio complete. Begin listening. Unmute STT.
        put('speech_recognition','unmute')
        yield ''
