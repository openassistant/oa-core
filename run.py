# OpenAssistant 0.04
# 2016 General Public License V3
# By Andrew Vavrek, Clayton G. Hobbs, Jezra

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


import os
import signal
import subprocess




def recognizer_finished(a, recognizer, text):
    logger.debug("Agent: {}, Recognier: {}, Text: {}".format(a, recognizer, text))
    t = text.lower()

    # cmd = a.db.get_action(t)

    # # Is There A Matching Command?
    # if cmd is not None:
    #     # Run The 'valid_sentence_command' If It's Set
    #     os.system('clear')
    #     if a.config.options['valid_sentence_command']:
    #         subprocess.call([a.config.options['valid_sentence_command'], text])
    #     # Should We Be Passing Words?
    #     #os.system('clear')
    #     if a.config.options['pass_words']:
    #         cmd += " " + t
    #     print("\x1b[32m< ? >\x1b[0m {0}".format(t))
    #     run_command(a, cmd)

    # Is There A Matching Command?
    if t in a.config.commands:
        # Run The 'valid_sentence_command' If It's Set
        os.system('clear')
        print("Open Assistant: \x1b[32mListening\x1b[0m")
        if a.config.options['valid_sentence_command']:
            subprocess.call([a.config.options['valid_sentence_command'], text], shell=True)
        cmd = a.config.commands[t]
        # Should We Be Passing Words?
        os.system('clear')
        print("Open Assistant: \x1b[32mListening\x1b[0m")
        if a.config.options['pass_words']:
            cmd += " " + t
        print("\x1b[32m< ! >\x1b[0m {0}".format(t))
        run_command(a, cmd)
        log_history(a, text)

    else:
        # Run The Invalid_sentence_command If It's Set
        logger.debug("Unrecognized command: {}".format(t))
        if a.config.options['invalid_sentence_command']:
            subprocess.call([a.config.options['invalid_sentence_command'], text])
        print("\x1b[31m< ? >\x1b[0m {0}".format(t))


def log_history(a, text):
    if a.config.options['history']:
        a.history.append(text)
        if len(a.history) > a.config.options['history']:
            # Pop Off First Item
            a.history.pop(0)

        # Open And Truncate History File
        with open(a.config.history_file, 'w') as hfile:
            for line in a.history:
                hfile.write(line + '\n')

def run_command(a, cmd):
    """PRINT COMMAND AND RUN"""
    print("\x1b[32m< ! >\x1b[0m", cmd)
    recognizer.pause()
    subprocess.call(cmd, shell=True)
    recognizer.listen()


def process_command(self, command):
    print(command)
    if command == "listen":
        self.recognizer.listen()
    elif command == "stop":
        self.recognizer.pause()
    elif command == "continuous_listen":
        self.continuous_listen = True
        self.recognizer.listen()
    elif command == "continuous_stop":
        self.continuous_listen = False
        self.recognizer.pause()
    elif command == "quit":
        self.quit()


if __name__ == '__main__':

    from gi.repository import GObject
    import sys

    # Parse command-line options,
    #  use `Config` to load mind configuration
    #  command-line overrides config file
    from core.util.args import _parser as arg_parser
    args = arg_parser(sys.argv[1:])
    if args.debug:
        logging.root.setLevel(logging.DEBUG)
    logger.debug("Arguments: {args}".format(args=args))


    # A configured Assistant
    from core import Assistant
    a = Assistant(path=args.mind_dir)

    logger.info("Begin Secondary Configuration")
    conf = a.config

    #
    # Pre-Configuration
    #

    # Configure Language
    logger.debug("Configuring Module: Language")

    # Language Paths
    conf.strings_file = os.path.join(conf.cache_dir, "sentences.corpus")
    conf.dic_file = os.path.join(conf.cache_dir, 'dic')
    # conf.lm_file = os.path.join(conf.cache_dir, 'lm')
    conf.lang_file = os.path.join(conf.cache_dir, 'lm')
    #XXX: hard coding this for now, sorry :(
    conf.hmm_path = "/usr/local/share/pocketsphinx/model/en-us/en-us"
    conf.fsg_file = None #os.path.join(conf.cache_dir, 'fsg')


    # Generate Language Files
    if args.update:
        from modules.language import LanguageUpdater

        # create_strings_file(conf.strings_file, db.get_prompts()) # conf.commands)
        # create_sphinx_files(conf.strings_file, conf.lm_file, conf.dic_file)

        l = LanguageUpdater(conf)
        l.update_language()





    # Configure Recognizer
    logger.debug("Configuring Module: Speech Recognition")
    from modules.speech_recognition.gst import Recognizer

    # recognizer = Recognizer(args.microphone, dic_file=conf.dic_file, lm_file=conf.lm_file)
    recognizer = Recognizer(conf)

    #
    # End Pre-Configuration
    #


    #
    # Post-Configuration
    #

    recognizer.connect('finished', lambda rec, txt, agent=a: recognizer_finished(agent, rec, txt))

    #
    # End Post-Configuration
    #

    logger.info("End Secondary Configuration")
    logger.debug("Agent Configuration: {}".format(a.config))



    #
    # Questionable dependencies
    #
    # Initialize Gobject Threads
    GObject.threads_init()

    # Create Main Loop
    main_loop = GObject.MainLoop()

    # Handle Signal Interrupts
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    #
    # End Questionable dependencies
    #

    # Run Assistant
    #  maybe use threading module?
    #  could supplant GObject features
    #a.run()
    recognizer.listen()


    # Start Main Loop
    try:
        main_loop.run()

    except Exception as e:
        print(e)
        main_loop.quit()
        sys.exit()
