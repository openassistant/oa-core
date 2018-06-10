# console.py - System text display.

def _in():
    while oa.alive:
        # Print messages from the queue.
        print(get())
        yield ''
