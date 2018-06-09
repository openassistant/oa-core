import os, sys, glob, random, string
import subprocess, requests
import inspect
import keyboard
import platform
import feedparser
import datetime, math
import getpass,socket
import psutil
import threading
import itertools
from itertools import *

try:
    import queue
except:
    import Queue as queue


unknown_os='unknown operating system'

import logging
logging.basicConfig(filename='oa.log', level=logging.INFO)
#logger = logging.getLogger(__name__)
#log_level = logging.getLevelName('INFO')
#logger.setLevel('INFO')
#logger.setLevel(log_level)
#info=logger.info

def isCallable(x):
    return hasattr(x, "__call__")

def switch(*args):
    """
    simple switch function
    with variable args count
    Example : switch(var,'aa',1,'bb',2,4)
    similar to
    if var=='aa' return 1
    elif var=='bb' return 2
    else return 4
    """
    lA=len(args)
    if lA<=2:
        raise Exception('switch: Wrong argument number.\nargs=%s'%str(args))

    # if not found -> return None
    ret=None
    if lA%2==0:
        #with else statement
        ret=args[-1]
        args=args[:-1]
    #we will check key:value via dict
    return dict(zip(args[1::2],args[2::2])).get(args[0],ret)

class AnyProp(object):
    """
      simple class to store any properties
      if attribute doesn't exists yet -
      we will assign it and return AnyProp
    """
    def __init__(_,*args,**kwargs):
        if args:
            _.args=args
        #simply update from kwargs
        _.__dict__.update(kwargs)

    def __nonzero__(_):
        return len(_.__dict__)

    def __bool__(_):
         return len(_.__dict__)>0

    def __getitem__(_, key):
        if not isinstance(key,str):
            print(key)
        return getattr(_,key)

    def __setitem__(_, key, value):
        setattr(_,key,value)

    def __getattribute__(_, name):
        """
          if attribute is a function and no arguments -
          we will return call of this function
        """
        try:
            att=object.__getattribute__(_, name)
        except AttributeError as e:
            #for unknown attributes - returns new Instance of AnyProp (except system attrs __*__)
            if name.startswith('__') and name.endswith('__'):
                raise
            att=AnyProp()
            object.__setattr__(_, name, att)

        if isCallable(att):
            insp=inspect.getargspec(att)
            if (len(insp.args)==0) and (att.__name__=='<lambda>'):
                #return func Call result
                return att()
        return att

#all global shared dependencies and resources
oa=AnyProp()
#oa=AnyProp(**{'a':1})
#print(oa.a)
#print(oa['aaa'])
#oa['bbb'].v=1
#print(oa.sys.test)
#common oa.sys funcs
#      OS name : 'win','mac','linux'
oa.sys.os=switch(platform.system(),'Windows','win','Linux','linux','Darwin','mac','unknown')
oa.sys.user=getpass.getuser()
oa.sys.host=socket.gethostname()
oa.sys.ip=socket.gethostbyname(oa.sys.host)
#date funcs
#property(fget=None, fset=None, fdel=None, doc=None)
oa.sys.now=lambda : datetime.datetime.now()
oa.sys.second=lambda : oa.sys.now.second
oa.sys.hour=lambda : oa.sys.now.hour
oa.sys.day=lambda : oa.sys.now.day
oa.sys.month=lambda : oa.sys.now.month
oa.sys.month_name=lambda : oa.sys.now.strftime("%B")
oa.sys.year=lambda : oa.sys.now.year
oa.sys.date_text=lambda : '%d %s %d'%(oa.sys.day,oa.sys.month_name,oa.sys.year)
oa.sys.time_text=lambda : '%d:%d'%(oa.sys.hour,oa.sys.second)
oa.sys.date_time_text=lambda : oa.sys.date_text+' '+oa.sys.time_text
oa.sys.free_memory=lambda : psutil.virtual_memory()[-1]
#oa.sys.public_ip=

if oa.sys.os=='win':
    global wshell
    import win32com.client
    from win32com.client import Dispatch as CreateObject
    wshell=CreateObject("WScript.Shell")

    #windows processing
    import win32gui
    import re

    class WindowMgr:
        """Encapsulates some calls to the winapi for window management"""

        def __init__ (self):
            """Constructor"""
            self._handle = None

        def find_window(self, class_name, window_name=None):
            """find a window by its class_name"""
            self._handle = win32gui.FindWindow(class_name, window_name)

        def _window_enum_callback(self, hwnd, wildcard):
            """Pass to win32gui.EnumWindows() to check all the opened windows"""
            if re.match(wildcard, str(win32gui.GetWindowText(hwnd))) is not None:
                self._handle = hwnd

        def find_window_wildcard(self, wildcard):
            """find a window whose title matches the wildcard regex"""
            self._handle = None
            win32gui.EnumWindows(self._window_enum_callback, wildcard)

        def set_foreground(self):
            """put the window in the foreground"""
            win32gui.SetForegroundWindow(self._handle)

