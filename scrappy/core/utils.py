from os import path, makedirs, mkdir


def ensure_dir(dir_path):
    """Creates a directory if it does not exist
    """
    if not path.exists(dir_path):
        mkdir(dir_path)


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]
