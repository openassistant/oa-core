# core.py - Essential OA classes and functions.

import datetime
import getpass
import importlib
import inspect
import logging
import os
import platform
import psutil
import queue
import socket


def bytes2gb(size):
    """ Convert size from bytes to gigabytes.
        Precision: 2 digits after point. """
    return size / float(1 << 30)


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
        return getattr(self, key)

    def __setitem__(self, key, value):
        setattr(self, key, value)

    def __iter__(self):
        yield from self.__dict__

    def __len__(self):
        return len(self.__dict__)


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

mind = None
minds = {}

sys = Core()

sys.os = switch(platform.system(),'Windows','win','Linux','linux','Darwin','mac','unknown')
sys.user = getpass.getuser()
sys.host = socket.gethostname()
#sys.ip = socket.gethostbyname(oa.sys.host)
sys.free_memory = lambda : psutil.virtual_memory()[4]

# Date functions.
sys.now = lambda : datetime.datetime.now()
sys.second = lambda : sys.now().second
sys.minute = lambda : sys.now().minute
sys.hour = lambda : sys.now().hour
sys.day = lambda : sys.now().day
sys.day_name = lambda : sys.now().strftime("%A")
sys.month = lambda : sys.now().month
sys.month_name = lambda : sys.now().strftime("%B")
sys.year = lambda : sys.now().year
sys.date_text = lambda : '%d %s %d' %(sys.day(), sys.month_name(), sys.year())
sys.time_text = lambda : '%d:%d' %(sys.hour(), sys.minute())
sys.date_time_text = lambda : sys.date_text() + ' ' + sys.time_text()
