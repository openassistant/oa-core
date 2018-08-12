# sound.py - Play audio.

import logging

import playsound

from oa.core import oa
from oa.modules.abilities.core import get, put

def _in():
    while not oa.core.finished.is_set():
        path = get()
        
        # Pause listening while talking. Mute STT.
        put('speech_recognition','mute')

        try:
            playsound.playsound(path)
        except Exception as ex:
            logging.error("Error playing sound: {}".format(ex))
   
        # Audio complete. Begin listening. Unmute STT.
        put('speech_recognition','unmute')
