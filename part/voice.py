import pyttsx3

def _in():
    tts = pyttsx3.init()
    while oa.alive:
        s=get()
        #pause Ear (listening) while talking. mute stt
        oa.stt.q_in.put('mute')
        tts.say(s)
        tts.runAndWait()
        #we stopped talking.
        #let's continue Ear (listening). unmute stt
        oa.stt.q_in.put('unmute')
        yield ''
