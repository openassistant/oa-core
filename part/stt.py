#speech to text
import os, re, time, pocketsphinx
from pocketsphinx.pocketsphinx import *

def config_stt(cache_dir, keywords, kws_last_modification_time_in_sec=None):
#    logger.debug("Configuring Module: Language")
    _=AnyProp()
    cache_path=lambda x: os.path.join(cache_dir, x)
    _.lang_file = cache_path('lm')
    _.fsg_file = None #os.path.join(_.cache_dir, 'fsg')
    _.dic_file = cache_path('dic')
    #let's save keywords (to further checks). we call config_stt every time (on mind switch), to check for changes.
    #_.keywords = [k in  for x in keywords]
    _.kwords={}
    _.max_w_cnt=0
    for phrase in keywords:
        spl_ph=phrase.strip().split(' ')
        w_cnt=len(spl_ph)
        if w_cnt>_.max_w_cnt:
            _.max_w_cnt=w_cnt
        for kword in spl_ph:
            #combine all phrases which use kword
            r_phrases=_.kwords.setdefault(kword,{})
            r_phrases[phrase]=w_cnt

    # check if commands file was modified
    if kws_last_modification_time_in_sec:
        if os.path.exists(_.dic_file) and (kws_last_modification_time_in_sec<stat_mtime(_.dic_file)):
            return _

    # save phrases
    # experimental replace(' ', '')
    #replace(' ', '').
    phrases=[x.strip().replace('%d', '').upper() for x in sorted(keywords)]
    _.strings_file = cache_path("sentences.corpus")
    data='\n'.join(phrases)
    fwrite(_.strings_file,data)

    # download data from speech.cs.cmu.edu
    update_language(_)
    return _

def update_language(_):
    """Update the language using the online lmtool"""
    ##NET_TEST_SERVER = "http://www.speech.cs.cmu.edu"
#    oa.logger.debug("\x1b[32mUpdating Language\x1b[0m")
    host = 'http://www.speech.cs.cmu.edu'
    url = host + '/cgi-bin/tools/lmtool/run'

    # SUBMIT THE CORPUS TO THE LMTOOL
    response_text = ""
    with open(_.strings_file, 'r') as f:
        files = {'corpus': f}
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
        info('_.cache_dir',_.cache_dir)
        raise Exception('NOT FOUND update_language: '+response_text)
    lm_url = path + '/' + number + '.lm'
    dic_url = path + '/' + number + '.dic'

    if _.lang_file is not None:
        download_file(lm_url, _.lang_file)
    download_file(dic_url, _.dic_file)

def BestHyp(s):
    ranks={}
    s=s.lower()
    len_ws=len(s.split(' '))
    kwords=get_decoder().kwords
    #max_rank=[result,rank,diff in words count]
    max_rank=['',0,0]
    for kword in s.split(' '):
        phrases=kwords.get(kword,{})
        for phrase,lw_ph in phrases.items():
            ranks.setdefault(phrase,0)
            ranks[phrase]+=1
            rank=ranks[phrase]
            # choose by rank - max words (from seacrh) contains in phrase
#            w_cnt_diff=abs(len_ws-lw_ph)
            if rank>max_rank[1]:
                max_rank[0]=phrase
                max_rank[1]=rank
                max_rank[2]=lw_ph
            elif rank==max_rank[1]:
                #fit better by words count
                # if rank is equal - looking for smaller (words count) sentence
                if lw_ph<max_rank[2]:
                    max_rank[0]=phrase
                    max_rank[2]=lw_ph

# 1.there is word match 
#2. and phrase (which we found) contains only 1 word 
#    or more than 75% of search sentence (words) contains in search result.
    if (max_rank[1]>0) and ((max_rank[2]==1) or ((abs(len_ws-max_rank[2])/max_rank[2])<0.25)):
        return max_rank[0]
    return ''

def get_decoder():
    mind=oa.mind.active
    ret=oa.stt.decoders[mind.name]
    if not ret:
        # Configure Speech to text dictionaries
        ret=config_stt(mind.cache_dir, mind.kws.keys(), stat_mtime(mind.module))
        # Process audio chunk by chunk. On keyphrase detected perform action and restart search
        config = pocketsphinx.Decoder.default_config()
        #    config.set_string("-hmm", acoustic_parameters_directory)  # set the path of the hidden Markov model (HMM) parameter files
        info('cur lang = '+mind.lang)
        config.set_string('-hmm', os.path.join(os.path.dirname(pocketsphinx.pocketsphinx.__file__), 'model',mind.lang))
#        info("-lm", ret.lang_file)
        config.set_string("-lm", ret.lang_file)
        config.set_string("-dict", ret.dic_file)
        config.set_string("-logfn", os.devnull)  # disable logging (logging causes unwanted output in terminal)
        ret.decoder=pocketsphinx.Decoder(config)
        oa.stt.decoders[mind.name]=ret

    return ret

def _in():
#    oa.stt.last_phrase=''
    mute=0
    skipIt=0
    while oa.alive:
        raw_data=get()
        if isinstance(raw_data,str):
            if raw_data=='mute':
                info('stt mute')
                mute=1
            elif raw_data=='unmute':
                info('stt unmute')
                mute=0
                time.sleep(.4)
                empty()
                continue
        #mute mode - do not parse audio data. until unmute
        if mute:
            time.sleep(.1)
            continue
        # obtain audio data
        dinf=get_decoder()
        decoder=dinf.decoder
        decoder.start_utt()  # begin utterance processing
        try:
            decoder.process_raw(raw_data, False, False)  # process audio data with recognition enabled (no_search = False), as a full utterance (full_utt = True)
        except Exception as e:
            info(str(e))
#        decoder.process_raw(raw_data, False, False)  # process audio data with recognition enabled (no_search = False), as a full utterance (full_utt = True)
        decoder.end_utt()  # stop utterance processing

        hypothesis = decoder.hyp()
        if hypothesis is not None:
            hyp=hypothesis.hypstr
            if (hyp is None) or (hyp.strip()==''):
                continue
            info('!STT! hyp=',hyp)
            #1 word check
            if dinf.max_w_cnt==1:
                for x in map(BestHyp,hyp.split(' ')):
                    yield x
            else:
                yield BestHyp(hyp)
        else:
            info('no transcriptions available')
