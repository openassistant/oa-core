import os, sys, re #json,
import pyttsx3
import pyaudio
import audioop
import playsound
import collections
import pocketsphinx
#from pocketsphinx.pocketsphinx import *
#from sphinxbase.sphinxbase import *
import oa_utils
import math
from oa_utils import *

import logging
logger = logging.getLogger(__name__)

#from pocketsphinx import LiveSpeech

#def playsound(path):
#    playsound(path)

class AudioUtils():
    def __init__(_):
        _.tts = pyttsx3.init()
#        self.
#        self.operation_timeout = None  # seconds after an internal operation (e.g., an API request) starts before it times out, or ``None`` for no timeout
#        self.audio = None
#        self.stream = None
        _.timeout=None
        _.channels=1
        #The ``phrase_time_limit`` parameter is the maximum number of seconds that this will allow a phrase to continue before stopping and returning the part of the phrase processed before the time limit was reached. The resulting audio will be the phrase cut off at the time limit. If ``phrase_timeout`` is ``None``, there will be no phrase time limit.
        _.phrase_time_limit=None
        _.dynamic_energy_adjustment_damping = 0.15
        _.dynamic_energy_ratio = 1.5
        _.dynamic_energy_threshold = True
        _.energy_threshold = 300  # minimum audio energy to consider for recording
        _.pause_threshold = 0.8  # seconds of non-speaking audio before a phrase is considered complete
        _.phrase_threshold = 0.3  # minimum seconds of speaking audio before we consider the speaking audio a phrase - values below this are ignored (for filtering out clicks and pops)
        _.non_speaking_duration = 0.5  # seconds of non-speaking audio to keep on both sides of the recording
        _.chunk=1024 # number of frames stored in each buffer
        _.sample_rate=16000 # sampling rate in Hertz
        _.pa_format=pyaudio.paInt16 # 16-bit int sampling
        _.sample_width=pyaudio.get_sample_size(_.pa_format) # size of each sample
        _.seconds_per_buffer = float(_.chunk) / _.sample_rate
        _.pause_buffer_count = int(math.ceil(_.pause_threshold / _.seconds_per_buffer))  # number of buffers of non-speaking audio during a phrase, before the phrase should be considered complete
        _.phrase_buffer_count = int(math.ceil(_.phrase_threshold / _.seconds_per_buffer))  # minimum number of buffers of speaking audio before we consider the speaking audio a phrase
        _.non_speaking_buffer_count = int(math.ceil(_.non_speaking_duration / _.seconds_per_buffer))  # maximum number of buffers of non-speaking audio to retain before and after a phrase
        #----------------------------------------------------------------------------------------------
        _.stream = pyaudio.PyAudio().open(format=_.pa_format, channels=_.channels, rate=_.sample_rate, input=True, frames_per_buffer=_.chunk)

    def cache_path(_,fname):#, check_exists=0
        """
          returns full path from cache folder
        """
        return os.path.join(_.cache_dir, fname)

    def playsound(_,path):
        playsound.playsound(path)

    def say(_, text):
        _.tts.say(text)
        _.tts.runAndWait()

    def config_stt(_,mind_dir, keywords, kws_last_modification_time_in_sec=None):
        logger.debug("Configuring Module: Language")
        _.cache_dir = os.path.join(mind_dir,'cache')
        _.lang_file = _.cache_path('lm')
        _.fsg_file = None #os.path.join(_.cache_dir, 'fsg')
        _.dic_file = _.cache_path('dic')
        _.kws_file = _.cache_path("kws")

        # check if commands file was modified
        if kws_last_modification_time_in_sec:
            if os.path.exists(_.dic_file) and (kws_last_modification_time_in_sec<stat_mtime(_.dic_file)):
                return

        # save phrases
        # experimental replace(' ', '')
        #replace(' ', '').
        phrases=[x.strip().replace('%d', '').upper() for x in sorted(keywords)]
        _.strings_file = _.cache_path("sentences.corpus")
        data='\n'.join(phrases)
        fwrite(_.strings_file,data)

        # explicitly specified set of keywords
        # generate a keywords file - Sphinx documentation recommendeds sensitivities between 1e-50 and 1e-5
        sensitivity=1e-5
        data='\n'.join(["{} /1e{}/".format(kw, 100 * sensitivity - 110) for kw in keywords])
        fwrite(_.kws_file,data)

        # download data from speech.cs.cmu.edu
        _.update_language()

    def update_language(_):
        """Update the language using the online lmtool"""
        ##NET_TEST_SERVER = "http://www.speech.cs.cmu.edu"
        logger.debug("\x1b[32mUpdating Language\x1b[0m")

        host = 'http://www.speech.cs.cmu.edu'
        url = host + '/cgi-bin/tools/lmtool/run'

        # SUBMIT THE CORPUS TO THE LMTOOL
        response_text = ""
        with open(_.strings_file, 'r') as corpus:
            files = {'corpus': corpus}
            values = {'formtype': 'simple'}

            r = requests.post(url, files=files, data=values)
            response_text = r.text

        # PARSE RESPONSE TO GET URLS OF THE FILES WE NEED
        path_re = r'.*<title>Index of (.*?)</title>.*'
        number_re = r'.*TAR([0-9]*?)\.tgz.*'
        path=None
        for line in response_text.split('\n'):
            # ERROR RESPONSE
            if "[_ERRO_]" in line:
                return 1
            # IF WE FOUND THE DIRECTORY, KEEP IT AND DON'T BREAK
            if re.search(path_re, line):
                path = host + re.sub(path_re, r'\1', line)
            # IF WE FOUND THE NUMBER, KEEP IT AND BREAK
            elif re.search(number_re, line):
                number = re.sub(number_re, r'\1', line)
                break

        if path is None:
            print('_.cache_dir',_.cache_dir)
            raise Exception('NOT FOUND update_language: '+response_text)
        lm_url = path + '/' + number + '.lm'
        dic_url = path + '/' + number + '.dic'

        if _.lang_file is not None:
            download_file(lm_url, _.lang_file)
        download_file(dic_url, _.dic_file)

    def listen(_): #until_silence
