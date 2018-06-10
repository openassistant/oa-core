# mind.py - Core mind operations.

import os

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

    cf_data = read_file(mind.module)
    d_exec = dict(oa.core.stub_funcs.items())
    exec(cf_data, d_exec)
    
    # Add command keywords without spaces.
    mind.kws = {}
    for key, value in d_exec['kws'].items():
        for synonym in key.strip().split(','):
            mind.kws[synonym] = value

def set_mind(name, history = 1):
    """ Activate new mind. """
    info('- Opening mind: %s' %(name))
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
    info('- Loading minds...')
    for mind in os.listdir(os.path.join(oa.core_directory, 'minds')):
        if mind.lower().endswith('.py'):
            load_mind(mind[:-3])
    info('- All minds are loaded! "Boot mind" is now listening. \n       Say "Boot Mind!" to see if it can hear you. Make sure your microphone is active. \n       Say "Open Assistant!" to launch "root mind". \n       Once root mind loads, say "List Commands!" to hear the commands available.')

def _in():
    global switch_hist
    # History of mind switching.
    switch_hist = []
    load_minds()
    set_mind('boot')

    while oa.alive:
        text = get()
        info('- Text:',text)
        mind = oa.mind.active
        info('%s - Command: %s' %(mind.name, text))
        if (text is None) or (text.strip() == ''):
            # Nothing to do.
            continue
        t = text.lower()

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
                info('- Unknown command: ', str(fn))

