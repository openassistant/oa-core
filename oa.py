# Open Assistant 0.21
# 2018 General Public License V3

"""Open Assistant reference implementation."""

import logging
import os
import threading

from core import oa, queue, Core, load_module
from core.agent import Agent


class OpenAssistant(Agent):
    """Example Agent class."""
    
    def __init__(self):
        logging.info("Initializing Open Assistant")
        Agent.__init__(self, home=os.path.dirname(__file__))

        # Establish OA core.
        oa.core = self
        oa.core_directory = self.home

        # Setup parts and threads.
        self.parts = Core()
        self.minds = Core()
        self.mind = None

        self.finished = threading.Event()
        self.thread_pool = []

    def run(self):
        self._load_modules()
        
        # Setup connections between parts.
        # XXX: can't ensure load order yet
        self._start_modules()
        self.parts.ear.output += [self.parts.speech_recognition]
        self.parts.speech_recognition.output += [self.parts.mind]
        # oa.core.parts.keyboard.output = [oa.mind, oa.display]
        # oa.core.parts.mind.output = [oa.display]

        self.finished.wait()

    def _load_modules(self):
        """ Setup all parts. """

        modules_path = os.path.join(self.home, 'modules')
        logging.info("Loading Modules <- {}".format(modules_path))

        for module_name in os.listdir(modules_path):
            try:
                m = load_module(os.path.join(modules_path, module_name))
                m.name = module_name
                self.parts[module_name] = m
            except Exception as ex:
                logging.error("Error loading {}: {}".format(module_name, ex))
        

    def _start_modules(self):
        # Setup input threads.
        for module_name in oa.core.parts:
            m = oa.core.parts[module_name]
            if getattr(m, '_in', None) is not None:
                thr = threading.Thread(target=thread_loop, name=module_name, args=(m,))
                self.thread_pool.append(thr)

        # Start all threads.
        [thr.start() for thr in self.thread_pool]


def thread_loop(part):
    """ Setup part inputs to the message wire. """
    if not isinstance(part.output, list):
        raise Exception('No output list defined: ' + part.name)

    if hasattr(part, 'init'):
        part.init()

    logging.debug('Started')

    muted = False
    try:
        for message in part._in():
            if not muted:
                for listener in part.output:
                    try:
                        logging.debug('{} -> {}'.format(part.name, listener.name))
                        listener.wire_in.put(message)
                    except Exception as ex:
                        logging.error("Sending {} -> {}: {}".format(part.name, listener.name, ex))
    except Exception as ex:
        logging.error(ex)

    logging.debug('Stopped')


def runapp():
    try:
        a = OpenAssistant()
        a.run()

    except KeyboardInterrupt:
        logging.info("Ctrl-C Pressed")

        logging.info("Signaling Shutdown")
        oa.core.finished.set()
        
        logging.info('Waiting on threads')
        [thr.join() for thr in oa.core.thread_pool]
        logging.info('Threads closed')


if __name__ == '__main__':
    # filename='oa.log'
    logging.basicConfig(level=logging.DEBUG, format="[%(asctime)s] %(levelname)-8s %(threadName)-24s [%(filename)s:%(funcName)s:%(lineno)d]\t  %(message)s")
    logging.info("Start Open Assistant")

    runapp()
    quit(0)
