# Open Assistant 0.21
# 2018 General Public License V3
# By Alex Kamosko, Andrew Vavrek, Jenya Chernotalova

# oa.py - Launch Open Assistant.

import os, time
import threading

import core

from core import oa, Core, Stub

import abilities.core
from abilities.core import info, read_file, queue


# Setup connections between parts.
oa.ear.input = [oa.stt]
oa.stt.input = [oa.mind]
oa.keyboard.input = [oa.mind, oa.display]


class OpenAssistant:
    """ Main OA loading class. """
    def __init__(_):
        info("- Loading Open Assistant...")

        # Establish OA core.
        oa.core = _
        oa.core_directory = os.path.dirname(__file__)

        # Setup Stubs for functions of `core.py`.
        _.stub_funcs = Stub.prepare_stubs(core)

        # Activate OA.
        _.active = threading.Event()
        _.active.set()
        oa.alive = lambda : _.active.is_set()

        # Setup parts and threads.
        _.parts = {}
        _.thread_pool = []
        _.load_parts()

    def loop(_):
        """ Remain active until exit. """
        try:
            while oa.alive:
                time.sleep(.1)

        except KeyboardInterrupt:
            info('- Attempting to close threads...')
            _.active.clear()
            [thr.join() for thr in _.thread_pool]
            info('- Threads closed.')

    def load_parts(_):
        """ Setup all parts. """
        for part_name in os.listdir('parts'):
            info('- Loading part: ' + part_name)
            name = part_name[:-3]
            part_core = read_file('parts/' + part_name)
            stream = dict(list(core.__dict__.items())[:])

            # Connect parts to the message wire.
            stream['wire_in'] = queue.Queue()
            exec(part_core, stream)
            part = Core(**stream)
            oa[name].__dict__.update(part.__dict__)
            part = oa[name]
            setattr(part, 'name', name)
            part.__dict__.setdefault('input', [])

            if stream.get('_in', None) is not None:

                # Additional check for yield.
                if 'yield' not in part_core.lower():
                    info('- WARNING: Please check part `%s` for yield in _in()' %(name))

                # Setup input threads.
                thr = threading.Thread(target = _in, name = name, args = (part,))
                _.parts[name] = part
                _.thread_pool.append(thr)

        # Start all threads.
        [thr.start() for thr in _.thread_pool]


def _in(part):
    """ Setup part inputs to the message wire. """
    if not isinstance(part.input, list):
        raise Exception('Wrong part: ' + part.name)

    stream = part._in
    info('- Started.')

    for message in stream():
        for listener in part.input:
            info('- Sending to part:', listener.name)
            listener.wire_in.put(message)
    info('- Closed.')


""" Boot Open Assistant. """
def runapp():
    OpenAssistant().loop()

if __name__ == '__main__':
    runapp()
