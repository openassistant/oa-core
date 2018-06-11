# console.py - System text display.

from core import oa
from abilities.core import get

def _in():
    while oa.alive:
        # Print messages from the queue.
        print(get())
        yield ''
