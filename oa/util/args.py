from argparse import ArgumentParser, Namespace

def _parser(args):
    parser = ArgumentParser()

    parser.add_argument("-A", "--agents", type=str,
            dest="agents_dir", action='store',
            help="Path to agents repository directory")

    parser.add_argument("-a", "--agent", type=str,
            dest="agent", action="store",
            help="Agent to load")

    parser.add_argument("-c", "--config",
            dest='config_file', action='store', default=None,
            help="Path to config file")

    parser.add_argument("-d", "--debug",
            action='store_true', dest="debug", default=False,
            help="Enable debug-level logging")

    parser.add_argument("-H", "--home", type=str,
            dest="home_dir", action='store',
            help="Path to directory to use as home")

    parser.add_argument("-l", "--log",
            dest='log_file', action='store', default=None,
            help="Path to log file")

    return parser.parse_args(args)
