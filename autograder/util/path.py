import os

THIS_DIR = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))

# Reserved filenames (mainly on Windows).
# See: https://github.com/python/cpython/blob/3.13/Lib/ntpath.py
RESERVED_NAMES = frozenset(
    {'CON', 'PRN', 'AUX', 'NUL', 'CONIN$', 'CONOUT$'} |  # noqa: W504
    {f'COM{c}' for c in '123456789\xb9\xb2\xb3'} |  # noqa: W504
    {f'LPT{c}' for c in '123456789\xb9\xb2\xb3'}
)

# Try to see of a file is "local" using only lexical analysis.
# See: https://pkg.go.dev/path/filepath#IsLocal
# This is not robust and should not be used for any systems where security can be an issue.
def is_local(path):
    path = os.path.normpath(path.strip())

    if (path == ''):
        return False

    if (os.path.isabs(path)):
        return False

    if (_is_reserved(path)):
        return False

    # To see if the path does not break out of the current directory,
    # join it to the current directory and see if the current
    # directory is still a base path.

    current_path = THIS_DIR

    # Note that the normalization should remove any (or several)
    # parent references ('..') at this point.
    test_path = os.path.normpath(os.path.join(THIS_DIR, path))

    common_prefix = os.path.commonprefix([current_path, test_path])
    if (common_prefix != current_path):
        return False

    return True

# A very weak version of ntpath.isreserved(path) (which was added in version 3.13).
# https://docs.python.org/3/library/os.path.html#os.path.isreserved
def _is_reserved(path):
    return os.path.basename(path).upper() in RESERVED_NAMES
