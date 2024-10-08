import os
import shutil

import autograder.util.dirent

def archive_dir(path, **kwargs):
    """
    Create an archive of the given dir in a temp directory,
    and return the path to the created archive.
    All kwargs will be passed to get_temp_path().
    """

    if (not os.path.isdir(path)):
        raise ValueError("Target archive path does not exist or is not a dir: '%s'." % (path))

    temp_dir = autograder.util.dirent.get_temp_path(**kwargs)
    os.makedirs(temp_dir, exist_ok = True)

    base_name = os.path.basename(path)
    base_path = os.path.join(temp_dir, base_name)

    return shutil.make_archive(base_path, 'zip', path)
