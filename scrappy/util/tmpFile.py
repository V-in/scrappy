from tempfile import gettempdir
from os import path


def tmpFile(file_path):
    return path.join(gettempdir(), file_path)
