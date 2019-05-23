from scrappy.persistor.document import Document
from scrappy.util.tmpFile import tmpFile
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


class FileSystemPersistor(Persistor):
    """Simple persistors that saves to files on disk
    """

    def save_one_sync(self, document):
        """Saves one Document to disk
        """
        if (not isinstance(document, Document)):
            raise ValueError("Document must be an instance of Document")

        file_path = make_valid_path(self.base_path, document)

        with open(file_path, "x") as file:
            file.write(document.data)


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

        new_file_path = tmpFile("scrappy/orphans")
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
