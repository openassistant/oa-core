from argparse import ArgumentParser, Namespace

def _parser(args):
    parser = ArgumentParser()



    parser.add_argument("-d", "--debug",
            action='store_true', dest="debug", default=False,
            help="Enable debug-level logging")

    return parser.parse_args(args)
