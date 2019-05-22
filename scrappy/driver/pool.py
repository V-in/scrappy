from scrappy.driver.worker import Worker
from scrappy.core.commands import Die
import time


def create(size, headless=True):
    return list([Worker(headless) for _ in range(size)])


def start_all(pool):
    """Starts all workers in a pool

    Arguments:
        pool Pool -- Pool of workers
    """
    for worker in pool:
        worker.start()


def dispose(pool):
    """Disposes of a pool of workers

    Arguments:
        pool Pool -- Pool of workers
    """
    for worker in pool:
        worker.schedule_task(Die)
    for worker in pool:
        worker.queue.join()
