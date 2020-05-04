import keyboard

import oa.boop

from oa.modules.abilities.core import call_function, put
from oa.modules.abilities.system import find_file


def answer(text):
    """ Save the return function parameter and switch to previous mind. """
    text = text.lower()
    func = oa.boop.mind.user_choices.get(text, None)
    if func:
        call_function(func)
    oa.boop.mind.switch_back()

def yes_no(msg, func):
    """ Receive a yes or no answer from the user. """
    say(msg)
    user_answer('yes_no', {'yes': func})

def user_answer(mind_for_answer, choices):
    """ Within any `mind` we will receive a one word answer command (voice, file path, etc, any) from the user. """
    mind(mind_for_answer, 0) # No history.
    oa.boop.mind.user_choices = choices

def say(text):
    """ Text to speech using the `oa.audio.say` defined function. """
    text = call_function(text)
    oa.boop.sys.last_say = text

    # Put message into voice.
    put('voice', text)

def keys(s):
    """ Hook and simulate keyboard events. """
    if '+' in s:
        keyboard.press_and_release(s)
    else:
        keyboard.write(s)

def play(fname):
    """ Play a sound file. """
    put('sound', find_file(fname))

def mind(name, history = 1):
    """ Switch the current mind to `name`. """
    oa.boop.hub.parts['mind'].set_mind(name, history)