def bytes2gb(size):
    """
      convert size from bytes to gigabytes
      precision : 2 digits after point.
    """
    ##round(x,2)
    return size/float(1<<30)

"""
useful functions which may be used in commands.py files of different mind.
"""
def activate(s):
    if oa.sys.os=='win':
        w = WindowMgr()
        w.find_window_wildcard('.*'+s+'.*')
        w.set_foreground()
    else:
        raise Exception('`activate` is unsupported')

def get_sys(s):
    """
      returns system information from oa.sys
    """
    return getattr(oa.sys,s)

def thread_name():
    """
      returns current thread name only
    """
    return threading.current_thread().name.split(' ')[0]

def info(*args,**kwargs):
    #'\nThread : '
    s=thread_name()+' '
    if args:
        s+=' '.join([str(v) for v in args])+'\n'
#        s+=' '.join([' %d : %s'%(i,str(v)) for i,v in enumerate(args)])

    if kwargs:
        s+='\n'.join([' %s : %s'%(str(k),str(v)) for k,v in args.items()])

    if oa.console and oa.alive:
        oa.console.q_in.put(s)
    else:
        print(s)

    logging.info(s)
#    if len(args)==1:
#        print(args[0])
#    else:
#        print(args)

def close(s):
    """
      close app by window or process name
      (partial window name will works too : 'note*')
    """
    say('cannot close %s for now'%s)
    pass

def mute(mute=True):
    """set mute/unmute for speakers"""
    if oa.sys.os=='win':
        wshell.SendKeys(chr(173))
    elif oa.sys.os in ('linux','mac'):
        sys_exec('amixer set Master %smute'(((not mute) and 'un') or ''))
    else:
        info(unknown_os)

def unmute():
    """set unmute for speakers"""
    mute(False)

def volume(move=2):
    """
      chnage value of Volume :
        positive `move` - Volume Up
        negative `move` - Volume Down
    """
    if oa.sys.os=='win':
        #up by 2
        if move>0:
            #volume up
            key=chr(175)
        else:
            move=-move
            key=chr(174)

        while move>0:
            wshell.SendKeys(key)
            move-=2
    elif oa.sys.os in ('linux','mac'):
        if move>0:
            sys_exec('pamixer --increase %d'%move)
        else:
            sys_exec('pamixer --decrease %d'%(-move))
    else:
        info(unknown_os)

def keys(s):
    """
      Hook and simulate keyboard events
    """
    if '+' in s:
        keyboard.press_and_release(s)
    else:
        keyboard.write(s)

def find_file(fname):
    """
      search for file with name `fname` in all OA sub-directories
      (so we may use short file name if we sure it will be unique).
      NEED FIX - put files names into Cache list ?
    """
    cur_dir=os.path.dirname(__file__)
    ret=glob.glob(os.path.join(cur_dir,'mind/*/%s'%fname))
    if not ret:
        ret=glob.glob(os.path.join(cur_dir,'mind/*/*/%s'%fname))
    if len(ret)!=1:
        raise Exception('%s : found %d results.'%(fname,len(ret)))
    return ret[0]

def cur_part():
    """
      returns "current" part
      which is associated with current thread
    """
    name=thread_name()
    ret=oa.app.parts.get(name,None)
    if ret is None:
        err='%s Error : Cannot find a corresponed part'%name
        info(err)
        raise Exception(err)
    return ret

def empty(part=None):
    """
      no params
      thread safe
      simply remove all messages
      from part.q_in input Queue
    """
    if part is None:
        part=cur_part()
    try:
        while True:
            part.q_in.get(False)
    except queue.Empty:
        pass

def get(part=None,timeout=0):
    """
      no params
      thread safe
      simply returns message
      from part.q_in input Queue
      if part is None - takes message from current q_in (thread)
    """
    if part is None:
        part=cur_part()

#    print('!!',part,'!!')
#    print('!',part.name,'!')
    if part.name=='mind':
        info('get for :',part.name)

    while oa.alive:
        try:
            return part.q_in.get(timeout=timeout)
        except queue.Empty:
            pass
        if timeout!=0:
            return None

    #terminated - raise Exception
    raise Exception('App.Terminated')


def put(part,value):
    """
      let's put message into
      part.q_in - input messages Queue
    """
    oa[part].q_in.put(value)

def say(text):
    """
      text to speech
      using oa.audio.say defined function
      to generate voice from `text`
    """
    text=call_func(text)
    info(text)
    oa.sys.last_say=text
    #put message into voice
    put('voice',text)

