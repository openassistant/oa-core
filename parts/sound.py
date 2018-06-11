# sound.py - Play audio.

import playsound

from core import oa
from abilities.core import get, put

def _in():
    while oa.alive:
        path = get()
        
        # Pause listening while talking. Mute STT.
        put('stt','mute')
        playsound.playsound(path)
   
        # Audio complete. Begin listening. Unmute STT.
        put('stt','unmute')
        yield ''
