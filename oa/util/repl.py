import logging

def command_loop(hub:object) -> None:
    """Responsible for maintaining command line interface for OA. Interfaces
    textual commands with the hub. 

    Args:
        hub (object): The current instance of hub passed over from oa.__main__.py

    Returns:
        None

    Raises:
        None
    """

    while not hub.finished.is_set():
        cmd = input("OA> ")
        if cmd in ['q', 'quit']:
            hub.finished.set()
        elif cmd in ['h', 'help', '?']:
            print("Help Stuff")
        elif cmd.find(' ') > -1:
            p, m = cmd.split(' ', 1)
            logging.debug("{} <- {}".format(p, m))
            hub.put(p, m)
        else:
            print("Unrecognized command: {}".format(cmd))
