def _in():
    while oa.alive:
        #just print everything from Queue
        print(get())
        yield ''
