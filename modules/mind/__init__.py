# mind.py - Core mind operations.

import importlib
import logging
import os

from abilities.core import read_file, info, call_function, get, sys_exec
from core import oa
from core.util import isCallable

""" Core mind functions. """

def load_mind(name):
    """ Load a mind by its `name`. """
    mind = oa.mind.minds[name]
    mind.name = name
    mind.module = os.path.join(oa.core_directory, 'minds', name +'.py')
    mind.cache_dir = os.path.join(oa.core_directory, 'cache', name)

    # Make directories.
    if not os.path.exists(mind.cache_dir):
        os.makedirs(mind.cache_dir)

    pkg = os.path.split(oa.core_directory)[-1]
    M = importlib.import_module('minds.'+name, package=pkg)
    
    # Add command keywords without spaces.
    mind.kws = {}
    for key, value in M.kws.items():
        for synonym in key.strip().split(','):
            mind.kws[synonym] = value

def set_mind(name, history = 1):
    """ Activate new mind. """
    logging.info('Opening Mind: {}'.format(name))
    if history:
        switch_hist.append(name)
    oa.mind.active = oa.mind.minds[name]
    return oa.mind.active

def switch_back():
    """ Switch back to the previous mind. (from `switch_hist`). """
    set_mind(switch_hist.pop(), 0)

def load_minds():
    """ Load and check dictionaries for all minds. Handles updating language models using the online `lmtool`.
    """
    logging.info('Loading minds...')
    for mind in os.listdir(os.path.join(oa.core_directory, 'minds')):
        if mind.lower().endswith('.py'):
            load_mind(mind[:-3])
    logging.info('Minds loaded!')

def _in():
    # History of mind switching.
    global switch_hist
    switch_hist = []
    
    default_mind = 'boot'
    load_minds()
    set_mind(default_mind)

    logging.debug('"{}" is now listening. Say "Boot Mind!" to see if it can hear you.'.format(default_mind))


    while not oa.core.finished.is_set():
        text = get()
        logging.info('Input: {}'.format(text))
        mind = oa.mind.active
        if (text is None) or (text.strip() == ''):
            # Nothing to do.
            continue
        t = text.upper()

        # Check for a matching command.
        fn = mind.kws.get(t, None)

        if fn is not None:
            # There are two types of commands, stubs and command line text.
            # For stubs, call `perform()`.
            if isCallable(fn):
                call_function(fn)
                oa.last_command = t
            # For strings, call `sys_exec()`.
            elif isinstance(fn, str):
                sys_exec(fn)
                oa.last_command = t
            else:
                # Any unknown command raises an exception.
                raise Exception("Unable to process: {}".format(text))

