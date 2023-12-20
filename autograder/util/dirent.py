import atexit
import os
import shutil
import tempfile
import uuid

def get_temp_path(prefix = '', suffix = '', rm = True):
    """
    Get a path to a valid (but not currently existing) temp dirent.
    If rm is True, then the dirent will be attempted to be deleted on exit
    (no error will occur if the path is not there).
    """

    path = None
    while ((path is None) or os.path.exists(path)):
        path = os.path.join(tempfile.gettempdir(), prefix + str(uuid.uuid4()) + suffix)

    if (rm):
        atexit.register(remove, path)

    return path

def remove(path):
    if (not os.path.exists(path)):
        return

    if (os.path.isfile(path) or os.path.islink(path)):
        os.remove(path)
    elif (os.path.isdir(path)):
        shutil.rmtree(path)
    else:
        raise ValueError("Unknown type of dirent: '%s'." % (path))

def copy(source, dest):
    """
    Copy a file or directory into dest.
    If source is a file, then dest can be a file or dir.
    If source is a dir, then dest must be a non-existent dir.
    """

    if (os.path.isfile(source)):
        shutil.copy2(source, dest)
    else:
        shutil.copytree(source, dest)

def copy_contents(source, dest):
    """
    Copy a file or the contents of a directory (excluding the top-level directory) into dest.
    For a file: `cp source dest/`
    For a dir: `cp -r source/* dest/`
    """

    source = os.path.abspath(source)

    if (os.path.isfile(source)):
        shutil.copy2(source, dest)
        return

    for dirent in os.listdir(source):
        source_path = os.path.join(source, dirent)
        dest_path = os.path.join(dest, dirent)

        if (os.path.isfile(source_path)):
            shutil.copy2(source_path, dest_path)
        else:
            shutil.copytree(source_path, dest_path)
