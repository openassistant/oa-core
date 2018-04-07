# Open Assistant

import logging
logger = logging.getLogger(__name__)


class Agent:

    def __init__(self, **opts):
        logger.debug(self)
        self.config = opts