#    stream.start_stream()
        # read audio input for phrases until there is a phrase that is long enough
        elapsed_time = 0  # number of seconds of audio read
        buf = b""  # an empty buffer means that the stream has ended and there is no data left to read
        _.energy_threshold = 300  # minimum audio energy to consider for recording
        while True:
            frames = collections.deque()

            # store audio input until the phrase starts
            while True:
                # handle waiting too long for phrase by raising an exception
                elapsed_time += _.seconds_per_buffer
                if _.timeout and elapsed_time > _.timeout:
                    raise Exception("listening timed out while waiting for phrase to start")

                buf = _.stream.read(_.chunk)
#                if len(buffer) == 0: break  # reached end of the stream
                frames.append(buf)
                if len(frames) > _.non_speaking_buffer_count:  # ensure we only keep the needed amount of non-speaking buffers
                    frames.popleft()

                # detect whether speaking has started on audio input
                energy = audioop.rms(buf, _.sample_width)  # energy of the audio signal
                if energy > _.energy_threshold: break

                # dynamically adjust the energy threshold using asymmetric weighted average
                if _.dynamic_energy_threshold:
                    damping = _.dynamic_energy_adjustment_damping ** _.seconds_per_buffer  # account for different chunk sizes and rates
                    target_energy = energy * _.dynamic_energy_ratio
                    _.energy_threshold = _.energy_threshold * damping + target_energy * (1 - damping)

            # read audio input until the phrase ends
            pause_count, phrase_count = 0, 0
            phrase_start_time = elapsed_time
            while True:
                # handle phrase being too long by cutting off the audio
                elapsed_time += _.seconds_per_buffer
                if _.phrase_time_limit and elapsed_time - phrase_start_time > _.phrase_time_limit:
                    break

                buf = _.stream.read(_.chunk)
#                if len(buffer) == 0: break  # reached end of the stream
                frames.append(buf)
                phrase_count += 1

                # check if speaking has stopped for longer than the pause threshold on the audio input
                energy = audioop.rms(buf, _.sample_width)  # unit energy of the audio signal within the buffer
                if energy > _.energy_threshold:
                    pause_count = 0
                else:
                    pause_count += 1
                if pause_count > _.pause_buffer_count:  # end of the phrase
                    break

            # check how long the detected phrase is, and retry listening if the phrase is too short
            phrase_count -= pause_count  # exclude the buffers for the pause before the phrase
            if phrase_count >= _.phrase_buffer_count or len(buf) == 0: break  # phrase is long enough or we've reached the end of the stream, so stop listening

        # obtain frame data
        for i in range(pause_count - _.non_speaking_buffer_count): frames.pop()  # remove extra non-speaking frames at the end
        frame_data = b"".join(frames)

        return frame_data #AudioData(frame_data, _.sample_rate, _.sample_width)

    def speech_to_text(_, adata):
        """
          stt
          speech to text
        """
        #--------parse audio data----------------------------------------------------------------------------------------------------------------
        # Process audio chunk by chunk. On keyphrase detected perform action and restart search
        config = pocketsphinx.Decoder.default_config()
    #    config.set_string("-hmm", acoustic_parameters_directory)  # set the path of the hidden Markov model (HMM) parameter files
        config.set_string('-hmm', os.path.join(os.path.dirname(pocketsphinx.pocketsphinx.__file__), 'model','en-us'))
#        config.set_string("-lm", _.lang_file)
        config.set_string("-dict", _.dic_file)
        config.set_string("-logfn", os.devnull)  # disable logging (logging causes unwanted output in terminal)

        decoder = pocketsphinx.Decoder(config)

        # obtain audio data
        raw_data=adata
        #raw_data = audio_data.get_raw_data(convert_rate=sample_rate, convert_width=2)  # the included language models require audio to be 16-bit mono 16 kHz in little-endian format

        #Please note that -kws conflicts with the -lm and -jsgf options. You cannot specify both.

        # obtain recognition results
        # perform the speech recognition with the keywords file (this is inside the context manager so the file isn;t deleted until we're done)
        decoder.set_kws("keywords", _.kws_file)
#        decoder.set_search("ngram/lm")
#        decoder.set_search("keywords")
#        decoder.start_utt()  # begin utterance processing
        decoder.process_raw(raw_data, False, False)  # process audio data with recognition enabled (no_search = False), as a full utterance (full_utt = True)
#        decoder.end_utt()  # stop utterance processing

    ##    if show_all: return decoder
        # return results
        hypothesis = decoder.hyp()
        if hypothesis is not None: return hypothesis.hypstr
        raise UnknownValueError()  # no transcriptions available

