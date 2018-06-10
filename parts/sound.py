# sound.py - Play audio.

import playsound

def _in():
    while oa.alive:
        path = get()
        
        # Pause listening while talking. Mute STT.
        put('stt','mute')
        playsound.playsound(path)
   
        # Audio complete. Begin listening. Unmute STT.
        put('stt','unmute')
        yield ''
