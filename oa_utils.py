import os, sys, glob
import subprocess, requests
import playsound

#import logging
#logger = logging.getLogger(__name__)
#info=logger.info

oa=None

"""
useful functions which may be used in commands.py files of different mind.
"""
def info(*args):
#    logger.info(args)
    if len(args)==1:
        print(args[0])
    else:
        print(args)

def find_file(fname):
    """
      search for file with name `fname` in all OA sub-directories
      (so we may use short file name if we sure it will be unique).
      NEED FIX - put files names into Cache list ?
    """
    cur_dir=os.path.dirname(__file__)
    ret=glob.glob(os.path.join(cur_dir,'mind/*/*/%s'%fname))
    if len(ret)!=1:
        raise Exception('%s : found %d results.'%(fname,len(ret)))
    return ret[0]

def say(text):
    """
      text to speech
      using oa.audio.say defined function
      to generate voice from `text`
    """
    oa.audio.say(text)

def play(fname):
    """
      playing sound file
    """
    playsound.playsound(find_file(fname))

def mind(name):
    """
      switch current mind to `name`
    """
    global oa
    info('!mind!',name)
    oa.set_mind(name)

def sys_exec(cmd):
    """print cmd execute in OS env"""
    subprocess.call(cmd, shell=True)

def download_file(url, path):
    """
      download file by url and save it by local path
    """
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        with open(path, 'wb') as f:
            for chunk in r:
                f.write(chunk)

def fwrite(fname, data, append=False):
        #no max_size analyze for now.
        #FIX : in case of max_size -> use LIFO
#        if os.path.exists(fname):
#            if os.stat(fname).st_size
    if append:
        with open(fname, 'w+') as f:
            f.write(data)
    else:
        with open(fname, 'w') as f:
            f.write(data)

def fread(fname):
    try:
        with open(fname, 'r') as f:
            return f.read()
    except FileNotFoundError:
        logger.warn("Error loading file: {path}".format(path=fname))
        return ''

def stat_size(fname):
    """
      returns file size
    """
    return os.stat(fname).st_size

def stat_mtime(fname):
    """
      returns file last modification time (in seconds)
    """
    return os.stat(fname).st_mtime

#def make_dirs(_, directory):
#    if not os.path.exists(directory):
#        os.makedirs(directory)

class Stub():
    """
      Stub for delayed py calls
      for minds, commands.py
    """
    def __init__(_,o, *args, **kwargs):
        _.commands=[[o,args,kwargs]]
##        info('init',o, args, kwargs)

    def __and__(_,o):
##        info('__and__',o)
        _.commands.append(o.commands[0])
        return _

    def __add__(_,o):
        """
          simple redirect to __and__ oper
        """
        return _ & o

    def __call__(_,*args,**kwargs):
        """
          just fill func parameters
          for real calls (all at once)
          we will use `perform`
        """
        ret=Stub(_.commands[0][0])
        ret.commands[0][1]=args
        ret.commands[0][2]=kwargs
        return ret

##    def __or__(_,o):
##        info('__or__',o)
##        pass
    def perform(_):
        """
          call all functions one by one
        """
        for func,args,kwargs in _.commands:
            func(*args,**kwargs)


    @classmethod
    def prepare_stubs(_,module):
        """
          returns dictionary with Stubs of all functions
          in corresponded `module`
        """
        ret={}
        #hasattr(obj, '__call__')
        #isinstance(open, types.FunctionType)
        for name,body in module.__dict__.items():
            # let's skip for current class definition. to prevent hard recursion =)
            if name==_.__name__:
                continue

            if hasattr(body,'__call__'):
                ret[name]=Stub(body)
        return ret

    @classmethod
    def test(_):
        c1=Stub(play)
        c2=Stub(mind)
        ret=c1('beep_hello.wav') & c2('root_arch')
        #execute all
        ret.perform()
##        print(c1 or c2)


def replace_echo_voice(fname):
    """
     util to convert echo * VOICE command to say(*)
     in commands.py file.
     for manual usage only =)
    """
    with open(fname,'r') as f:
        d=f.readlines()
    nd=[]
    for x in d:
        #"you there?": "echo yes... i am here... | $VOICE",
        ret=x.strip()
        spl=ret.split(':')
        if len(spl)==2:
            s1,s2=spl
            if s2.strip().startswith('"echo ') and s2.strip().endswith('$VOICE",') and not ('.py' in x):
                ret=s1+': say("'+s2.replace('"echo ','').replace('| $VOICE",','').strip()+'"),'
        nd.append('  '+ret)
    fwrite(fname,'\n'.join(nd))

#replace_echo_voice(r'C:\!OA\mind\stella\conf\commands.py')

#test
#Stub.test()
#def_stubs=Stub.prepare_stubs(sys.modules[__name__])