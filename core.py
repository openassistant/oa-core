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
