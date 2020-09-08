# Open Assistant

import logging
_logger = logging.getLogger(__name__)

import logging
import os
import threading


class Agent:

    def __init__(self, home=None, **opts):
        _logger.debug(self)
        self.finished = threading.Event()

        self.home = home if home is not None else os.getcwd()
        self.modules = opts.get('modules', [])

        self.mind = None
        self.minds = {}
