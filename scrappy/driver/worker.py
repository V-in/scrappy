from contextlib import contextmanager
from scrappy.core import error_dump
from queue import Empty, Queue
from selenium import webdriver
from threading import Thread, Event
from uuid import uuid4
import time
import pydebug

debug = pydebug.debug("driver:worker")
# This task tells a worker to stop and cleanup
Die = object()


class Worker(Thread):
    """Scrapper worker
    A Worker continuously consumes and executes tasks from its internal queue
    until a Die task arrives.
    """

    def __init__(self, driver_path, headless=True):
        Thread.__init__(self)
        self.driver_path = driver_path
        self.driver = None
        self.headless = headless
        self._id = uuid4()
        self.queue = Queue()
        self.is_open = False

    def __del__(self):
        self.dispose()

    def __enter__(self):
        return self

    def __exit__(self, *a):
        self.schedule_task(Die)

    def _open(self):
        """Instanciates a driver window and sets internal .is_open flag to True
        """

        self.is_open = True
        options = webdriver.ChromeOptions()
        if(self.headless):
            options.add_argument('headless')
        self.driver = webdriver.Chrome(
            self.driver_path, options=options)
        debug("Worker {} has started".format(self._id))

    def dispose(self):
        """Disposes of active driver windowsd
        """
        try:
            self.driver.quit()
        except:
            pass

    def schedule_task(self, task):
        """Enqueues a task to be executed later

        Arguments:
            task Job -- task to be enqueued
        """
        self.queue.put(task)

    def run(self):
        """Worker loop
        """

        self._open()

        while True:
            task = self.queue.get()
            if task is Die:
                break
            try:
                task(self.driver)
            except Exception as error:
                error_dump.error_dump(self._id, error)
            self.queue.task_done()

        self.dispose()
        debug("Worker {} has stopped".format(self._id))


def test_worker_with_context():
    def task(driver):
        driver.get("http://google.com")
        driver.find_element_by_css_selector("coco")

    with Worker("/home/vinicius/Downloads/chromedriver") as worker:

        assert not worker.is_open
        worker.start()
        assert worker.is_open

        worker.schedule_task(task)
        worker.schedule_task(task)
        worker.schedule_task(task)

        assert worker.is_open


def test_worker_without_jobs():
    def task(driver):
        driver.get("http://google.com")
        driver.find_element_by_css_selector("coco")

    with Worker("/home/vinicius/Downloads/chromedriver") as worker:

        assert not worker.is_open
        worker.start()
        assert worker.is_open


def test_worker_without_context():
    def task(driver):
        driver.get("http://google.com")
        driver.find_element_by_css_selector("coco")

    worker = Worker("/home/vinicius/Downloads/chromedriver")
    assert not worker.is_open
    worker.start()
    assert worker.is_open
    worker.schedule_task(Die)
    worker.join()