def say_random(slist):
    return random.choice([x.strip() for x in slist.split(',')])

def random_from_file(fname):
    l=fread(fname,result_as_list=1)
    return random.choice(l)

def play(fname):
    """ playing sound file  """
    put('sound',find_file(fname))

def mind(name, history=1):
    """ switch current mind to `name` """
#    info('Test Mind',oa.mind.__dict__)
    oa.mind.set_mind(name, history)

def sys_exec(cmd):
    """ print cmd execute in OS env """
    subprocess.call(cmd, shell=True)

def download_file(url, path):
    """ download file by url and save it by local path """
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

def fread(fname, result_as_list=0):
    """
      just read file content and return as a string
      or list of string - splitted by new line symbol
    """
    try:
        info('read file', fname)
        if not os.path.exists(fname):
            fname=find_file(fname)
        with open(fname, 'r') as f:
            if result_as_list:
                return f.readlines()
            else:
                return f.read()
    except:# FileNotFoundError:
        info("Error loading file: {path}".format(path=fname))
        #logger.warn("Error loading file: {path}".format(path=fname))
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
#        info('init',o, args, kwargs)

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
        ret=[]
        for func,args,kwargs in _.commands:
            #check args for Stubs (to perform them too)
#            args=[(isinstance(x,Stub) and x.perform()) or x for x in args]
            ret.append(func(*args,**kwargs))

        if len(ret)==1:
            return ret[0]
        else:
            return ret


##    def __call__(_,*args,**kwargs):
##        _.perform()

    @classmethod
    def prepare_stubs(_,module):
        """
          returns dictionary with Stubs of all functions
          in corresponded `module`
        """
##        #nowait - to call function without delays
##        nowait=AnyProp()
##        ret={'nowait':nowait}
        ret={}
        #hasattr(obj, '__call__')
        #isinstance(open, types.FunctionType)
        for name,body in module.__dict__.items():
            # let's skip for current class definition. to prevent hard recursion =)
#            if name==_.__name__:
#                continue
            #oa.sys and others AnyProp instances
            if isinstance(body,AnyProp):
                ret[name]=body
            else:
                #direct call without stub
##                setattr(nowait,name,body)
                if hasattr(body,'__call__'):
                    #lets add all funcs to oa.sys - for direct call (no Stubs)
#                    setattr(oa.sys,name,body)
                    #if we call function with _ prefix it will be executed immediately without Stub
                    ret['_'+name]=body
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

#test
#Stub.test()
#def_stubs=Stub.prepare_stubs(sys.modules[__name__])


def is_online(host='8.8.8.8', port=53, timeout=1):
    """If Connected Return True
     Else False
     Host: 8.8.8.8 (google-public-dns-a.google.com)
     OpenPort: 53/tcp
     Service: domain (DNS/TCP)
     """
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except Exception as ex:
        info(ex.message)
        return False

def say_last_phrase(s):
  say(s+' '+oa.last_phrase)

def read_news_feed(news_feed, category):
    rss = feedparser.parse(news_feed)
    info(rss['feed']['title'])
    say('reading %s news'%category)
    for post in rss.entries:
        headline = post.title
        exclude = set(string.punctuation)
        headline = ''.join(ch for ch in headline if ch not in exclude)
        say(headline)

def read_forecast():
    import forecastio
    """
    Get Weather Forecast From Dark Sky (darksky.net)
    Get Your API Key And Longitude / Latitude At: https://darksky.net/dev/
    Install 'forecastio' module with: pip install python-forcastio
    """
    # Weather For Darmstadt, Germany

    api_key = "e3f8667cb539171dc2f4b389d33648ce"
    lat = 49.8705556
    lng = 8.6494444

    forecast = forecastio.load_forecast(api_key, lat, lng)
    byNow = forecast.currently()
    byHour = forecast.hourly()
    byDay = forecast.daily()
    wheather_summary="""The weather is currently %s ...\n
The temperature is %d degrees Celsius ... %s %s"""%(byNow.summary,int(byNow.temperature),byHour.summary,byDay.summary)
    say(wheather_summary)

def diagnostic():
    sDiag='ok... running diagnostics...'
    # Processor Temperature
    #cputemp=$(sensors | grep "id 0" | awk -F "id 0: " '{print $2}' | awk -F "C " '{print $1}' | sed 's/ +//') && echo "Proccessor temperature is currently $cputemp degrees Centegrade..." | tee /dev/tty | $VOICE
    if hasattr(psutil, "sensors_temperatures"):
##        sys.exit("platform not supported")
        temps = psutil.sensors_temperatures()
        if not temps:
            sDiag+="can't read any temperature\n"
        else:
            for name, entries in temps.items():
