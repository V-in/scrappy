from scrappy.scheduler.round_robin import RoundRobin
from scrappy.persistor.dummy_persistor import DummyPersistor
from scrappy.tasks.task import Task
from scrappy.persistor.document import Document
from pathlib import Path
import pytest

_current_path = Path().absolute()


class HelloWorld(Task):
    def __init__(self, persistor):
        Task.__init__(self, persistor)

    def run(self, driver, persistor):
        driver.get("http://google.com")
        driver.find_element_by_xpath(
            "//input[@title='Pesquisar']").send_keys("Hello world")

        doc = Document(1, "The quick brown fox jumps over the lazy dog")
        persistor.save_one(doc)


@pytest.mark.timeout(30)
def test_round_robin_scheduler():
    s = RoundRobin(2, headless=True)
    p = DummyPersistor()
    task = HelloWorld(p)

    s.schedule_task(task)
    s.schedule_task(task)
    s.schedule_task(task)

    s.start()
    s.dispose()
    assert s.tasks.qsize() == 0


def test_round_robin_context_manager():
    p = DummyPersistor()
    task = HelloWorld(p)
    with RoundRobin(1, headless=True) as scheduler:
        scheduler.schedule_task(task)
        scheduler.schedule_task(task)
        scheduler.schedule_task(task)
        scheduler.schedule_task(task)
        scheduler.schedule_task(task)
