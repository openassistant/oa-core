# Open Assistant 0.21
# 2018 General Public License V3

"""Open Assistant reference implementation."""

import logging
import os
import threading

from oa import core
from oa.core.agent import Agent
from oa.core.hub import Hub


class OpenAssistant(Agent):
    """Example Implementation: Agent."""
    
    def __init__(self, module_path=None, modules=[]):
        logging.info("Initializing Open Assistant")
        Agent.__init__(self, home=module_path, modules=modules)


def _command_loop(a):

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
            a.put(p, m)
        else:
            print("Unrecognized command: {}".format(cmd))


def start(**kwargs):
    """Initialize and run the OpenAssistant Agent"""

    try:

        config = {
            'module_path': [
                os.path.join(os.path.dirname(__file__), 'modules'),
            ],
            'modules': [
                'voice',
                'sound',
                'ear',
                'speech_recognition',
                'mind',
            ],
        }

        import json
        config_path = kwargs.get('config')
        if config_path is not None:
            config.update(json.load(open(config_path)))

        h = Hub(config=config)
        
        # XXX: temporary compatability hack
        core.oa.core = h
        core.oa.core_directory = os.path.dirname(__file__)

        h.run()

        _map = [
            ('ear', 'speech_recognition'),
            ('speech_recognition', 'mind'),
        ]
        for _in, _out in _map:
            h.parts[_in].output += [h.parts[_out]]

        
        while not h.finished.is_set():
            try:
                _command_loop(h)
            except Exception as ex:
                logging.error("Command Loop: {}".format(ex))

        h.ready.wait()


    except KeyboardInterrupt:
        logging.info("Ctrl-C Pressed")

        logging.info("Signaling Shutdown")
        h.finished.set()
        
        logging.info('Waiting on threads')
        [thr.join() for thr in h.thread_pool]
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
