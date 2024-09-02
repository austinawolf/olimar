import threading
from typing import Callable, Collection
import queue
from threading import Condition
import time


class Waitable:
    def __init__(self):
        self._when_ready: Collection[Callable] = []
        self._when_timeout: Collection[Callable] = []
        self._wait_event = threading.Event()
        self._args = queue.Queue()

    def _timer_expired(self):
        if not self._wait_event.is_set():
            self._wait_event.set()

    def _timeout(self):
        for callback in self._when_timeout:
            callback(self)

    def wait(self, timeout: int):
        """
        Called from waiting thread to wait on arguments/timeout

        :param timeout:
        :return:
        """
        self._timer = threading.Timer(timeout, self._wait_event.set)
        self._timer.start()
        self._wait_event.wait()
        self._timer.cancel()

        try:
            results = self._args.get(block=False)
        except queue.Empty:
            self._timeout()
            results = None
        
        if not results:
            raise TimeoutError

        return results[0] if len(results) == 1 else results

    def notify(self, *results):
        self._args.put(results)
        self._wait_event.set()

        for callback in self._when_ready:
            callback(*results)

    def on_ready(self, callback: Callable):
        if not callback:
            raise ValueError
        self._when_ready += [callback]

    def on_timeout(self, callback: Callable):
        if not callback:
            raise ValueError
        self._when_timeout += [callback]


