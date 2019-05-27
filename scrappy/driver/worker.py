from contextlib import contextmanager
from scrappy.core import crash_dump
from queue import Empty, Queue
from selenium import webdriver
from threading import Thread, Event
from uuid import uuid4
from scrappy.core.commands import Die
import time
import pydebug

debug = pydebug.debug("driver:worker")


class Worker(Thread):
    """Scrapper worker
    A Worker continuously consumes and executes tasks from its internal queue
    until a Die task arrives.
    """

    def __init__(self, headless=True):
        Thread.__init__(self)
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
            "chromedriver", options=options)
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
            task task -- task to be enqueued
        """
        self.queue.put(task)

    def run(self):
        """Worker loop
        """

        self._open()

        while True:
            task = self.queue.get()
            if task is Die:
                self.queue.task_done()
                break
            try:
                task._run(self.driver)
            except Exception as error:
                debug(error)
                crash_dump.crash_dump(self._id, error)
            self.queue.task_done()

        self.dispose()
        debug("Worker {} has stopped".format(self._id))
