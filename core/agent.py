# Open Assistant

import logging
import os
import threading

from .util import Core, load_module


class Agent:

    def __init__(self, home=None, **opts):
        logging.debug(self)
        self.finished = threading.Event()

        self.home = home if home is not None else os.getcwd()
        self.modules = opts.get('modules', [])
        self.parts =  Core()
        self.thread_pool = []
        self.mind = None


    def run(self):
        self._load_modules()
        self._start_modules()


    def _load_modules(self):
        """ Setup all parts. """

        modules_path = os.path.join(self.home, 'modules')
        logging.info("Loading Modules <- {}".format(os.path.realpath(modules_path)))

        # for module_name in os.listdir(modules_path):
        for module_name in self.modules:
            try:
                m = load_module(os.path.join(modules_path, module_name))
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
        

from modules.abilities.core import get

def thread_loop(agent, part, b):
    """ Setup part inputs to the message wire. """
    # if not isinstance(part.output, list):
        # raise Exception('No output list defined: ' + part.name)

    logging.debug('Starting')
    ready = threading.Event()

    
    if hasattr(part, 'init'):
       part.init()

    b.wait()
    
    agent.finished.wait()

    while not agent.finished.is_set():
        msg = get()
            # for message in part._in():
            # for listener in part.output:
            # logging.error("Sending {} -> {}: {}".format(part.name, listener.name, ex))
     #       part.__call__(msg)
    #    except Exception as ex:
    #        logging.error


    # part("test")
    # muted = False
    # try:
    #     
    #             
    #                 try:
    #                     logging.debug('{} -> {}'.format(part.name, listener.name))
    #                     # listener.wire_in.put(message)
    #                     listener(message)
    #                 except Exception as ex:
    #                     
    # except Exception as ex:
    #     logging.error(ex)

    logging.debug('Stopped')