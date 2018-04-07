# Open Assistant 0.03
# 2016 General Public License V3
# By Andrew Vavrek, Clayton G. Hobbs, Jezra, Jonathan Kulp

# core.py - Open Assistant System Core
import os
import audio
import oa_utils
from oa_utils import *

class Assistant:
    def __init__(_, mind='boot'):
        info("Initializing Assistant")
        _.cur_dir=os.path.dirname(__file__)
        _.audio=audio.AudioUtils()
        _.mind='undefined'
        _.files=[]
        # stubs for functions of oa_utils
        # let's add link to OA itself
        oa_utils.oa=_
        _.d_funcs=Stub.prepare_stubs(oa_utils)

        # history for switch minds commands
        _.switch_hist=[]
        #last perform
        _.last_phrase=''

        if mind:
            if mind=='boot':
                #check langs - dic, lm and other files. auto update if commands file was modified.
                _.check_langs()

            _.set_mind(mind)

    def loop(_, condition=lambda : True):
        while condition():
            adata=_.audio.listen()
            phrase=_.audio.speech_to_text(adata)
            _.perform(phrase)

    def log_history(_, text):
        fwrite(_.history_file(), text, append=True)

    def perform(_,text):
        info('%s.Command : %s'%(_.mind,text))
        if (text is None) or (text.strip()==''):
            #nothing to do
            return
        t = text.lower()
        # Is There A Matching Command?
        if t in _.kws:
            info('Perform : %s'%str(_.kws[t]))
            _.last_phrase=t
            #for now - 2 types of commands : Stub and Command line Text
            #for Stubs we will call perform
            if isinstance(_.kws[t],Stub):
                _.kws[t].perform()
            #for string we will call sys_exec
            elif isinstance(_.kws[t],basestring):
                sys_exec(_.kws[t])
            else:
                #we have not idea what type of this command is, so we'll raise Exception
                raise Exception('Unkown command type : %s'%str(_.kws[t]))

            _.log_history(text)

    def set_mind(_, name, history=1):
        """
          use this to switch current mind to `name` mind
        """
        info('Switch mind: %s->%s'%(_.mind,name))
        if history:
            _.switch_hist.append(name)
        _.mind=name
        _.mind_dir=os.path.join(_.cur_dir, 'mind', _.mind)
        # let's make dirs
#        _._make_dir(_.cache_dir)
#        _._make_dir(_.conf_dir)
        cf=_.commands_file()
        cf_data=fread(cf)
        d_exec=dict(_.d_funcs.items())
        exec(cf_data,d_exec)
        #let's add commands without spaces
#        _.kws=d_exec['kws']
        _.kws={}#d_exec['kws']
        for key, value in d_exec['kws'].items():
            for synonym in key.strip().split(','):
                _.kws[synonym]=value
            #_.kws[key.replace(' ','').replace('?','').replace("'",'')]=value
        # Configure Speech to text dictionaries
        _.audio.config_stt(_.mind_dir, _.kws.keys(), stat_mtime(cf))

    def switch_back(_):
        """
          let's switch to previous `mind` (from switch_hist)
        """
        _.set_mind(_.switch_hist.pop(),0)

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
        info('Update for "Speech to text" dictionaries (all minds).\nPlease wait...')
        for mind in os.listdir('mind'):
            _.set_mind(mind)
        info('Done!')

if __name__ == '__main__':
    oa=Assistant()
    oa.loop()
