# voice.py - Audio output: Text To Speech (TTS)

import pyttsx3

from oa.core import oa
from oa.modules.abilities.core import get, put


import platform
sys_os = platform.system()
flMac = (sys_os == 'Darwin')
if flMac:
    import subprocess
else:
    import pyttsx3


def _in():
    if not flMac:
        tts = pyttsx3.init()

    while not oa.core.finished.is_set():
        s = get()
        # Pause Ear (listening) while talking. Mute TTS.
        # TODO: move this somewhere else
        put('speech_recognition', 'mute')

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
        # TODO: move this somewhere else
        put('speech_recognition', 'unmute')
