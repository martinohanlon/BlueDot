import atexit
from threading import Thread, Event

_THREADS = set()

def _shutdown():
    while _THREADS:
        for t in _THREADS.copy():
            t.stop()

atexit.register(_shutdown)

class WrapThread(Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs={}):
        super(WrapThread, self).__init__(group, target, name, args, kwargs)
        self.stopping = Event()
        self.daemon = True

    def start(self):
        self.stopping.clear()
        _THREADS.add(self)
        super(WrapThread, self).start()

    def stop(self):
        self.stopping.set()
        self.join()

    def join(self):
        super(WrapThread, self).join()
        _THREADS.discard(self)

