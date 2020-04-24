""" Common library functions """
import sys
import pathlib


def get_absolute_path(file_path):
    """ Return the absolute path of a potentially relative file path"""
    path = pathlib.Path(file_path)
    path = path.expanduser()
    path = path.absolute()
    return str(path)


def assert_file_exists(file_path):
    """ Gracefully exist if a file does not exist """
    path = pathlib.Path(get_absolute_path(file_path))
    if not path.exists():
        err = f'ERROR: Expected file/directory {file_path} not found\n'
        sys.stderr.write(err)
        sys.exit(1)


def volume_opt(src, dest):
    """ Return a volume optional argument for docker run commands """
    assert_file_exists(src)
    absolute_path = get_absolute_path(src)
    return f'-v {absolute_path}:{dest} '
