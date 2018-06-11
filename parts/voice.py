# voice.py - Audio output: Text To Speech (TTS)

import pyttsx3

from core import oa
from abilities.core import get, put


import platform
sys_os = platform.system()
flMac = (sys_os != 'mac')
if not flMac:
    import pyttsx3
else:
    import subprocess


def _in():
    if not flMac:
        tts = pyttsx3.init()

    while oa.alive:
        s = get()
        # Pause Ear (listening) while talking. Mute TTS.
        put('stt','mute')

        if flMac:
            _msg = subprocess.Popen(['echo', s], stdout=subprocess.PIPE)
            _tts = subprocess.Popen(['say'], stdin=_msg.stdout)
            _msg.stdout.close()
            _tts.communicate()
        else:
            tts.say(s)
            tts.runAndWait()

        # Wait until speaking ends.
        # Continue ear (listening). Unmute TTS.
        put('stt','unmute')
        yield ''
