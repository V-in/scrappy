from scrappy.driver.worker import Worker
import time
from scrappy.driver.pool import create
from itertools import cycle
from threading import Thread
from scrappy.scheduler.scheduler import Scheduler
from queue import Queue
import pydebug

debug = pydebug.debug("scheduler")


class RoundRobin(Scheduler):
    def __init__(self, pool_size, headless=True):
        super().__init__(pool_size, headless)

    def consume_queue(self, q):
        """task queue consumption implementation

        Distributes tasks in a Robin Round fashion

        Arguments:
            q {[type]} -- [description]
        """
        gen = cycle(range(self.pool_size))
        for _ in range(q.qsize()):
            self.pool[next(gen)].schedule_task(self.tasks.get())

        for worker in self.pool:
            worker.start()
