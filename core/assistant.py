# Open Assistant 0.03
# 2016 General Public License V3
# By Andrew Vavrek, Clayton G. Hobbs, Jezra, Jonathan Kulp

# core.py - Open Assistant System Core

import logging
logger = logging.getLogger(__name__)

class Assistant:

    def __init__(self, path=None, config=None):
        logger.info("Loading Assistant: {}".format(path))
        self.path = path

        logger.debug("Configuring Assistant: {}".format(str(config)))
        self.config = config if config is not None else {}

        from core import Config
        self.config = Config(path=self.path)

        logger.debug("Assistant Configured: {}".format(self.config))
        self.history = []
