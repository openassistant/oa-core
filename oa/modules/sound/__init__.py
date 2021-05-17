# sound.py - Play audio.

import logging
_logger = logging.getLogger(__name__)

import playsound


def _in(ctx):
    while not ctx.finished.is_set():
        path = ctx.get('sound')
        
        # Pause listening while talking. Mute STT.
        ctx.put('speech_recognition','mute')

        try:
            playsound.playsound(path)
        except Exception as ex:
            _logger.error("Error playing sound: {}".format(ex))

        # Audio complete. Begin listening. Unmute STT.
        ctx.put('speech_recognition','unmute')
