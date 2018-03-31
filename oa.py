# Open Assistant 0.03
# 2016 General Public License V3
# By Andrew Vavrek, Clayton G. Hobbs, Jezra, Jonathan Kulp

# core.py - Open Assistant System Core

import logging
import os
import audio
import oa_utils
from oa_utils import *
logger = logging.getLogger(__name__)

class Assistant:
    def __init__(_, mind='boot'):
        logger.info("Initializing Assistant")
        _.audio=audio.AudioUtils()
        if mind:
            if mind=='boot':
                #check langs - dic, lm and other files. auto update if commands file was modified.
                _.check_langs()

            _.set_mind(mind)

    def loop(_):
        while True:
            adata=_.audio.listen()
            phrase=_.audio.speech_to_text(adata)
            _.perform(phrase)

    def log_history(_, text):
        fwrite(_.history_file(), text, append=True)

    def perform(_,text):
#        logger.debug("Agent: {}, Text: {}".format(_, text))
        print('Command : ' + text)
        if (text is None) or (text.strip()==''):
            #nothing to do
            return
        t = text.lower()
        # Is There A Matching Command?
        if t in _.kws:
            exec_cmd(_.kws[t])
            _.log_history(text)

    def set_mind(_, mind):
        logger.info("Loading Mind: {cur}".format(cur=mind))
        _.mind=mind
        _.mind_dir=os.path.join(os.path.dirname(__file__), 'mind', _.mind)
        # let's make dirs
#        _._make_dir(_.cache_dir)
#        _._make_dir(_.conf_dir)
        d_exec={}
        cf=_.commands_file()
        execfile(cf,d_exec)
        #let's add commands without spaces
#        _.kws=d_exec['kws']
        _.kws={}
        for key, value in d_exec['kws'].iteritems():
            _.kws[key.replace(' ','').replace('?','').replace("'",'')]=value
        # Configure Language
        _.audio.config_stt(_.mind_dir, _.kws.keys())#, stat_mtime(cf))

    def conf_path(_,fname):#, check_exists=0
        """
          returns full path from conf folder
        """
        return os.path.join(_.mind_dir,'conf', fname)

    def history_file(_):
        return os.path.join(_.mind_dir,'cache', 'history')

    def commands_file(_):
        return _.conf_path("commands.py")

    def check_langs(_):
        """
          check dictionaries for all minds.
          Handles updating the language using the online lmtool.
          see :
        """
        for mind in os.listdir('mind'):
            _.set_mind(mind)

if __name__ == '__main__':
    oa=Assistant()
    oa.loop()
