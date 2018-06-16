# console.py - System text display.

from core import oa
from abilities.core import get

def _in():
    while not oa.core.finished.is_set():
        # Print messages from the queue.
        print(get())
        yield ''
