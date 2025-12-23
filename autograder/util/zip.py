import os
import shutil
import typing

import edq.util.dirent

def archive_dir(path: str, **kwargs: typing.Any) -> str:
    """
    Create an archive of the given dir in a temp directory,
    and return the path to the created archive.
    All kwargs will be passed to get_temp_path().
    """

    if (not os.path.isdir(path)):
        raise ValueError(f"Target archive path does not exist or is not a dir: '{path}'.")

    temp_dir = edq.util.dirent.get_temp_dir(**kwargs)

    base_name = os.path.basename(path)
    base_path = os.path.join(temp_dir, base_name)

    return shutil.make_archive(base_path, 'zip', path)
