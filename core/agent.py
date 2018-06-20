# Open Assistant

import logging
import os
import threading

from . import Core

class Agent:

    def __init__(self, home=None, **opts):
        logging.debug(self)

        self.home = home if home is not None else os.getcwd()
        self.config = opts
