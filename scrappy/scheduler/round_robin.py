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
    def __init__(self, pool_size, driver_path, headless=True):
        super().__init__(pool_size, driver_path, headless)

    def consume_queue(self, q):
        """Job queue consumption implementation

        Distributes jobs in a Robin Round fashion

        Arguments:
            q {[type]} -- [description]
        """
        gen = cycle(range(self.pool_size))
        for _ in range(q.qsize()):
            self.pool[next(gen)].schedule_task(self.jobs.get())

        for worker in self.pool:
            worker.start()


def test_robin_round_scheduler():
    s = RoundRobin(3, "/home/vinicius/Downloads/chromedriver", False)

    def job(driver):
        driver.get("http://google.com")
        driver.find_element_by_xpath(
            "//input[@title='Pesquisar']").send_keys("Hello world")

    s.schedule_job(job)
    s.schedule_job(job)
    s.schedule_job(job)
    s.schedule_job(job)
    s.schedule_job(job)
    s.schedule_job(job)
    s.schedule_job(job)

    s.start()
    s.dispose()
