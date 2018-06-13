# Open Assistant 0.21
# 2018 General Public License V3
# By Alex Kamosko, Andrew Vavrek, Jenya Chernotalova

# oa.py - Launch Open Assistant.

import os, time
import importlib
import threading

import core
from core import oa, Core, Stub

import abilities.core
from abilities.core import info, read_file, queue


# Setup connections between parts.
oa.ear.output = [oa.speech_recognition]
oa.speech_recognition.output = [oa.mind]
oa.keyboard.output = [oa.mind, oa.display]


class OpenAssistant:
    """ Main OA loading class. """
    def __init__(self):
        info("- Loading Open Assistant...")

        # Establish OA core.
        oa.core = self
        oa.core_directory = os.path.dirname(__file__)

        # Setup Stubs for functions of `core.py`.
        self.stub_funcs = Stub.prepare_stubs(core)

        # Activate OA.
        self.active = threading.Event()
        self.active.set()
        oa.alive = lambda : self.active.is_set()

        # Setup parts and threads.
        self.parts = {}
        self.thread_pool = []
        self.load_parts()

    def loop(self):
        """ Remain active until exit. """
        try:
            while oa.alive:
                time.sleep(.1)

        except KeyboardInterrupt:
            info('- Attempting to close threads...')
            self.active.clear()
            [thr.join() for thr in self.thread_pool]
            info('- Threads closed.')

    def load_parts(self):
        """ Setup all parts. """

        pkg = os.path.split(oa.core_directory)[-1]

        for module_name in os.listdir('modules'):
            try:

                # A module is a folder with an __init__.py file
                if not all([
                    os.path.isdir(os.path.join('modules', module_name)),
                    os.path.exists(os.path.join('modules', module_name, '__init__.py')),
                ]): continue

                info('Loading Module: {} <- {}'.format(module_name, os.path.join('modules', module_name, '__init__.py')))

                # Import part as module
                M = importlib.import_module('modules.{}'.format(module_name), package=pkg)
                info("Module: {}".format(repr(M)))

                # If the module provides an input queue, link it
                if getattr(M, '_in', None) is not None:

                    m = oa[module_name]
                    m.__dict__.update(M.__dict__)
                    
                    setattr(m, 'name', module_name)
                    m.__dict__.setdefault('wire_in', queue.Queue())
                    m.__dict__.setdefault('output', [])

                    # Setup input threads.
                    thr = threading.Thread(target = _in, name = module_name, args = (m,))
                    self.parts[module_name] = m
                    self.thread_pool.append(thr)
                    
            except Exception as ex:
                info(ex)

        # Start all threads.
        [thr.start() for thr in self.thread_pool]


def _in(part):
    """ Setup part inputs to the message wire. """
    if not isinstance(part.output, list):
        raise Exception('Wrong part: ' + part.name)

    info('- Started.')

    for message in part._in():
        try:
            for listener in part.output:
                info('- Sending to part:', listener.name)
                listener.wire_in.put(message)
        except Exception as ex:
            info(ex)
    info('- Closed.')


""" Boot Open Assistant. """
def runapp():
    OpenAssistant().loop()

if __name__ == '__main__':
    runapp()
