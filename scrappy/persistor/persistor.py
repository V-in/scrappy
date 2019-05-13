from scrappy.persistor.document import Document
from scrappy.core.error_dump import error_dump
from scrappy.core.utils import ensure_dir
from scrappy.core.commands import Die
from os import path, makedirs
from threading import Thread
from queue import Queue
from uuid import uuid4
import pydebug

debug = pydebug.debug("persistor")


class Persistor(Thread):
    """Simple persistors that saves to files on disk
    """

    def __init__(self, base_path):
        Thread.__init__(self)
        self._id = uuid4()
        self.queue = Queue()
        self.base_path = base_path

    def save_one_sync(self, document):
        """Saves one document

        Arguments:
            document {Document} -- Document injected into this function

        Raises:
            NotImplementedError: All persistors should implement a save_one_sync function
        """
        raise NotImplementedError

    def die(self):
        """Graceful shutdown triggered by a Die task. Default behavior is to just pass
        """
        pass

    def save_one(self, document):
        self.queue.put_nowait(document)

    def shutdown(self):
        self.queue.put(Die)

    def __enter__(self):
        return self

    def __exit__(self, *arg):
        self.queue.put(Die)

    def run(self):
        debug("Persistor {} has started".format(self._id))

        while True:
            document = self.queue.get()
            if document is Die:
                self.die()
                break
            try:
                self.save_one_sync(document)
            except Exception as error:
                error_dump(self._id, error)
            self.queue.task_done()

        debug("Persistor {} has stopped".format(self._id))


def make_valid_path(base_path, document):
    """Creates a valid file path from a directory and a document

    Uses globally unique IDs on name clash and tmp folder on invalid dir.

    Arguments:
        base_path {str} -- Directory where document should be saved
        document {Document} -- Document to be saved
    """
    file_path = path.join(base_path, document.id)

    if not path.exists(base_path):
        msg = """Directory at {} does not exist,
              falling back to /tmp/scrappy/orphans""".replace("\n", "")

        msg = ' '.join(msg.replace('\n', " ").split())

        debug(msg.format(base_path))

        new_file_path = "/tmp/scrappy/orphans"
        if not path.exists(new_file_path):
            makedirs(new_file_path)

        return make_valid_path(new_file_path, document)

    if path.exists(file_path):
        msg = """File at {0} already exists,
               falling back to uui and saving to {0}/duplicates"""

        msg = ' '.join(msg.replace('\n', " ").split())

        debug(msg.format(file_path))

        unique_id = "document-{}".format(str(uuid4()))
        new_base_path = path.join(base_path, "duplicates")
        new_document = Document(unique_id, document.data)
        ensure_dir(new_base_path)

        return make_valid_path(new_base_path, new_document)

    return file_path
