# Open Assistant 0.21
# 2018 General Public License V3

"""Open Assistant reference implementation."""

import logging
import os
import threading

import core
import core.agent
# from core.agent import Agent

# Setup connections between parts.
# XXX: can't ensure load order yet
# self.parts.ear.output += [self.parts.speech_recognition]
# self.parts.speech_recognition.output += [self.parts.mind]
# oa.core.parts.keyboard.output = [oa.mind, oa.display]
# oa.core.parts.mind.output = [oa.display]


class OpenAssistant(core.agent.Agent):
    """Example Implementation: Agent."""
    
    def __init__(self, home=None, modules=[]):
        logging.info("Initializing Open Assistant")
        core.agent.Agent.__init__(self, home=home, modules=modules)

        # Establish OA core.
        core.oa.core = self
        core.oa.core_directory = self.home



def runapp():
    """Initialize and run the OpenAssistant Agent"""

    try:
        a = OpenAssistant(
            home=os.path.dirname(__file__),
            modules=[
                'voice',
            ]
          )
        a.run()

        # from modules.abilities.core import get, put
        while not a.finished.is_set():
            cmd = input("OA> ")
            if cmd in ['q', 'quit']:
                a.finished.set()
                continue
            a.parts.voice.__call__(cmd)


        a.finished.wait()


    except KeyboardInterrupt:
        logging.info("Ctrl-C Pressed")

        logging.info("Signaling Shutdown")
        a.finished.set()
        
        logging.info('Waiting on threads')
        [thr.join() for thr in a.thread_pool]
        logging.info('Threads closed')


if __name__ == '__main__':
    fn = 'oa.log'
    logging.basicConfig(level=logging.DEBUG, filename=fn, format="[%(asctime)s] %(levelname)-8s %(threadName)-10s [%(filename)s:%(funcName)s:%(lineno)d]    %(message)s")
    logging.info("Start Open Assistant")

    runapp()
    quit(0)
