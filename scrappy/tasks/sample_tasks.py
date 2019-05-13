from scrappy.tasks.task import Task
from scrappy.persistor.dummy_persistor import DummyPersistor
from scrappy.persistor.document import Document


class SimpleTask(Task):
    def __init__(self, persistor):
        Task.__init__(self, persistor)

    def run(self, driver, persistor):
        driver.get("http://google.com")
        driver.find_element_by_xpath(
            "//input[@title='Pesquisar']").send_keys("Hello world")

        doc = Document(1, "The quick brown fox jumps over the lazy dog")
        persistor.save_one(persistor, document=doc)


HelloGoogle = SimpleTask(DummyPersistor)
