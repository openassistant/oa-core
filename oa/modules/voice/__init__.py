# voice.py - Audio output: Text To Speech (TTS)

import logging
_logger = logging.getLogger(__name__)

import pyttsx3


import platform
sys_os = platform.system()
flMac = (sys_os == 'Darwin')
if flMac:
    import subprocess
else:
    import pyttsx3


def _in(ctx):
    if not flMac:
        tts = pyttsx3.init()

    while not ctx.finished.is_set():
        s = ctx.get('voice')
        _logger.debug("Saying: %s", s)

        # Pause Ear (listening) while talking. Mute TTS.
        # TODO: move this somewhere else
        ctx.put('speech_recognition', 'mute')

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
        ctx.put('speech_recognition', 'unmute')
