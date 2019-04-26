from scrappy.driver.worker import Worker
from scrappy.core.commands import Die


def test_worker_with_context():
    def task(driver):
        driver.get("http://google.com")

    with Worker("/home/vinicius/Downloads/chromedriver") as worker:

        assert not worker.is_open
        worker.start()
        assert worker.is_open

        worker.schedule_task(task)
        worker.schedule_task(task)
        worker.schedule_task(task)
        worker.schedule_task(Die)

        assert worker.is_open

        worker.join()


def test_worker_without_jobs():
    def task(driver):
        driver.get("http://google.com")

    with Worker("/home/vinicius/Downloads/chromedriver") as worker:

        assert not worker.is_open
        worker.start()
        assert worker.is_open


def test_worker_without_context():
    def task(driver):
        driver.get("http://google.com")

    worker = Worker("/home/vinicius/Downloads/chromedriver")
    assert not worker.is_open
    worker.start()
    assert worker.is_open
    worker.schedule_task(Die)
    worker.join()
