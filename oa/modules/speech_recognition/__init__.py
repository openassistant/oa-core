# stt.py - Speech to text.

import logging
_logger = logging.getLogger(__name__)

import os, re, time
import logging

import pocketsphinx
import requests

from oa.util.abilities.core import get, empty, info
from oa.util.abilities.system import download_file, write_file, stat_mtime

import queue
input_queue = queue.Queue()


_decoders = {}

def config_stt(cache_dir, keywords, kws_last_modification_time_in_sec = None):
    cache_path = lambda x: os.path.join(cache_dir, x)

    _config = {
        'lang_file': cache_path('lm'),
        'fsg_file': None,
        'dic_file': cache_path('dic'),
        'kwords': {},
        'max_w_cnt': 3,
        'phrases': [],
        'strings_file': cache_path("sentences.corpus"),
    }

    # Save keywords for further pattern matching. Call `config_stt()` when switching minds to check for command file changes.
    for phrase in keywords:
        spl_ph = phrase.strip().split(' ')
        w_cnt = len(spl_ph)
        if w_cnt > _config['max_w_cnt']:
            _config['max_w_cnt'] = w_cnt
        for kword in spl_ph:
            # Combine all phrases which use keywords.
            r_phrases = _config['kwords'].setdefault(kword,{})
            r_phrases[phrase] = w_cnt

    # Save phrases.
    _config['phrases'] += [x.strip().replace('%d', '').upper() for x in sorted(keywords)]

    # XXX: Check if commands file was modified.
    # if kws_last_modification_time_in_sec:
        # if os.path.exists(_.dic_file) and (kws_last_modification_time_in_sec < stat_mtime(_.dic_file)):
            # return _
    data = '\n'.join(_config['phrases'])
    write_file(_config['strings_file'], data)

    # Download language model data from `speech.cs.cmu.edu`.
    update_language(_config)
    return _config

def update_language(config):
    # Update the language model using the online `lmtool`.
    host = 'http://www.speech.cs.cmu.edu'
    url = host + '/cgi-bin/tools/lmtool/run'

    # Submit the corpus to the `lmtool`.
    response_text = ""
    with open(config['strings_file'], 'r') as f:
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
            break
        # If we find the directory, keep it and don't break.
        if re.search(path_re, line):
            path = host + re.sub(path_re, r'\1', line)
        # If we find a number, keep it and break.
        elif re.search(number_re, line):
            number = re.sub(number_re, r'\1', line)
            break

    if path is None:
        raise Exception(response_text)

    lm_url = path + '/' + number + '.lm'
    dic_url = path + '/' + number + '.dic'

    if config['lang_file'] is not None:
        download_file(lm_url, config['lang_file'])
    download_file(dic_url, config['dic_file']) 

# XXX: not quite the right place, but a step
def get_decoder(ctx):
    # Configure Speech to text dictionaries.
    # XXX: just a hack to get things going
    # ret = config_stt(ctx.cache_dir, ctx.kws.keys(), time.now())
    _dir = os.path.dirname(__file__)
    ret = config_stt(os.path.join(_dir, ""), ["the quick boot mind jumped over the great open assistant", "this is a test"])

    # Process audio chunk by chunk. On a keyphrase detected perform the action and restart search.
    config = pocketsphinx.Decoder.default_config()

    # Set paths for the language model files.
    config.set_string('-hmm', os.path.join(_dir, "hmm-en_US")) # XXX: should come from user's config/system
    config.set_string("-lm", ret['lang_file'])
    config.set_string("-dict", ret['dic_file'])
    config.set_string("-logfn", os.devnull)  # Disable logging.

    _decoder = pocketsphinx.Decoder(config)

    return _decoder


def __call__(ctx):
    mute = 0

    decoder = get_decoder(ctx)

    while not ctx.finished.is_set():
        raw_data = input_queue.get()

        if isinstance(raw_data, str):
            if raw_data == 'mute':
                _logger.debug('Muted')
                mute = 1
            elif raw_data == 'unmute':
                _logger.debug('Unmuted')
                mute = 0
                time.sleep(.9)
                empty()
            continue
            
        # Mute mode. Do not listen until unmute.
        if mute:
            continue
        
        # Obtain audio data.
        try:
            decoder.start_utt()  # Begin utterance processing.

            # Process audio data with recognition enabled (no_search = False), as a full utterance (full_utt = True)
            decoder.process_raw(raw_data, False, False)  

            decoder.end_utt()  # Stop utterance processing.

        except Exception as e:
            _logger.error(e)

        else:
            hypothesis = decoder.hyp()
            if hypothesis is not None: 
                hyp = hypothesis.hypstr
                if (hyp is None) or (hyp.strip() == ''):
                    continue
                _logger.info("Recognized: {}".format(hyp))
                yield hyp

            else:
                _logger.warn('Speech not recognized')
