# Open Assistant 0.21
# 2018 General Public License V3

"""Open Assistant reference implementation."""

import logging
import os
import threading

from oa import core
from oa.core.agent import Agent


class OpenAssistant(Agent):
    """Example Implementation: Agent."""
    
    def __init__(self, home=None, modules=[]):
        logging.info("Initializing Open Assistant")
        Agent.__init__(self, home=home, modules=modules)

        # Establish OA core.
        core.oa.core = self
        core.oa.core_directory = self.home


def LoadAssistant(config):
    """Example Configuration."""

    modules = [
        'sound',
        'voice',
        'speech_recognition',
        'ear',
        'mind',
    ]

    a = OpenAssistant(
        home=os.path.dirname(__file__),
        modules=modules,
    )

    a.run()

    # Link the output of ear to speech_recognition
    a.parts['ear'].output += [a.parts['speech_recognition']]

    # Link the output of speech_recognition to mind
    a.parts['speech_recognition'].output += [a.parts['mind']]

    # oa.core.parts.keyboard.output = [oa.mind, oa.display]
    # oa.core.parts.mind.output = [oa.display]
        
    return a


# from modules.abilities.core import get, put
def _command_loop(a):
    from oa.modules.abilities.core import put

    while not a.finished.is_set():
        cmd = input("OA> ")
        if cmd in ['q', 'quit']:
            a.finished.set()
            continue
        elif cmd in ['h', 'help', '?']:
            print("Help Stuff")
        elif cmd.find(' ') > -1:
            p, m = cmd.split(' ', 1)
            logging.debug("{} <- {}".format(p, m))
            put(p, m)


def start(**kwargs):
    """Initialize and run the OpenAssistant Agent"""

    try:
        a = LoadAssistant(config=kwargs.get('config'))
        
        while not a.finished.is_set():
            try:
                _command_loop(a)
            except Exception as ex:
                logging.error("Command Loop: {}".format(ex))

        a.finished.wait()


    except KeyboardInterrupt:
        logging.info("Ctrl-C Pressed")

        logging.info("Signaling Shutdown")
        a.finished.set()
        
        logging.info('Waiting on threads')
        [thr.join() for thr in a.thread_pool]
        logging.info('Threads closed')


if __name__ == '__main__':
    import sys
    
    from oa.util.args import _parser
    args = _parser(sys.argv[1:])
    
    log_template = "[%(asctime)s] %(threadName)s [%(filename)s:%(funcName)s:%(lineno)d] %(levelname)s: %(message)s"
    logging.basicConfig(level=logging.INFO if not args.debug else logging.DEBUG, filename=args.log_file, format=log_template)
    logging.info("Start Open Assistant")

    start(
        home=args.home_dir,
        config=args.config_file,
    )
    quit(0)
