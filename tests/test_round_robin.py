from scrappy.scheduler.round_robin import RoundRobin
from scrappy.persistor.dummy_persistor import DummyPersistor
from scrappy.tasks.task import Task
from scrappy.persistor.document import Document


class HelloWorld(Task):
    def __init__(self, persistor):
        Task.__init__(self, persistor)

    def run(self, driver, persistor):
        driver.get("http://google.com")
        driver.find_element_by_xpath(
            "//input[@title='Pesquisar']").send_keys("Hello world")

        doc = Document(1, "The quick brown fox jumps over the lazy dog")
        persistor.save_one(doc)


def test_robin_round_scheduler():
    s = RoundRobin(2, "/home/vinicius/Downloads/chromedriver", headless=True)
    p = DummyPersistor()
    task = HelloWorld(p)

    s.schedule_task(task)
    s.schedule_task(task)
    s.schedule_task(task)

    s.start()
    s.dispose()
