import logging
import threading

import oa.boop


""" CORE FUNCTIONS """

def thread_name():
    """ Return the current thread name. """
    return threading.current_thread().name.split(' ')[0]

def current_part():
    """ Return the part name which is associated with the current thread. """
    name = thread_name()
    if name in oa.boop.oa.parts:
        return oa.boop.oa.parts[name]
    else:
        err = '%s Error: Cannot find a related part' %name
        logging.error(err)
        raise Exception(err)

def call_function(func_or_value):
    """ A helper function. For Stubs, call `perform()`.
        For other functions, execute a direct call. """
    if oa.boop.isCallable(func_or_value):
        if isinstance(func_or_value, oa.boop.Stub):
            return func_or_value.perform()
        else:
            return func_or_value()
    else:
        return func_or_value

def info(*args, **kwargs):
    """ Display information to the screen. """
    string = "[{}]".format(thread_name()) + ' '
    if args:
        string += ' '.join([str(v) for v in args]) + '\n'
    if kwargs:
        string += '\n'.join([' %s: %s' %(str(k), str(v)) for k, v in kwargs.items()])
    if hasattr(oa.boop.oa.parts, 'console') and not oa.boop.oa.finished.is_set():
        oa.boop.oa.parts.console.wire_in.put(string)
    else:
        print(string)

def get(part = None, timeout = .1):
    """ Get a message from the wire. If there is no part found, take a message from the current wire input thread. (No parameters. Thread safe) """
    if part is None:
        part = current_part()
    while not oa.boop.oa.finished.is_set():
        try:
            return part.wire_in.get(timeout = timeout)
        except oa.boop.queue.Empty:
            pass
    raise Exception('Open Assistant closed.')

def put(part, value):
    """ Put a message on the wire. """
    oa.boop.oa.parts[part].wire_in.put(value)

def empty(part = None):
    """ Remove all messages from `part.wire_in` input queue.
        (No parameters. Thread safe) """
    if part is None:
        part = current_part()
    try:
        while True:
            part.wire_in.get(False)
    except oa.boop.queue.Empty:
        pass

def quit_app():
    quit(0)

def close():
    """ Close Open Assistant. """
    quit()