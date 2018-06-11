# voice.py - Audio output: Text To Speech (TTS)

import pyttsx3

from core import oa
from abilities.core import get, put


def _in():
    tts = pyttsx3.init()
    
    # Set the voice to a German accent.
    # voices = tts.getProperty('voices')
    # tts.setProperty('voice', 'german')
    
    # Set speaking speed rate.
    rate = tts.getProperty('rate')
    tts.setProperty('rate', rate - 28)

    while oa.alive:
        s = get()
        # Pause Ear (listening) while talking. Mute TTS.
        put('stt','mute')

        tts.say(s)
        tts.runAndWait()
        # Wait until speaking ends.
        # Continue ear (listening). Unmute TTS.
        put('stt','unmute')
        yield ''
