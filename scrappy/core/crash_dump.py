from time import gmtime, strftime
from scrappy.util.tmpFile import tmpFile
from uuid import uuid4
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


def crash_dump(caller_id, error, path=tmpFile("scrappy.dump")):
    """
        Securely logs an error

        Keyword arguments:
            caller_id  -- id of the caller
            error -- error to be logged
            path  -- path to log file (default tmpFile("scrappy.dump"))
    """

    formatedError, error_id = format_error(error)

    with open(path, "a") as file:
        msg = "{id} has crashed, logging with error_id {error_id}:\
               {error_summary}...".format(id=caller_id, error_id=error_id,
                                          error_summary=formatedError[:20])
        debug(msg)
        file.write(str(formatedError))
