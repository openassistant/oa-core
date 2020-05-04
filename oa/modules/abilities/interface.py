import oa.boop

from oa.modules.abilities.core import info, put
from oa.modules.abilities.interact import say
from oa.modules.abilities.system import find_file, sys_exec

def activate(s):
    """ Activate a specific window. """
    if oa.sys.os == 'win':
        w = WindowMgr()
        w.find_window_wildcard('.*' + s + '.*')
        w.set_foreground()
    else:
        raise Exception('`Activate` is unsupported.')

def close(s):
    """ Close an application by a window or process name.
        A partial window name will work, for example: 'note*'. """
    say('- Unable to close %s for now.' %s)
    pass

def volume(move = 2):
    """ Change volume level.
        Positive `move`: Volume Up
        Negative `move`: Volume Down 
    """
    if oa.sys.os == 'win':
        # Up by 2.
        if move > 0:
            # Volume up.
            key = chr(175)
        else:
            move =- move
            key = chr(174)

        while move > 0:
            wshell.SendKeys(key)
            move -= 2

    elif oa.sys.os in ('linux','mac'):
        if move > 0:
            sys_exec('pamixer --increase %d' %move)
        else:
            sys_exec('pamixer --decrease %d' %(-move))
    else:
        info('Unknown operating system.')

def mute(mute = True):
    """ Mute or unmute speakers. """
    if oa.sys.os == 'win':
        wshell.SendKeys(chr(173))
    elif oa.sys.os in ('linux', 'mac'):
        sys_exec('amixer set Master %smute' % (((not mute) and 'un') or ''))
    else:
        info('Unknown operating system.')

def unmute():
    """ Unmute speakers. """
    mute(False)
