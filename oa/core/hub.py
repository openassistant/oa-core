# Need something to act as 'core'

import logging
import os
import threading

from . import util

class Hub:
    def __init__(self, config=None):
        self.config = config

        self.ready = threading.Event()
        self.finished = threading.Event()
        
        self.thread_pool = []
        self.parts = {}


    def run(self):
        self._load_modules()
        self._start_modules()
        self.ready.set()
        self.finished.clear()


    def put(self, part, value):
        """ Put a message on the wire. """
        if part in self.parts:
            self.parts[part].wire_in.put(value)


    def _load_modules(self):
        """ Setup all parts. """

        for module_repo in self.config.get('module_path', []):
            logging.info("Loading Modules <- {}".format(module_repo))

            for module_name in os.listdir(module_repo):
                if module_name in self.config.get('modules'):
                    try:
                        m = util.load_module(os.path.join(module_repo, module_name))
                        m.name = module_name
                        self.parts[module_name] = m
                    except Exception as ex:
                        logging.error("Error loading {}: {}".format(module_name, ex))


    def _start_modules(self):
        # Setup input threads.
        b = threading.Barrier(len(self.parts)+1)

        for module_name in self.parts:
            m = self.parts[module_name]
            thr = threading.Thread(target=thread_loop, name=module_name, args=(self, m, b))
            self.thread_pool.append(thr)

        # Start all threads.
        [thr.start() for thr in self.thread_pool]
        b.wait()


def thread_loop(hub, part, b):
    """ Setup part inputs to the message wire. """
    # if not isinstance(part.output, list):
        # raise Exception('No output list defined: ' + part.name)

    logging.debug('Starting')
    # ready = threading.Event()

    
    if hasattr(part, 'init'):
        part.init()

    b.wait()
    
    hub.ready.wait()

    while hub.ready.is_set():
        try:
            for msg in part._in():
                for listener in part.output:
                    logging.debug('{} -> {}'.format(part.name, listener.name))
                    listener.wire_in.put(msg)
        except Exception as ex:
            logging.error("Error processing queue: {}".format(ex))


    logging.debug('Stopped')