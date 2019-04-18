from scrappy.driver.worker import Worker
from scrappy.driver.pool import create, dispose
from itertools import cycle
from threading import Thread
from queue import Queue
import pydebug

debug = pydebug.debug("scheduler")


class Scheduler(Thread):

    def __init__(self, pool_size, driver_path, headless=True):
        Thread.__init__(self)
        self.pool = list()
        self.retry = Queue()
        self.jobs = Queue()
        self.pool_size = pool_size
        self.headless = headless
        self.pool = create(pool_size, driver_path, headless)

    def __enter__(self):
        return self

    def __exit__(self, *arg):
        dispose(self.pool)

    def schedule_job(self, job):
        """Enqueues a job
        """

        self.jobs.put(job)

    def consume_queue(self):
        raise NotImplementedError

    def dispose(self):
        """Disposes of all workers
        """
        dispose(self.pool)

    def run(self):
        self.consume_queue(self.jobs)
        while(self.retry._qsize() > 0):
            self.consume_queue(self.retry)
