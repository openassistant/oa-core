# core.py - Essential OA classes and functions.

import datetime
import getpass
import importlib
import inspect
import logging
import os
import platform
import psutil
import socket

import itertools
from itertools import *

try:
    import queue
except:
    import Queue as queue


""" CORE VARIABLE ASSIGNMENTS """
from .util import Core, switch

oa = Core()

oa.sys = Core()
oa.sys.os = switch(platform.system(),'Windows','win','Linux','linux','Darwin','mac','unknown')
oa.sys.user = getpass.getuser()
oa.sys.host = socket.gethostname()
oa.sys.ip = socket.gethostbyname(oa.sys.host)
oa.sys.free_memory = lambda : psutil.virtual_memory()[4]

# Date functions.
oa.sys.now = lambda : datetime.datetime.now()
oa.sys.second = lambda : oa.sys.now().second
oa.sys.minute = lambda : oa.sys.now().minute
oa.sys.hour = lambda : oa.sys.now().hour
oa.sys.day = lambda : oa.sys.now().day
oa.sys.day_name = lambda : oa.sys.now().strftime("%A")
oa.sys.month = lambda : oa.sys.now().month
oa.sys.month_name = lambda : oa.sys.now().strftime("%B")
oa.sys.year = lambda : oa.sys.now().year
oa.sys.date_text = lambda : '%d %s %d' %(oa.sys.day(), oa.sys.month_name(), oa.sys.year())
oa.sys.time_text = lambda : '%d:%d' %(oa.sys.hour(), oa.sys.minute())
oa.sys.date_time_text = lambda : oa.sys.date_text() + ' ' + oa.sys.time_text()
