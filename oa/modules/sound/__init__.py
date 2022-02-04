# sound.py - Play audio.

import logging
_logger = logging.getLogger(__name__)

import playsound

import queue
input_queue = queue.Queue()


def __call__(ctx):
    while not ctx.finished.is_set():
        path = input_queue.get()
        
        # Pause listening while talking. Mute STT.
        # ctx.put('speech_recognition','mute')
        yield "start"

        try:
            playsound.playsound(path)
        except Exception as ex:
            _logger.error("Error playing sound: {}".format(ex))

        # Audio complete. Begin listening. Unmute STT.
        # ctx.put('speech_recognition','unmute')
        yield "stop"
