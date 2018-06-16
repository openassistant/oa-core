# stt.py - Speech to text.

import os, re, time
import logging

import pocketsphinx
from pocketsphinx.pocketsphinx import *

import requests

from core import oa, Core
from abilities.core import info, write_file, download_file, get, empty, stat_mtime

def config_stt(cache_dir, keywords, kws_last_modification_time_in_sec = None):
    _ = Core()
    cache_path = lambda x: os.path.join(cache_dir, x)
    _.lang_file = cache_path('lm')
    _.fsg_file = None
    _.dic_file = cache_path('dic')
    _.hmm_dir = cache_path('hmm')

    # Save keywords for further pattern matching. Call `config_stt()` when switching minds to check for command file changes.
    _.kwords = {}
    _.max_w_cnt = 3
    for phrase in keywords:
        spl_ph = phrase.strip().split(' ')
        w_cnt = len(spl_ph)
        if w_cnt > _.max_w_cnt:
            _.max_w_cnt = w_cnt
        for kword in spl_ph:
            # Combine all phrases which use keywords.
            r_phrases = _.kwords.setdefault(kword,{})
            r_phrases[phrase] = w_cnt

    # Save phrases.
    _.phrases = [x.strip().replace('%d', '').upper() for x in sorted(keywords)]

     # Check if commands file was modified.
    if kws_last_modification_time_in_sec:
        if os.path.exists(_.dic_file) and (kws_last_modification_time_in_sec < stat_mtime(_.dic_file)):
            return _
    _.strings_file = cache_path("sentences.corpus")
    data = '\n'.join(_.phrases)
    write_file(_.strings_file, data)

    # Download language model data from `speech.cs.cmu.edu`.
    update_language(_) 
    return _

def update_language(_):
    # Update the language model using the online `lmtool`.
    host = 'http://www.speech.cs.cmu.edu'
    url = host + '/cgi-bin/tools/lmtool/run'

    # Submit the corpus to the `lmtool`.
    response_text = ""
    with open(_.strings_file, 'r') as f:
        files = {'corpus': f}
        values = {'formtype': 'simple'}

        r = requests.post(url, files = files, data = values)
        response_text = r.text

    # Parse response to get urls of the files we need.
    path_re = r'.*<title>Index of (.*?)</title>.*'
    number_re = r'.*TAR([0-9]*?)\.tgz.*'
    path = None
    for line in response_text.split('\n'):
        # Error response.
        if "[_ERRO_]" in line:
            return 1
        # If we find the directory, keep it and don't break.
        if re.search(path_re, line):
            path = host + re.sub(path_re, r'\1', line)
        # If we find a number, keep it and break.
        elif re.search(number_re, line):
            number = re.sub(number_re, r'\1', line)
            break

    if path is None:
        info('_.cache_dir',_.cache_dir)
        raise Exception('Not found: update_language: ' + response_text)
    lm_url = path + '/' + number + '.lm'
    dic_url = path + '/' + number + '.dic'

    if _.lang_file is not None:
        download_file(lm_url, _.lang_file)
    download_file(dic_url, _.dic_file) 

def get_decoder():
    mind = oa.mind.active
    ret = oa.speech_recognition.decoders[mind.name]
    if not ret:
        # Configure Speech to text dictionaries.
        ret = config_stt(mind.cache_dir, mind.kws.keys(), stat_mtime(mind.module))
        
        # Process audio chunk by chunk. On a keyphrase detected perform the action and restart search.
        config = pocketsphinx.Decoder.default_config()

        # Set paths for the language model files.
        config.set_string('-hmm', ret.hmm_dir)
        config.set_string("-lm", ret.lang_file)
        config.set_string("-dict", ret.dic_file)
        config.set_string("-logfn", os.devnull)  # Disable logging.

        ret.decoder = pocketsphinx.Decoder(config)
        oa.speech_recognition.decoders[mind.name] = ret

    return ret

def _in():
    mute = 0
    skipIt = 0
    while not oa.core.finished.is_set():
        raw_data = get()
        if isinstance(raw_data, str):
            if raw_data == 'mute':
                logging.debug('Muted')
                mute = 1
            elif raw_data == 'unmute':
                logging.debug('Unmuted')
                mute = 0
                time.sleep(.9)
                empty()
                continue
        # Mute mode. Do not listen until unmute.
        if mute:
            time.sleep(.9)
            continue
        # Obtain audio data.
        dinf = get_decoder()
        decoder = dinf.decoder
        decoder.start_utt()  # Begin utterance processing.
        try:
            decoder.process_raw(raw_data, False, False)  
            # Process audio data with recognition enabled (no_search = False), as a full utterance (full_utt = True)
        except Exception as e:
            info(str(e))

        decoder.end_utt()  # Stop utterance processing.

        hypothesis = decoder.hyp()
        if hypothesis is not None: 
            hyp = hypothesis.hypstr
            if (hyp is None) or (hyp.strip() == ''):
                continue
            logging.info("Heard: {}".format(hyp))
            if hyp.upper() in dinf.phrases:
                yield hyp
            else:
                continue

        else:
            logging.warn('Speech not recognized')
