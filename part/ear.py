import sounddevice,audioop
import math, collections, numpy

def _in():
    timeout=None
    channels=1
    #The ``phrase_time_limit`` parameter is the maximum number of seconds that this will allow a phrase to continue before stopping and returning the part of the phrase processed before the time limit was reached. The resulting audio will be the phrase cut off at the time limit. If ``phrase_timeout`` is ``None`` there will be no phrase time limit.
    phrase_time_limit=None
    dynamic_energy_adjustment_damping = 0.15
    dynamic_energy_ratio = 1.5
    dynamic_energy_threshold = True
    energy_threshold = 3000  # minimum audio energy to consider for recording
    pause_threshold = 0.5  # seconds of non-speaking audio before a phrase is considered complete
    phrase_threshold = 0.3  # minimum seconds of speaking audio before we consider the speaking audio a phrase - values below this are ignored (for filtering out clicks and pops)
    non_speaking_duration = 0.5  # seconds of non-speaking audio to keep on both sides of the recording
    chunk=1024 # number of frames stored in each buffer
    sample_rate=16000 # sampling rate in Hertz
    ##        pa_format=pyaudio.paInt16 # 16-bit int sampling
    sample_width=2 #pyaudio.get_sample_size(pa_format) # size of each sample
    seconds_per_buffer = float(chunk) / sample_rate
    pause_buffer_count = int(math.ceil(pause_threshold / seconds_per_buffer))  # number of buffers of non-speaking audio during a phrase before the phrase should be considered complete
    phrase_buffer_count = int(math.ceil(phrase_threshold / seconds_per_buffer))  # minimum number of buffers of speaking audio before we consider the speaking audio a phrase
    non_speaking_buffer_count = int(math.ceil(non_speaking_duration / seconds_per_buffer))  # maximum number of buffers of non-speaking audio to retain before and after a phrase
    stream=sounddevice.Stream(samplerate=sample_rate, channels=channels, dtype='int16')
    with stream:
        while oa.alive:
            elapsed_time = 0  # number of seconds of audio read
            buf = b""  # an empty buffer means that the stream has ended and there is no data left to read
#            energy_threshold = 300  # minimum audio energy to consider for recording
            while oa.alive:
                frames = collections.deque()
                
                # store audio input until the phrase starts
                while oa.alive:
                    # handle waiting too long for phrase by raising an exception
                    elapsed_time += seconds_per_buffer
                    if timeout and elapsed_time > timeout:
                        raise Exception("listening timed out while waiting for phrase to start")

                    buf = stream.read(chunk)[0]
        #                if len(buffer) == 0: break  # reached end of the stream
                    frames.append(buf)
                    if len(frames) > non_speaking_buffer_count:  # ensure we only keep the needed amount of non-speaking buffers
                        frames.popleft()

                    # detect whether speaking has started on audio input
                    energy = audioop.rms(buf, sample_width)  # energy of the audio signal
                    if energy > energy_threshold: break

                    # dynamically adjust the energy threshold using asymmetric weighted average
                    if dynamic_energy_threshold:
                        damping = dynamic_energy_adjustment_damping ** seconds_per_buffer  # account for different chunk sizes and rates
                        target_energy = energy * dynamic_energy_ratio
                        energy_threshold = energy_threshold * damping + target_energy * (1 - damping)

                # read audio input until the phrase ends
                pause_count, phrase_count = 0, 0
                phrase_start_time = elapsed_time
                while oa.alive:
                    # handle phrase being too long by cutting off the audio
                    elapsed_time += seconds_per_buffer
                    if phrase_time_limit and elapsed_time - phrase_start_time > phrase_time_limit:
                        break

                    buf = stream.read(chunk)[0]
        #                if len(buffer) == 0: break  # reached end of the stream
                    frames.append(buf)
                    phrase_count += 1

                    # check if speaking has stopped for longer than the pause threshold on the audio input
                    energy = audioop.rms(buf, sample_width)  # unit energy of the audio signal within the buffer
                    if energy > energy_threshold:
                        pause_count = 0
                    else:
                        pause_count += 1
                    if pause_count > pause_buffer_count:  # end of the phrase
                        break

                # check how long the detected phrase is, and retry listening if the phrase is too short
                phrase_count -= pause_count  # exclude the buffers for the pause before the phrase
                if phrase_count >= phrase_buffer_count or len(buf) == 0: break  # phrase is long enough or we've reached the end of the stream, so stop listening
           
            # obtain frame data
            for i in range(pause_count - non_speaking_buffer_count): frames.pop()  # remove extra non-speaking frames at the end
        #            frame_data = b"".join(frames)
            frame_data=numpy.concatenate(frames)
            yield frame_data

#for x in _in():
#    print(len(x))
#no output
#def _out():