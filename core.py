# core.py - Essential OA classes and functions.

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

import logging
logging.basicConfig(filename = 'oa.log', level = logging.INFO)


""" CORE FUNCTIONS AND CLASSES """

def isCallable(obj):
    """ Return True if an object is callable, or False if not. """
    return hasattr(obj, "__call__")

def switch(*args):
    """ Switch function for counting variable arguments.
        Example: switch(var, 'aa', 1, 'bb', 2, 4)
        Similar to:
        if var == 'aa' return 1
        elif var == 'bb' return 2
        else return 4
    """
    lA = len(args)
    if lA <= 2:
        raise Exception('Switch: Wrong argument number.\n Arguments = %s' %str(args))

    # If not found, return None.
    ret = None
    if lA % 2 == 0:
        # With else statement.
        ret = args[-1]
        args = args[:-1]
    # Check key:value via dictionary.
    return dict(zip(args[1::2], args[2::2])).get(args[0], ret)

class Core(object):
    """ General template to store all properties. If attributes do not exist, assign them and return Core(). """
    def __init__(_, *args, **kwargs):
        if args:
            _.args = args
        # Get keyword arguments.
        _.__dict__.update(kwargs)

    def __nonzero__(_):
        return len(_.__dict__)

    def __bool__(_):
         return len(_.__dict__) > 0

    def __getitem__(_, key):
        if not isinstance(key, str):
            print(key)
        return getattr(_, key)

    def __setitem__(_, key, value):
        setattr(_, key, value)

    def __getattribute__(_, name):
        """ If an attribute is a function without arguments, return the call. """
        try:
            attributes = object.__getattribute__(_, name)
        except AttributeError as e:

            # For unknown attributes, return a fresh instance of Core (except for system attributes `__*__`).
            if name.startswith('__') and name.endswith('__'):
                raise
            attributes = Core()
            object.__setattr__(_, name, attributes)

        if isCallable(attributes):
            insp = inspect.getargspec(attributes)
            if (len(insp.args) == 0) and (attributes.__name__ == '<lambda>'):
                # Return the function call result.
                return attributes()
        return attributes

class Stub():
    """ Stubs for delayed command calls. """
    def __init__(_,o, *args, **kwargs):
        _.commands = [[o,args,kwargs]]

    def __and__(_,o):
        _.commands.append(o.commands[0])
        return _

    def __add__(_, o):
        """ Redirect to `__and__` operator. """
        return _ & o

    def __call__(_,*args,**kwargs):
        """ Fill function parameters all at once for real calls and use `perform()`. """
        ret = Stub(_.commands[0][0])
        ret.commands[0][1] = args
        ret.commands[0][2] = kwargs
        return ret

    def perform(_):
        """ Call all functions one by one. """
        ret = []
        for func, args, kwargs in _.commands:
            # Check arguments for Stubs and perform them.
            ret.append(func(*args, **kwargs))
        if len(ret) == 1:
            return ret[0]
        else:
            return ret

    @classmethod
    def prepare_stubs(_, module):
        """ Return dictionary with Stubs of all functions in related `module`. """
        # Nowait - to call a function without delays.
        ret = {}
        for name, body in module.__dict__.items():

            # oa.sys and other Core instances.
            if isinstance(body, Core):
                ret[name] = body
            else:
                if hasattr(body, '__call__'):
                    # Calling a function with an underscore `_` prefix will execute it immediately without a Stub.
                    ret['_' + name] = body
                    ret[name] = Stub(body)

        return ret

    @classmethod
    def test(_):
        c1 = Stub(play)
        c2 = Stub(mind)
        ret = c1('beep_hello.wav') & c2('root')

        # Execute all.
        ret.perform()


""" CORE VARIABLE ASSIGNMENTS """

oa = Core()

oa.sys.os = switch(platform.system(),'Windows','win','Linux','linux','Darwin','mac','unknown')
oa.sys.user = getpass.getuser()
oa.sys.host = socket.gethostname()
oa.sys.ip = socket.gethostbyname(oa.sys.host)
oa.sys.free_memory = lambda : psutil.virtual_memory()[4]

