import glob
import logging
import math
import os
import psutil
import random
import socket
import string
import subprocess
import threading

import feedparser
import keyboard
import requests

from core import isCallable, groupby, oa, queue, Stub, switch


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
    core_directory = oa.core_directory
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
    while not oa.core.finished.is_set():
        try:
            return part.wire_in.get(timeout = timeout)
        except queue.Empty:
            pass
    raise Exception('Open Assistant closed.')

def info(*args, **kwargs):
    """ Display information to the screen. """
    string = "[{}]".format(thread_name()) + ' '
    if args:
        string += ' '.join([str(v) for v in args]) + '\n'
    if kwargs:
        string += '\n'.join([' %s: %s' %(str(k), str(v)) for k, v in kwargs.items()])
    if oa.console and not oa.core.finished.is_set():
        oa.console.wire_in.put(string)
    else:
        print(string)

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
        sys_exec('amixer set Master %smute' % (((not mute) and 'un') or ''))
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