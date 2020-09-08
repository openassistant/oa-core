import logging
import re
_logger = logging.getLogger(__name__)

regex_mind_command = re.compile(r'^(\S+):')

def command_loop(hub:object) -> None:
    """Responsible for maintaining command line interface for OA. Interfaces
    textual commands with the hub. Commands are directed to the OA bus addressed
    to the minds by default. Commands can be directed at modules specifically
    using the syntax `<module>: <command>`

    Args:
        hub (object): The current instance of hub passed over from oa.__main__.py

    Returns:
        None

    Raises:
        None
    """

    while not hub.finished.is_set():
        cmd = input("OA> ")
        _logger.debug("Raw CLI Command: {}".format(cmd))
        if cmd in ['q', 'quit']:
            hub.finished.set()
            break
        elif cmd in ['h', 'help', '?']:
            print("Help Stuff")
            continue
        elif regex_mind_command.match(cmd):
            # Dircted at a specific module. Extract the module and command.
            # Remove initial whitespace if space was given after <module>:
            p, m = cmd.split(':', 1)
            m = m.lstrip(' ')
        else:
            # Default to send the command to the minds.
            p, m = "mind", cmd

        _logger.debug("{} <- {}".format(p, m))
        hub.put(p, m)
