from scrappy.core.error_dump import error_dump, format_error
from os import remove
from uuid import uuid4
from pytest import raises


def test_format_error():
    error, error_id = format_error("An error occured")
    assert type(error) == str


def test_error_dump():
    _id = uuid4()
    path = "/tmp/{}".format(_id)
    with raises(FileNotFoundError):
        open(path, 'r')
    error_dump(1, "fuck", path)
    try:
        open(path, 'r')
    except:
        assert False
    finally:
        remove(path)
