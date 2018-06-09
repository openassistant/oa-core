import pyttsx3

voices={}
tts=None

def onStart(name):
#   info('say_start1')
   put('display',('say_start', name))
#   info('say_start2')

def onWord(name, location, length):
   put('display',('say_word', name, location, length))

def onEnd(name, completed):
   put('display',('say_stop', name, completed))

def _in():
    global voices, tts
    tts = pyttsx3.init()
    voices = tts.getProperty('voices')
    tts.connect('started-utterance', onStart)
    tts.connect('started-word', onWord)
    tts.connect('finished-utterance', onEnd)
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
