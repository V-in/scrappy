from os import path, makedirs, mkdir


def ensure_dir(dir_path):
    """Creates a directory if it does not exist
    """
    if not path.exists(dir_path):
        mkdir(dir_path)
