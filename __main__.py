# OpenAssistant 0.04
# 2016 General Public License V3
# By Andrew Vavrek, Clayton G. Hobbs, Jezra

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


if __name__ == '__main__':

    from gi.repository import GObject
    import sys

    # Parse command-line options,
    #  use `Config` to load mind configuration
    #  command-line overrides config file
    from .core.util.args import _parser as arg_parser
    args = arg_parser(sys.argv[1:])
    if args.debug:
        logging.root.setLevel(logging.DEBUG)
    logger.debug("Arguments: {args}".format(args=args))


    # A configured Assistant
    if args.agents_dir is not None:
        agents_path = os.path.realpath(args.agents_dir)
        logger.info("Agents Path: %s" % agents_path)
        sys.path.insert(0, agents_path)

    if args.agent is not None:
        import importlib
        A = importlib.import_module(args.agent)
        logger.info("Loading {}".format(A))
        a = A.__call__()


    #
    # Questionable dependencies
    #

    # Initialize Gobject Threads
    GObject.threads_init()

    # Create Main Loop
    main_loop = GObject.MainLoop()

    # Handle Signal Interrupts
    import signal
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    #
    # End Questionable dependencies
    #


    # Start Main Loop
    try:
        main_loop.run()

    except Exception as e:
        print(e)
        main_loop.quit()
        sys.exit()
