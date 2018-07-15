# Open Assistant 0.21
# 2018 General Public License V3

"""Open Assistant reference implementation."""

import logging
import os
import threading

from oa import core
from oa.core import agent


class OpenAssistant(core.agent.Agent):
    """Example Implementation: Agent."""
    
    def __init__(self, home=None, modules=[]):
        logging.info("Initializing Open Assistant")
        core.agent.Agent.__init__(self, home=home, modules=modules)

        # Establish OA core.
        core.oa.core = self
        core.oa.core_directory = self.home



def start():
    """Initialize and run the OpenAssistant Agent"""

    try:
        a = OpenAssistant(
            home=os.path.dirname(__file__),
            modules=[
                'sound',
                'voice',
                'speech_recognition',
                'ear',
                'mind',
            ]
          )
        a.run()
        
        # Setup connections between parts.
        a.parts['ear'].output += [a.parts.speech_recognition]
        a.parts.speech_recognition.output += [a.parts.mind]
        # oa.core.parts.keyboard.output = [oa.mind, oa.display]
        # oa.core.parts.mind.output = [oa.display]

        
        # from modules.abilities.core import get, put
        def command_loop():
            from oa.modules.abilities.core import put

            while not a.finished.is_set():
                cmd = input("OA> ")
                if cmd in ['q', 'quit']:
                    a.finished.set()
                    continue
                if cmd.find(' ') > -1:
                    p, m = cmd[:cmd.find(' ')], cmd[cmd.find(' ')+1:]
                    logging.debug("{} <- {}".format(p, m))
                    put(p, m)

        
        while not a.finished.is_set():
            try:
                command_loop()
            except Exception as ex:
                logging.error("Command Loop: {}".format(ex))
                print("Command Loop: {}".format(ex))


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
    
    logging.basicConfig(level=logging.DEBUG, filename=args.log_file, format="[%(asctime)s] %(levelname)-8s %(threadName)-10s [%(filename)s:%(funcName)s:%(lineno)d]    %(message)s")
    logging.info("Start Open Assistant")

    start()
    quit(0)