# Date functions.
oa.sys.now = lambda : datetime.datetime.now()
oa.sys.second = lambda : oa.sys.now.second
oa.sys.minute = lambda : oa.sys.now.minute
oa.sys.hour = lambda : oa.sys.now.hour
oa.sys.day = lambda : oa.sys.now.day
oa.sys.day_name = lambda : oa.sys.now.strftime("%A")
oa.sys.month = lambda : oa.sys.now.month
oa.sys.month_name = lambda : oa.sys.now.strftime("%B")
oa.sys.year = lambda : oa.sys.now.year
oa.sys.date_text = lambda : '%d %s %d' %(oa.sys.day, oa.sys.month_name,oa.sys.year)
oa.sys.time_text = lambda : '%d:%d' %(oa.sys.hour, oa.sys.minute)
oa.sys.date_time_text = lambda : oa.sys.date_text + ' ' + oa.sys.time_text

if oa.sys.os == 'win':
    global wshell
    import win32com.client
    from win32com.client import Dispatch as CreateObject
    wshell = CreateObject("WScript.Shell")

    # Windows processing.
    import win32gui
    import re

    class WindowMgr:
        """ Encapsulates calls to the WinAPI for window management. """

        def __init__ (self):
            """ Constructor. """
            self._handle = None

        def find_window(self, class_name, window_name = None):
            """ Find a window by its class_name. """
            self._handle = win32gui.FindWindow(class_name, window_name)

        def _window_enum_callback(self, hwnd, wildcard):
            """ Pass to win32gui.EnumWindows() to check all opened windows. """
            if re.match(wildcard, str(win32gui.GetWindowText(hwnd))) is not None:
                self._handle = hwnd

        def find_window_wildcard(self, wildcard):
            """ Find a window whose title matches a wildcard regex. """
            self._handle = None
            win32gui.EnumWindows(self._window_enum_callback, wildcard)

        def set_foreground(self):
            """ Put a window in the foreground. """
            win32gui.SetForegroundWindow(self._handle)


""" CORE FUNCTIONS """

def answer(text):
    """ Save the return function parameter and switch to previous mind. """
    text = text.lower()
    func = oa.mind.user_choices.get(text, None)
    if func:
        call_function(func)
    oa.mind.switch_back()

def call_function(func_or_value):
    """ A helper function. For Stubs, call `perform()`.
        For other functions, execute a direct call. """
    if isCallable(func_or_value):
        if isinstance(func_or_value, Stub):
            return func_or_value.perform()
        else:
            return func_or_value()
    else:
        return func_or_value

def close():
    """ Close Open Assistant. """
    quit()

def current_part():
    """ Return the part name which is associated with the current thread. """
    name = thread_name()
    ret = oa.core.parts.get(name, None)
    if ret is None:
        err = '%s Error: Cannot find a related part' %name
        info(err)
        raise Exception(err)
    return ret

def download_file(url, path):
    """ Download a file by url and save it to a local path. """
    r = requests.get(url, stream = True)
    if r.status_code == 200:
        with open(path, 'wb') as f:
            for chunk in r:
                f.write(chunk)

def empty(part = None):
    """ Remove all messages from `part.wire_in` input queue.
        (No parameters. Thread safe) """
    if part is None:
        part = current_part()
    try:
        while True:
            part.wire_in.get(False)
    except queue.Empty:
        pass

def find_file(fname):
    """ Search for a file with `fname` in all OA sub-directories.
        Able to use a short name if it is unique.
        NEED FIX - Put file names into Cache list ? """
    core_directory = os.path.dirname(__file__)
    ret = glob.glob(os.path.join(core_directory,'minds/*/%s' %fname))
    if not ret:
        ret = glob.glob(os.path.join(core_directory,'minds/*/*/%s' %fname))
    if len(ret) != 1:
        raise Exception('%s: found %d results.' %(fname, len(ret)))
    return ret[0]

def read_file(fname, result_as_list = 0):
    """ Read the contents of a file and return a string or a list of strings split by a new line symbol. """
    try:
        info('- Reading file: ', fname)
        if not os.path.exists(fname):
            fname = find_file(fname)
        with open(fname, 'r') as f:
            if result_as_list:
                return f.readlines()
            else:
                return f.read()
    except: # FileNotFoundError:
        info("- Error loading file: {path}".format(path = fname))
        # logger.warn("Error loading file: {path}".format(path = fname))
        return ''

def get(part = None, timeout = .1):
    """ Get a message from the wire. If there is no part found, take a message from the current wire input thread. (No parameters. Thread safe) """
    if part is None:
        part = current_part()
    if part.name == 'mind':
        info('- Listening: ', part.name)
    while oa.alive:
        try:
            return part.wire_in.get(timeout = timeout)
        except queue.Empty:
            pass
    raise Exception('Open Assistant closed.')

