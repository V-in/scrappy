from scrappy.driver.worker import Worker
from scrappy.driver.pool import create, dispose
from scrappy.tasks.task import Task
from itertools import cycle
from threading import Thread
from queue import Queue
import pydebug

debug = pydebug.debug("scheduler")


class Scheduler(Thread):

    def __init__(self, pool_size, headless=True):
        Thread.__init__(self)
        self.pool = list()
        self.retry = Queue()
        self.tasks = Queue()
        self.pool_size = pool_size
        self.headless = headless
        self.pool = create(pool_size, headless)

    def __enter__(self):
        return self

    def __exit__(self, *arg):
        self.start()
        dispose(self.pool)

    def schedule_task(self, task):
        """Enqueues a task
        """
        if(not issubclass(task.__class__, Task)):
            raise ValueError("task must be an instance of Task")
        self.tasks.put(task)

    def consume_queue(self):
        raise NotImplementedError

    def dispose(self):
        """Disposes of all workers
        """
        dispose(self.pool)

    def run(self):
        self.consume_queue(self.tasks)
        while(self.retry._qsize() > 0):
            self.consume_queue(self.retry)
