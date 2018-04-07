import os, sys, glob, random
import subprocess, requests
import playsound
import keyboard
import platform
import datetime
import getpass,socket
import psutil

unknown_os='unknown operating system'

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
    """
    def __init__(_,*args,**kwargs):
        _.args=args
        #simply update from kwargs
        _.__dict__.update(kwargs)

sys_info=AnyProp()
#common sys_info funcs
#      OS name : 'win','mac','linux'
sys_info.os=switch(platform.system(),'Windows','win','Linux','linux','Darwin','mac','unknown')
sys_info.user=getpass.getuser()
sys_info.host=socket.gethostname()
sys_info.ip=socket.gethostbyname(sys_info.host)
#date funcs
#property(fget=None, fset=None, fdel=None, doc=None)
sys_info.now=property(fget=lambda : datetime.datetime.now())
sys_info.second=property(fget=lambda : sys_info.now.second)
sys_info.hour=property(fget=lambda : sys_info.now.hour)
sys_info.day=property(fget=lambda : sys_info.now.day)
sys_info.month=property(fget=lambda : sys_info.now.month)
sys_info.month_name=property(fget=lambda : sys_info.now.strftime("%B"))
sys_info.year=property(fget=lambda : sys_info.now.year)
sys_info.date_text=property(fget=lambda : '%d %s %d'%(sys_info.day,sys_info.month_name,sys_info.year))
sys_info.time_text=property(fget=lambda : '%d:%d'%(sys_info.hour,sys_info.second))
sys_info.date_time_text=property(fget=lambda : sys_info.date_text+' '+sys_info.time_text)
sys_info.free_memory=property(fget=lambda : psutil.virtual_memory()[-1])
#sys_info.public_ip=

if sys_info.os=='win':
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

#import logging
#logger = logging.getLogger(__name__)
#info=logger.info

oa=None

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
    if sys_info.os=='win':
        w = WindowMgr()
        w.find_window_wildcard('.*'+s+'.*')
        w.set_foreground()
    else:
        raise Exception('`activate` is unsupported')

def _sys(s):
    """
      returns system information from sys_info
    """
    return getattr(sys_info,s)

def info(*args):
#    logger.info(args)
    if len(args)==1:
        print(args[0])
    else:
        print(args)

def close(s):
    """
      close app by window or process name
      (partial window name will works too : 'note*')
    """
    say('cannot close %s for now'%s)
    pass

def mute(mute=True):
    """set mute/unmute for speakers"""
    if sys_info.os=='win':
        wshell.SendKeys(chr(173))
    elif sys_info.os in ('linux','mac'):
        sys_exec('amixer set Master %smute'(((not mute) and 'un') or ''))
    else:
        info(unknown_os)

def unmute():
    """set unmute for speakers"""
    mute(false)

def volume(move=2):
    """
      chnage value of Volume :
        positive `move` - Volume Up
        negative `move` - Volume Down
    """
    if sys_info.os=='win':
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
    elif sys_info.os in ('linux','mac'):
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
    info(text)
    sys_info.last_say=text
    oa.audio.say(text)

def say_random(slist):
    return random.choice([x.strip() for x in slist.split(',')])

def random_from_file(fname):
    l=fread(find_file(fname),result_as_list=1)
    return random.choice(l)

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

def fread(fname, result_as_list=0):
    try:
        with open(fname, 'r') as f:
            if result_as_list:
                return f.readlines()
            else:
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
        info('init',o, args, kwargs)

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
            args=[(isinstance(x,Stub) and x.perform()) or x for x in args]
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
            if name==_.__name__:
                continue

            #sys_info and others AnyProp instances
            if isinstance(body,AnyProp):
                ret[name]=body
            else:
                #direct call without stub
##                setattr(nowait,name,body)
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
    rss = feedparser.parse()
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
The temperature is %d degrees Celsius ..."""%(byNow.summary,int(byNow.temperature),byHour.summary,byDay.summary)
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
    sDiag+='System memory has %.2f Gigabytes free...\n'%bytes2gb(sys_info.free_memory)
    # Drive Space Free
    #space=$(df -h /dev/sda1 | awk '{print $4}' | grep G | cut -d "G" -f1 -) && echo "Internal hard drive has $space Gigabytes free..." | tee /dev/tty | $VOICE
#psutil.disk_usage('/')
#sys_info.disk_usage=sdiskusage(total=21378641920, used=4809781248, free=15482871808, percent=22.5)
    sDiag+='Internal hard drive has %.2f Gigabytes free...\n'%bytes2gb(psutil.disk_usage('/').free)
    # Network Status
    sDiag+=switch(is_online(),True, 'Internet access is currently available.', 'We are offline.')
    say(sDiag)

def answer(text):
    """
      save ret func parameter
      and switch `mind` to previous
    """
    sys_info.last_answer=text

def user_answer(mind):
    """
      within `mind` we will get
      1 command - answer (voice, file path, etc - any) from user
    """
    sys_info.last_answer=None
    oa.switch(mind)
    #we will start loop in loop, until user say something
    oa.loop(condition=lambda : sys_info.last_answer is None)
    oa.switch_back()
    return sys_info.last_answer

def yes_no(msg,func):
    """
      we want to get answer from user.
      we will use here `yes_no` - mind.
    """
    say(msg)
    if user_answer('yes_no')=='yes':
        func()

def close():
    """
      close Assistant
    """
    quit()

def say_last_user_phrase(s=''):
    say(s+' '+oa.last_phrase)