def info(*args, **kwargs):
    """ Display information to the screen. """
    string = thread_name() + ' '
    if args:
        string += ' '.join([str(v) for v in args]) + '\n'
    if kwargs:
        string += '\n'.join([' %s: %s' %(str(k), str(v)) for k, v in args.items()])
    if oa.console and oa.alive:
        oa.console.wire_in.put(string)
    else:
        print(string)

    logging.info(string)

def lines_to_dict(sLines, func = lambda s : s, params = {}):
    """ Tranlate dictionary string.
      where
         end of line - separator between keys
         : - separator between key and value
         params and oa.sys dicts - is using to fill parameters:
            %(param)s, %(user)s etc
      Example string:
       key1 : value1
       key2 : value2
       ...
       You there?: yes... i am here...
       You think: i think sometimes...
    """
    params.update(oa.sys.__dict__)
    sLines = sLines %params
    ret = dict([[k, func(v)] for k, v in [[x.strip() for x in ph.split(':')] for ph in sLines.split('\n') if ph.strip() != '']])
    return ret

def mind(name, history = 1):
    """ Switch the current mind to `name`. """
    oa.mind.set_mind(name, history)

def put(part, value):
    """ Put a message on the wire. """
    oa[part].wire_in.put(value)

def quit_app():
    quit(0)

def thread_name():
    """ Return the current thread name. """
    return threading.current_thread().name.split(' ')[0]

def write_file(fname, data, append = False):
    """ Write data to a file. """
    if append:
        with open(fname, 'w+') as f:
            f.write(data)
    else:
        with open(fname, 'w') as f:
            f.write(data)


""" CORE ABILITY FUNCTIONS (Move to new `abilities` folder in separate files.) """

def activate(s):
    """ Activate a specific window. """
    if oa.sys.os == 'win':
        w = WindowMgr()
        w.find_window_wildcard('.*' + s + '.*')
        w.set_foreground()
    else:
        raise Exception('`Activate` is unsupported.')

def add2expr(s):
    # Check for calculator. Move to a numbers definition file.
    # For numbers, add sum operator.
    oa.sys.expr.append(s)

def bytes2gb(size):
    """ Convert size from bytes to gigabytes.
        Precision: 2 digits after point. """
    return size / float(1 << 30)

def calculate():
    ret = expr2str()
    info(oa.sys.expr)
    info('expr=' + ret)
    try:
        say(eval(ret))
    except:
        say('Error. Wrong expression. ' + ret)
    # Clear the expression.
    oa.sys.expr = []

def close(s):
    """ Close an application by a window or process name.
        A partial window name will work, for example: 'note*'. """
    say('- Unable to close %s for now.' %s)
    pass

def diagnostics():
    """ Run system diagnostics. """
    response = '- Running diagnostics... '

    # Processor Temperature.
    if hasattr(psutil, "sensors_temperatures"):
        temps = psutil.sensors_temperatures()
        if not temps:
            response += "Unable to read temperature.\n"
        else:
            for name, entries in temps.items():
                for entry in entries:
                    response += 'Proccessor temperature is currently %.0f degrees Centegrade...\n' %entry.current
                    break
                break

    # Memory Free.
    response += 'System memory has %.0f Gigabytes free...\n' %bytes2gb(oa.sys.free_memory)

    # Drive Space Free.
    response += 'Internal hard drive has %.0f Gigabytes free...\n' %bytes2gb(psutil.disk_usage('/').free)

    # Network Status.
    response += switch(is_online(), True, 'Internet access is currently available.', 'We are offline.')

    say(response)

def expr2str():
    """ Convert a numerical expression into a string. """
    ret = ''
    info(oa.sys.calc_opers.values())
    for k, g in groupby(oa.sys.expr, lambda x: ((x in oa.sys.calc_opers.values()) and 1) or 2):
        l=list(g)
        if len(l) > 1:
            if k == 1:
                raise Exception('two opers')
            else:
                sr='(' + l[0]
                for x in l[1:]:
                    if isNum(x):
                        sr += '+' + x
                    else:
                        # 'hundreds, thousands so on'
                        sr += x
                ret += sr + ')'
        else:
            ret += l[0]
    return ret

