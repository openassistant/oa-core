import pyttsx3

def _in():
    tts = pyttsx3.init()
    while oa.alive:
        s=get()
        #pause Ear (listening) while talking. mute stt
        put('stt','mute')
        tts.say(s)
        tts.runAndWait()
        #we stopped talking.
        #let's continue Ear (listening). unmute stt
        put('stt','unmute')
        yield ''
