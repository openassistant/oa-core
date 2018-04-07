from argparse import ArgumentParser, Namespace

def _parser(args):
    parser = ArgumentParser()

    parser.add_argument("-A", "--agents", type=str,
            dest="agents_dir", action='store',
            help="Path to agents repository directory")

    parser.add_argument("-a", "--agent", type=str,
            dest="agent", action="store",
            help="Agent to load")


    parser.add_argument("-d", "--debug",
            action='store_true', dest="debug", default=False,
            help="Enable debug-level logging")

    return parser.parse_args(args)
