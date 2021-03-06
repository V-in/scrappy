from scrappy.core.crash_dump import crash_dump, format_error
from os import remove
from scrappy.util.tmpFile import tmpFile
from uuid import uuid4
from pytest import raises


def test_format_error():
    error, error_id = format_error("An error occured")
    assert type(error) == str


def test_crash_dump():
    _id = uuid4()
    path = tmpFile(str(_id))
    with raises(FileNotFoundError):
        open(path, 'r')
    crash_dump(1, "fuck", path)
    try:
        open(path, 'r')
    except:
        assert False
    finally:
        remove(path)
