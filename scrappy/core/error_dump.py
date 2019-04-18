from time import gmtime, strftime
from uuid import uuid4
from os import remove
from pytest import raises
import pydebug

debug = pydebug.debug("core:logger")


def format_error(error):
    """
        format_error(error) => (string, integer)

        Formats an error message, returning formated output and generated id

        Keyword arguments:

    """

    time = strftime("%Y-%m-%d-%H:%M:%S", gmtime())
    uuid = uuid4()
    error = '---\nid: {id}\ntime: {time}\nmessage: "{msg}"\n---'.format(
        id=uuid, time=time, msg=str(error))

    return (error, uuid)


def error_dump(caller_id, error, path="/tmp/scrappy.dump"):
    """
        Securely logs an error

        Keyword arguments:
            caller_id  -- id of the caller
            error -- error to be logged
            path  -- path to log file (default "/tmp/scrappy.dump")
    """

    formatedError, error_id = format_error(error)

    with open(path, "a") as file:
        msg = "{id} has crashed, logging with error_id {error_id}:\
               {error_summary}...".format(id=caller_id, error_id=error_id,
                                          error_summary=formatedError[:20])
        debug(msg)
        file.write(str(formatedError))


def test_format_error():
    error, error_id = format_error("eita p** deu errado")
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
