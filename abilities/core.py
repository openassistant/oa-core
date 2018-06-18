import threading

from core import oa, queue, Stub
from core.util import isCallable, bytes2gb


""" CORE FUNCTIONS """

def thread_name():
    """ Return the current thread name. """
    return threading.current_thread().name.split(' ')[0]

def current_part():
    """ Return the part name which is associated with the current thread. """
    name = thread_name()
    ret = oa.core.parts.get(name, None)
    if ret is None:
        err = '%s Error: Cannot find a related part' %name
        info(err)
        raise Exception(err)
    return ret

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

def put(part, value):
    """ Put a message on the wire. """
    oa[part].wire_in.put(value)

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

def quit_app():
    quit(0)

def close():
    """ Close Open Assistant. """
    quit()