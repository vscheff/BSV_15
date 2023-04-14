from threading import Thread

# Local Dependencies
from src.puzzle import Puzzle


class ThreadWithReturn(Thread):
    def __init__(self, target=None, args=(), kwargs=None):
        Thread.__init__(self, None, target, None, args, kwargs)
        self.ret = None

    def run(self):
        if self._target is not None:
            self.ret = self._target(*self._args, **self._kwargs)

    def join(self, *args):
        Thread.join(self, *args)
        return self.ret
