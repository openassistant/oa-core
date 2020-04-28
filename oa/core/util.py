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


def load_module(path):
    """Load an OA module from path."""
    import os
    import logging
    import importlib
    import queue
    
    # An OA module is a folder with an __oa__.py file
    if not all([
        os.path.isdir(path),
        os.path.exists(os.path.join(path, '__oa__.py')),
    ]): raise Exception("Invalid module: {}".format(path))

    # Import package
    module_name = os.path.basename(path)
    logging.info('{} <- {}'.format(module_name, path))
    M = importlib.import_module("oa.modules"+'.{}'.format(module_name))

    # If the module provides an input queue, link it
    # if getattr(M, '_in', None) is not None:

    m = Core(**M.__dict__)
    m.__dict__.setdefault('wire_in', queue.Queue())
    m.__dict__.setdefault('output', [])
    # m.__dict__.update(M.__dict__)
        
    return m


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
