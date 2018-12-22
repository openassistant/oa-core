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
    
    def __init__(self, module_path=None, modules=[]):
        logging.info("Initializing Open Assistant")
        Agent.__init__(self, home=module_path, modules=modules)


def LoadAssistant(config):
    """Example Configuration."""

    _module_path = [
        os.path.dirname(__file__),
    ][0]

    modules = [
        'sound',
        'voice',
        'speech_recognition',
        'ear',
        'mind',
    ]

    _map = [
        ('ear', 'speech_recognition'),
        ('speech_recognition', 'mind'),
    ]

    a = OpenAssistant(
        module_path=_module_path,
        modules=modules,
    )

    # Establish OA core.
    core.oa.core = a
    core.oa.core_directory = a.home

    a.run()

    for _in, _out in _map:
        a.parts[_in].output += [a.parts[_out]]
        
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
    
    log_template = "[%(asctime)s] %(levelname)s %(threadName)s [%(filename)s:%(funcName)s:%(lineno)d]: %(message)s"
    logging.basicConfig(level=logging.INFO if not args.debug else logging.DEBUG, filename=args.log_file, format=log_template)
    logging.info("Start Open Assistant")

    start(
        config=args.config_file,
    )
    quit(0)
