import logging
_logger = logging.getLogger(__name__)

import threading

import oa.legacy


""" CORE FUNCTIONS """

def thread_name():
    """ Return the current thread name. """
    return threading.current_thread().name.split(' ')[0]

def current_part():
    """ Return the part name which is associated with the current thread. """
    name = thread_name()
    if name in oa.legacy.hub.parts:
        return oa.legacy.hub.parts[name]
    else:
        err = '%s Error: Cannot find a related part' %name
        _logger.error(err)
        raise Exception(err)

def call_function(func_or_value):
    """ A helper function. For Stubs, call `perform()`.
        For other functions, execute a direct call. """
    if oa.legacy.isCallable(func_or_value):
        if isinstance(func_or_value, oa.legacy.Stub):
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
    if hasattr(oa.legacy.hub.parts, 'console') and not oa.legacy.hub.finished.is_set():
        oa.legacy.hub.parts.console.wire_in.put(string)
    else:
        print(string)

def get(part = None, timeout = .1):
    """ Get a message from the wire. If there is no part found, take a message from the current wire input thread. (No parameters. Thread safe) """
    if part is None:
        part = current_part()
    while not oa.legacy.hub.finished.is_set():
        try:
            return part.wire_in.get(timeout = timeout)
        except oa.legacy.queue.Empty:
            pass
    raise Exception('Open Assistant closed.')

def put(part, value):
    """ Put a message on the wire. """
    _logger.debug(f"PUT Called... {part} <- {value}")
    oa.legacy.hub.parts[part].wire_in.put(value)

def empty(part = None):
    """ Remove all messages from `part.wire_in` input queue.
        (No parameters. Thread safe) """
    if part is None:
        part = current_part()
    try:
        while True:
            part.wire_in.get(False)
    except oa.legacy.queue.Empty:
        pass

def quit_app():
    quit(0)

def close():
    """ Close Open Assistant. """
    quit()