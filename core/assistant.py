# Open Assistant 0.03
# 2016 General Public License V3
# By Andrew Vavrek, Clayton G. Hobbs, Jezra, Jonathan Kulp

# core.py - Open Assistant System Core

import logging
logger = logging.getLogger(__name__)

class Assistant:

    def __init__(self, **opts):
        logger.debug(self)
        self.config = opts

        self.history = []
