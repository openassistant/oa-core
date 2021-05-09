# Open Assistant 0.21
# 2018 General Public License V3

"""Open Assistant reference implementation."""

import logging
_logger = logging.getLogger(__name__)

import os

import oa

import oa.legacy

def start(hub, **kwargs):
    """Initialize and run the OpenAssistant Agent"""
    from oa.util.repl import command_loop

    hub.run()

    while not hub.finished.is_set():
        try:
            command_loop(hub)
        except Exception as ex:
            _logger.error("Command Loop: {}".format(ex))

    hub.ready.wait()


if __name__ == '__main__':
    import sys

    from argparse import ArgumentParser, Namespace

    # Parse arguments
    parser = ArgumentParser()

    parser.add_argument("-c", "--config",
                        dest='config_file', action='store', default=None,
                        help="Path to config file")

    parser.add_argument("-d", "--debug",
                        action='store_true', dest="debug", default=False,
                        help="Enable debug-level logging")

    parser.add_argument("-l", "--log",
                        dest='log_file', action='store', default=None,
                        help="Path to log file")

    args = parser.parse_args(sys.argv[1:])

    log_template = "[%(asctime)s] %(levelname)s %(threadName)s %(name)s: %(message)s"
    logging.basicConfig(level=logging.INFO if not args.debug else logging.DEBUG, filename=args.log_file, format=log_template)

    _logger.info("Start Open Assistant")

    config = {
        'module_path': [
            os.path.join(os.path.dirname(__file__), 'modules'),
        ],
        'modules': [
        ],
    }

    import json
    config_path = args.config_file 

    if config_path is None:
        config_path = os.path.join(os.path.dirname(__file__), 'oa.conf')
    
    if os.path.exists(config_path):
        config.update(json.load(open(config_path)))

    hub = oa.Hub(config=config)

    # XXX: temporary compatability hack
    oa.legacy.hub = hub
    oa.legacy.core_directory = os.path.dirname(__file__)

    try:
        start(hub)

    except KeyboardInterrupt:
        _logger.info("Ctrl-C Pressed")

        _logger.info("Signaling Shutdown")
        hub.finished.set()

        _logger.info('Waiting on threads')
        [thr.join() for thr in hub.thread_pool]
        _logger.info('Threads closed')
