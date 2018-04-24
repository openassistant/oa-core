import playsound

def _in():
    while oa.alive:
        path=get()
        #pause Ear (listening) while talking. mute stt
        put('stt','mute')
#        oa.stt.q_in.put('mute')
        playsound.playsound(path)
        #we stopped talking.
        #let's continue Ear (listening). unmute stt
        put('stt','unmute')
#        oa.stt.q_in.put('unmute')
        yield ''
