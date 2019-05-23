from scrappy.persistor.file_system import make_valid_path
from scrappy.util.tmpFile import tmpFile
from scrappy.persistor.document import Document
from tempfile import gettempdir
from scrappy.persistor.file_system import FileSystemPersistor
from os import path, remove


def test_persistor_saves_document():
    doc = Document(1, "Hello world")
    persistor = FileSystemPersistor(gettempdir())
    persistor.start()
    persistor.save_one(doc)
    persistor.shutdown()
    persistor.join()
    assert path.exists(tmpFile("1"))
    assert open(tmpFile("1"), "r").read() == "Hello world"
    remove(tmpFile("1"))


def test_make_valid_path_valid_arguments():
    document = Document("unique-id", "Hello world")
    base_path = "/home/vinicius"

    assert make_valid_path(base_path, document) == "/home/vinicius/unique-id"


def test_make_valid_path_base_path():
    document = Document("unique-id", "Hello world")
    base_path = "/1/2/3/4/5"

    assert make_valid_path(
        base_path, document) == tmpFile("scrappy/orphans/unique-id")


def test_make_valid_path_duplicated_id():
    document = Document("dummy", "Hello world")
    base_path = tmpFile("scrappy")

    if not path.exists(tmpFile("scrappy/dummy")):
        open(tmpFile("scrappy/dummy"), 'a').close()

    assert make_valid_path(
        base_path, document)[:33] == tmpFile("scrappy/duplicates/document-")


def test_make_valid_path_valid_arguments():
    document = Document("unique-id", "Hello world")
    base_path = "/home/vinicius"

    assert make_valid_path(base_path, document) == "/home/vinicius/unique-id"


def test_make_valid_path_base_path():
    document = Document("unique-id", "Hello world")
    base_path = "/1/2/3/4/5"

    assert make_valid_path(
        base_path, document) == tmpFile("scrappy/orphans/unique-id")


def test_make_valid_path_duplicated_id():
    document = Document("dummy", "Hello world")
    base_path = tmpFile("scrappy")

    if not path.exists(tmpFile("scrappy/dummy")):
        open(tmpFile("scrappy/dummy"), 'a').close()

    assert make_valid_path(
        base_path, document)[:33] == tmpFile("scrappy/duplicates/document-")
