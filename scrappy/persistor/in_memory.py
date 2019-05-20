from scrappy.persistor.document import Document
from scrappy.persistor.persistor import Persistor
from scrappy.core.error_dump import error_dump
from scrappy.core.utils import ensure_dir
from scrappy.core.commands import Die
from os import path, makedirs
from threading import Thread
from queue import Queue
from uuid import uuid4
import pydebug

debug = pydebug.debug("persistor")


class InMemoryPersistor():
    """Saves data in memory

    Data is accessed at self.data [List]
    """

    def __init__(self):
        self.data = []

    def save_one(self, document):
        """Saves one Document
        """
        if (not isinstance(document, Document)):
            raise ValueError("Document must be an instance of Document")

        self.data.append(document)
