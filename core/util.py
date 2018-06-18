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
