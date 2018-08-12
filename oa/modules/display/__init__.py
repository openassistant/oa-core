# display.py - Graphical interface  (Let's make this part! 8-).

import logging

from core import oa
from abilities.core import get


def _in():

    while not oa.core.finished.is_set():
        msg = get()
        logging.debug(msg)
