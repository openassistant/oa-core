from argparse import ArgumentParser, Namespace

def _parser(args):
    parser = ArgumentParser()

    # parser.add_argument("-c", "--continuous",
    #         action="store_true", dest="continuous", default=False,
    #         help="Start interface with 'continuous' listen enabled")
    #
    # parser.add_argument("-p", "--pass-words",
    #         action="store_true", dest="pass_words", default=False,
    #         help="Pass the recognized words as arguments to the shell command")
    #
    # parser.add_argument("-H", "--history", type=int,
    #         action="store", dest="history",
    #         help="Number of commands to store in history file")
    #
    # parser.add_argument("-m", "--microphone", type=int,
    #         action="store", dest="microphone", default=None,
    #         help="Audio input card to use (if other than system default)")
    #
    # parser.add_argument("--valid-sentence-command", type=str,
    #         dest="valid_sentence_command", action='store', default=None,
    #         help="Command to run when a valid sentence is detected")
    #
    # parser.add_argument("--invalid-sentence-command", type=str,
    #         dest="invalid_sentence_command", action='store', default=None,
    #         help="Command to run when an invalid sentence is detected")

    parser.add_argument("-M", "--mind", type=str,
            dest="mind_dir", action='store',
            help="Path to mind to use for assistant")

    parser.add_argument("-d", "--debug",
            action='store_true', dest="debug", default=False,
            help="Enable debug-level logging")

    # parser.add_argument("-u", "--update",
    #         action='store_true', dest="update", default=False,
    #         help="Update language files online")

    return parser.parse_args(args)
