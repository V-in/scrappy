from scrappy.driver.worker import Worker, Die
import time


def create(size, driver_path="/home/vinicius/Downloads/chromedriver",
           headless=False):
    return list([Worker(driver_path, headless) for _ in range(size)])


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


def test_pool_lifecycle():
    # Birth
    pool = create(5)
    for worker in pool:
        assert not worker.is_open

    # Life
    start_all(pool)
    for worker in pool:
        assert worker.is_open

    # Death
    dispose(pool)
