# Need something to act as 'core'

import logging
_logger = logging.getLogger(__name__)

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
        self.finished.clear()
        self._load_modules()
        self._start_modules()
        self.ready.set()


    def put(self, part, value):
        """ Put a message on the wire. """
        _logger.debug(f"PUT Called... {part} <- {value}")
        if part in self.parts:
            _logger.debug("Part specified... putting on the wire.")
            self.parts[part].wire_in.put(value)


    def _load_modules(self):
        """ Setup all parts. """

        for module_repo in self.config.get('module_path', []):
            _logger.info("Loading Modules <- {}".format(module_repo))

            for module_name in os.listdir(module_repo):
                if module_name in self.config.get('modules'):
                    try:
                        m = util.load_module(os.path.join(module_repo, module_name))
                        m.name = module_name
                        self.parts[module_name] = m
                    except Exception as ex:
                        _logger.error("Error loading {}: {}".format(module_name, ex))


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

    _logger.debug('Starting')
    # ready = threading.Event()

    
    if hasattr(part, 'init'):
        part.init()

    b.wait()
    
    hub.ready.wait()

    while not hub.finished.is_set():
        try:
            for msg in part._in(hub):
                for listener in part.output:
                    _logger.debug('{} -> {}'.format(part.name, listener.name))
                    listener.wire_in.put(msg)
        except Exception as ex:
            _logger.error("Error processing queue: {}".format(ex))


    _logger.debug('Stopped')