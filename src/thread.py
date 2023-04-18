from threading import Thread
from typing import Callable


# Custom implementation of the Thread object that forwards the return value of the function back to the main thread
# attr ret - value returned from the target function
class ThreadWithReturn(Thread):
    def __init__(self, target: Callable = None, args: tuple = (), kwargs: dict = None):
        Thread.__init__(self, None, target, None, args, kwargs)
        self.ret = None

    # Runs the target function and stores its return value
    def run(self):
        if self._target is not None:
            self.ret = self._target(*self._args, **self._kwargs)

    # Joins back to the main thread, forwarding the return value from the target function
    def join(self, *args):
        Thread.join(self, *args)
        return self.ret
