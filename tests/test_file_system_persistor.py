from scrappy.persistor.file_system import make_valid_path
from scrappy.persistor.document import Document
from scrappy.persistor.file_system import FileSystemPersistor
from os import path, remove


def test_persistor_saves_document():
    doc = Document(1, "Hello world")
    persistor = FileSystemPersistor("/tmp")
    persistor.start()
    persistor.save_one(doc)
    persistor.shutdown()
    persistor.join()
    assert path.exists("/tmp/1")
    assert open("/tmp/1", "r").read() == "Hello world"
    remove("/tmp/1")


def test_make_valid_path_valid_arguments():
    document = Document("unique-id", "Hello world")
    base_path = "/home/vinicius"

    assert make_valid_path(base_path, document) == "/home/vinicius/unique-id"


def test_make_valid_path_base_path():
    document = Document("unique-id", "Hello world")
    base_path = "/1/2/3/4/5"

    assert make_valid_path(
        base_path, document) == "/tmp/scrappy/orphans/unique-id"


def test_make_valid_path_duplicated_id():
    document = Document("dummy", "Hello world")
    base_path = "/tmp/scrappy"

    if not path.exists("/tmp/scrappy/dummy"):
        open("/tmp/scrappy/dummy", 'a').close()

    assert make_valid_path(
        base_path, document)[:33] == "/tmp/scrappy/duplicates/document-"


def test_make_valid_path_valid_arguments():
    document = Document("unique-id", "Hello world")
    base_path = "/home/vinicius"

    assert make_valid_path(base_path, document) == "/home/vinicius/unique-id"


def test_make_valid_path_base_path():
    document = Document("unique-id", "Hello world")
    base_path = "/1/2/3/4/5"

    assert make_valid_path(
        base_path, document) == "/tmp/scrappy/orphans/unique-id"


def test_make_valid_path_duplicated_id():
    document = Document("dummy", "Hello world")
    base_path = "/tmp/scrappy"

    if not path.exists("/tmp/scrappy/dummy"):
        open("/tmp/scrappy/dummy", 'a').close()

    assert make_valid_path(
        base_path, document)[:33] == "/tmp/scrappy/duplicates/document-"
