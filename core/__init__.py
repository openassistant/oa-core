# core.py - Essential OA classes and functions.

import datetime
import getpass
import inspect
import platform
import socket
import psutil

import itertools
from itertools import *

try:
    import queue
except:
    import Queue as queue

from core.util import isCallable, switch


""" CORE FUNCTIONS AND CLASSES """

def command_registry(kws):
    def command(cmd):
        def _command(fn):
            if type(cmd) == str:
                kws[cmd.upper()] = fn
            elif type(cmd) == list:
                for kw in cmd:
                    kws[kw.upper()] = fn
            return fn
        return _command
    return command

class Core(object):
    """ General template to store all properties. If attributes do not exist, assign them and return Core(). """
    def __init__(self, *args, **kwargs):
        if args:
            self.args = args
        # Get keyword arguments.
        self.__dict__.update(kwargs)

    def __nonzero__(self):
        return len(self.__dict__)

    def __bool__(self):
         return len(self.__dict__) > 0

    def __getitem__(self, key):
        if not isinstance(key, str):
            print(key)
        return getattr(self, key)

    def __setitem__(self, key, value):
        setattr(self, key, value)

    def __getattribute__(self, name):
        """ If an attribute is a function without arguments, return the call. """
        try:
            attributes = object.__getattribute__(self, name)
        except AttributeError as e:

            # For unknown attributes, return a fresh instance of Core (except for system attributes `__*__`).
            if name.startswith('__') and name.endswith('__'):
                raise
            attributes = Core()
            object.__setattr__(self, name, attributes)

        if isCallable(attributes):
            insp = inspect.getargspec(attributes)
            if (len(insp.args) == 0) and (attributes.__name__ == '<lambda>'):
                # Return the function call result.
                return attributes()
        return attributes

class Stub():
    """ Stubs for delayed command calls. """
    def __init__(self, o, *args, **kwargs):
        self.commands = [[o,args,kwargs]]

    def __and__(self, o):
        self.commands.append(o.commands[0])
        return self

    def __add__(self, o):
        """ Redirect to `__and__` operator. """
        return self & o

    def __call__(self, *args,**kwargs):
        """ Fill function parameters all at once for real calls and use `perform()`. """
        ret = Stub(self.commands[0][0])
        ret.commands[0][1] = args
        ret.commands[0][2] = kwargs
        return ret

    def perform(self):
        """ Call all functions one by one. """
        ret = []
        for func, args, kwargs in self.commands:
            # Check arguments for Stubs and perform them.
            ret.append(func(*args, **kwargs))
        if len(ret) == 1:
            return ret[0]
        else:
            return ret

    @classmethod
    def prepare_stubs(self, module):
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

