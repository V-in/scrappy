from scrappy.driver.worker import Worker
from scrappy.core.commands import Die
from scrappy.tasks.sample_tasks import HelloGoogle


def test_worker_with_context():
    with Worker("/home/vinicius/Downloads/chromedriver") as worker:

        assert not worker.is_open
        worker.start()
        assert worker.is_open

        worker.schedule_task(HelloGoogle)
        worker.schedule_task(HelloGoogle)
        worker.schedule_task(HelloGoogle)
        worker.schedule_task(Die)

        assert worker.is_open

        worker.join()


def test_worker_without_tasks():
    with Worker("/home/vinicius/Downloads/chromedriver") as worker:

        assert not worker.is_open
        worker.start()
        assert worker.is_open


def test_worker_without_context():
    worker = Worker("/home/vinicius/Downloads/chromedriver")
    assert not worker.is_open
    worker.start()
    assert worker.is_open
    worker.schedule_task(Die)
    worker.join()