#            print(name)
                for entry in entries:
                    sDiag+='Proccessor temperature is currently %.2f degrees Centegrade...\n'%entry.current
                    break
                break
    # Memory Free
    #freemem=$(free -h | grep "Mem:" | awk -F "Mem: " '{print $2}' | awk '{print $3}' | sed 's/G//') && echo "System memory has $freemem Gigabytes free..." | tee /dev/tty | $VOICE
    sDiag+='System memory has %.2f Gigabytes free...\n'%bytes2gb(oa.sys.free_memory)
    # Drive Space Free
    #space=$(df -h /dev/sda1 | awk '{print $4}' | grep G | cut -d "G" -f1 -) && echo "Internal hard drive has $space Gigabytes free..." | tee /dev/tty | $VOICE
#psutil.disk_usage('/')
#oa.sys.disk_usage=sdiskusage(total=21378641920, used=4809781248, free=15482871808, percent=22.5)
    sDiag+='Internal hard drive has %.2f Gigabytes free...\n'%bytes2gb(psutil.disk_usage('/').free)
    # Network Status
    sDiag+=switch(is_online(),True, 'Internet access is currently available.', 'We are offline.')
    say(sDiag)

def answer(text):
    """
      save ret func parameter
      and switch `mind` to previous
    """
##    info('AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA:   ',text)
    #oa.sys.last_answer=text
    text=text.lower()
    func=oa.mind.user_choices.get(text,None)
    if func:
        call_func(func)
    oa.mind.switch_back()
##    evt_answer.clear()

def user_answer(mind_for_answer, choices):
    """
      within `mind` we will get
      1 command - answer (voice, file path, etc - any) from user
    """
    mind(mind_for_answer,0)#no history
##    #we will start loop in loop, until user say something
##    evt_answer = threading.Event()
##    evt_answer.set()
##    # no loops
##    !!!!!!oa.app.loop(condition=lambda : evt_answer.is_set())
##    info('last answer',oa.sys.last_answer)
    oa.mind.user_choices=choices
##    return oa.sys.last_answer

def call_func(func_or_value):
    """
      helper function.
      For Stubs - call perform
      for others functions - direct call.
    """
    if isCallable(func_or_value):
        if isinstance(func_or_value,Stub):
            return func_or_value.perform()
        else:
            return func_or_value()
    else:
        return func_or_value

def yes_no(msg,func):
    """
      we want to get answer from user.
      we will use here `yes_no` - mind.
    """
    say(msg)
    user_answer('yes_no',{'yes':func})
#        info("yes_no->yes. let's start function")


def close():
    """
      close Assistant
    """
    quit()

def say_last_user_phrase(s=''):
    say(s+' '+oa.last_phrase)

def lines_to_dict(sLines,func=lambda s : s, params={}):
    """
      tranlate dict string
      where
         end of line - separator between keys
         : - separator between key and value
         params and oa.sys dicts - is using to fill parameters :
            %(param)s, %(user)s etc
      Example string:
       key1 : value1
       key2 : value2
       ...
       you there? : yes... i am here...
       you think : i think sometimes...
    """
    params.update(oa.sys.__dict__)
    sLines=sLines%params
    ret=dict([[k,func(v)] for k,v in [[x.strip() for x in ph.split(':')] for ph in sLines.split('\n') if ph.strip()!='']])
    return ret

def isNum(s):
    return s.replace('.','').isdigit()

def expr2str():
    ret=''
    #calc_opers=lines_to_dict(fread('nums'))
    info(oa.sys.calc_opers.values())
    for k, g in groupby(oa.sys.expr, lambda x: ((x in oa.sys.calc_opers.values()) and 1) or 2):
        l=list(g)
        if len(l)>1:
            if k==1:#oper
                raise Exception('two opers')
            else:
                sr='('+l[0]
                for x in l[1:]:
                    if isNum(x):
                        sr+='+'+x
                    else:
                        #'hundreds, thousands so on'
                        sr+=x
                ret+=sr+')'
        else:
            ret+=l[0]
    return ret

def calculate():
#    info('test1')
#    info(oa.sys.expr)
#    if isNum(s) and isNum(oa.sys.last_expr):
#        oa.sys.expr+='+'
    ret=expr2str()
    info(oa.sys.expr)
    info('expr='+ret)
    try:
        say(eval(ret))
    except:
        say('Error. wrong expression. '+ret)
    #clear expr
    oa.sys.expr=[]

def add2expr(s):
    #check for calc - we must move it to nums def file
    #for nums we will add sum oper
    oa.sys.expr.append(s)

def quit_app():
    quit(0)

##oa.sys.lines_to_dict=lines_to_dict
#print(bytes2gb(oa.sys.free_memory))
#info('oa',oa)