def get_sys(s):
    """ Return system information from `oa.sys`. """
    return getattr(oa.sys, s)

def isNum(s):
    return s.replace('.', '').isdigit()

def is_online(host = '8.8.8.8', port = 53, timeout = 1):
    """ If online Return True, if not return False.
     Host: 8.8.8.8 (google-public-dns-a.google.com)
     OpenPort: 53/tcp
     Service: domain (DNS/TCP) """
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except Exception as ex:
        info(ex.message)
        return False

def keys(s):
    """ Hook and simulate keyboard events. """
    if '+' in s:
        keyboard.press_and_release(s)
    else:
        keyboard.write(s)

def mute(mute = True):
    """ Mute or unmute speakers. """
    if oa.sys.os == 'win':
        wshell.SendKeys(chr(173))
    elif oa.sys.os in ('linux', 'mac'):
        sys_exec('amixer set Master %smute'(((not mute) and 'un') or ''))
    else:
        info('Unknown operating system.')

def play(fname):
    """ Play a sound file. """
    put('sound', find_file(fname))

def random_from_file(fname):
    l = read_file(fname, result_as_list = 1)
    return random.choice(l)

def read_forecast():
    import forecastio
    """ Get the weather forecast from Dark Sky (darksky.net).
    Get your API key and longitude / latitude at: https://darksky.net/dev/
    Install 'forecastio' module with: `pip install python-forcastio` """

    # Weather For Amberg, Germany.

    api_key = "e3f8667cb539171dc2f4b389d33648ce"
    lat = 49.44287
    lng = 11.86267

    forecast = forecastio.load_forecast(api_key, lat, lng, lang='en')
    byNow = forecast.currently()
    byHour = forecast.hourly()
    byDay = forecast.daily()
    weather_summary = """ - The weather is currently %s.\n The temperature is %d degrees Celsius.\n %s \n %s""" %(byNow.summary, int(byNow.temperature),byHour.summary,byDay.summary)
    say(weather_summary)

def read_news_feed(news_feed, category):
    rss = feedparser.parse(news_feed)
    info(rss['feed']['title'])
    say('- Reading %s news.' %category)
    headline_count = 1

    # Amount of headlines to read.
    headline_amount = 5

    for post in rss.entries:
        if(headline_count == headline_amount):
            break
        else:
            headline = post.title
            exclude = set(string.punctuation)
            headline = ''.join(ch for ch in headline if ch not in exclude)
            say(headline)
            headline_count += 1


def say(text):
    """ Text to speech using the `oa.audio.say` defined function. """
    text = call_function(text)
    info(text)
    oa.sys.last_say = text

    # Put message into voice.
    put('voice', text)

def say_random(slist):
    return random.choice([x.strip() for x in slist.split(',')])

def say_time():
    """ Speak the current time. """
    time = oa.sys.time_text
    say('- The time is %s.' %time)

def say_day():
    """ Speak the current day. """
    day = oa.sys.day_name
    say('- Today is %s.' %day)

def say_last_command(string = ''):
    say(string + ' ' + oa.last_command)

def stat_size(fname):
    """ Return a file size. """
    return os.stat(fname).st_size

def stat_mtime(fname):
    """ Return the last modification time of a file in seconds. """
    return os.stat(fname).st_mtime

def sys_exec(cmd):
    """ Execute a command. """
    subprocess.call(cmd, shell = True)

def unmute():
    """ Unmute speakers. """
    mute(False)

def user_answer(mind_for_answer, choices):
    """ Within any `mind` we will receive a one word answer command (voice, file path, etc, any) from the user. """
    mind(mind_for_answer, 0) # No history.
    oa.mind.user_choices = choices

def volume(move = 2):
    """ Change volume level.
        Positive `move`: Volume Up
        Negative `move`: Volume Down 
    """
    if oa.sys.os == 'win':
        # Up by 2.
        if move > 0:
            # Volume up.
            key = chr(175)
        else:
            move =- move
            key = chr(174)

        while move > 0:
            wshell.SendKeys(key)
            move -= 2

    elif oa.sys.os in ('linux','mac'):
        if move > 0:
            sys_exec('pamixer --increase %d' %move)
        else:
            sys_exec('pamixer --decrease %d' %(-move))
    else:
        info('Unknown operating system.')

def yes_no(msg, func):
    """ Receive a yes or no answer from the user. """
    say(msg)
    user_answer('yes_no', {'yes': func})