import logging

def command_loop(oa):
    while not oa.finished.is_set():
        cmd = input("OA> ")
        if cmd in ['q', 'quit']:
            oa.finished.set()
            continue
        elif cmd in ['h', 'help', '?']:
            print("Help Stuff")
        elif cmd.find(' ') > -1:
            p, m = cmd.split(' ', 1)
            logging.debug("{} <- {}".format(p, m))
            oa.put(p, m)
        else:
            print("Unrecognized command: {}".format(cmd))
