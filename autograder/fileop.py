"""
Fileops (File Operations) are simple operations on files
intended to be easy to implement on any platform.

See:
 - https://github.com/edulinq/autograder-server/blob/main/docs/types.md#file-operation-fileop
 - https://github.com/edulinq/autograder-server/blob/main/internal/util/fileop.go
"""

import fnmatch
import glob
import os
import re
import typing

import edq.util.dirent

import autograder.util.path

FILE_OP_LONG_COPY: str = "copy"
FILE_OP_SHORT_COPY: str = "cp"

FILE_OP_LONG_MOVE: str = "move"
FILE_OP_SHORT_MOVE: str = "mv"

FILE_OP_LONG_MKDIR: str = "make-dir"
FILE_OP_SHORT_MKDIR: str = "mkdir"

FILE_OP_LONG_REMOVE: str = "remove"
FILE_OP_SHORT_REMOVE: str = "rm"

fileop_normal_name: typing.Dict[str, str] = {
    FILE_OP_SHORT_COPY: FILE_OP_LONG_COPY,
    FILE_OP_LONG_COPY: FILE_OP_LONG_COPY,

    FILE_OP_SHORT_MOVE: FILE_OP_LONG_MOVE,
    FILE_OP_LONG_MOVE: FILE_OP_LONG_MOVE,

    FILE_OP_SHORT_MKDIR: FILE_OP_LONG_MKDIR,
    FILE_OP_LONG_MKDIR: FILE_OP_LONG_MKDIR,

    FILE_OP_SHORT_REMOVE: FILE_OP_LONG_REMOVE,
    FILE_OP_LONG_REMOVE: FILE_OP_LONG_REMOVE,
}
""" Map operations to their long/canonical name. """

fileop_num_args: typing.Dict[str, int] = {
    FILE_OP_LONG_COPY: 2,
    FILE_OP_LONG_MOVE: 2,
    FILE_OP_LONG_MKDIR: 1,
    FILE_OP_LONG_REMOVE: 1,
}
""" The number of operations for each file operation. """

FileOp = typing.List[str]
""" Alias file operations until they are formalized in a more robust class. """

def validate(operation: typing.Union[None, typing.List[str], FileOp]) -> FileOp:
    """
    Validate a fileop.
    Raise on failure or invalid operation.
    Otherwise, return the same list that has been validated, cleaned, and typed.
    """

    if (operation is None):
        raise ValueError("File operation is None.")

    if (len(operation) == 0):
        raise ValueError("File operation is empty.")

    command = fileop_normal_name.get(operation[0].lower(), None)
    if (command is None):
        raise ValueError(f"Unknown file operation: '{operation[0]}'.")

    operation[0] = command

    num_args = (len(operation) - 1)
    expected_num_args = fileop_num_args[command]
    if (expected_num_args != num_args):
        raise ValueError(f"Incorrect number of arguments for '{command}' file operation."
            + f" Expected {expected_num_args}, found {num_args}.")

    # Check all path arguments.
    for i in range(1, len(operation)):
        path = operation[i]

        if ('\\' in path):
            raise ValueError(f"Argument at index {i} ('{operation[i]}')"
                + " contains a backslash ('\\') or is not a POSIX path.")

        path = os.path.normpath(path)

        if (os.path.isabs(path)):
            raise ValueError(f"Argument at index {i} ('{operation[i]}') is an absolute path."
                + " Only relative paths are allowed.")

        if (not autograder.util.path.is_local(path)):
            raise ValueError(f"Argument at index {i} ('{operation[i]}')"
                + " points outside of the its base directory."
                + " File operation paths can not reference parent directories.")

        if (path == "."):
            raise ValueError(f"Argument at index {i} ('{operation[i]}')"
                + " cannot point just to the current directory."
                + " File operation paths must point to a"
                + " dirent inside the current directory tree.")

        try:
            glob_pattern = fnmatch.translate(path)
            re.compile(glob_pattern)
        except Exception as error:
            raise ValueError(f"Argument at index {i} ('{operation[i]}') is an invalid glob pattern: {error}.")  # pylint: disable=raise-missing-from

        operation[i] = path

    return typing.cast(FileOp, operation)

def execute(operation: FileOp, base_dir: str) -> None:
    """ Execute operation operation in the given directory. """

    validate(operation)

    command = operation[0]

    if (command == FILE_OP_LONG_COPY):
        source_path = _resolve_path(operation[1], base_dir)
        dest_path = _resolve_path(operation[2], base_dir)

        _handle_glob_file_operation(
            source_path, dest_path, edq.util.dirent.copy,
        )
    elif (command == FILE_OP_LONG_MOVE):
        source_path = _resolve_path(operation[1], base_dir)
        dest_path = _resolve_path(operation[2], base_dir)

        _handle_glob_file_operation(source_path, dest_path, edq.util.dirent.move)
    elif (command == FILE_OP_LONG_MKDIR):
        path = _resolve_path(operation[1], base_dir)

        edq.util.dirent.mkdir(path)
    elif (command == FILE_OP_LONG_REMOVE):
        path_glob = _resolve_path(operation[1], base_dir)

        _handle_glob_remove(path_glob)
    else:
        raise ValueError(f"Unknown file operation: '{command}'.")

def validate_file_operations(operations: typing.List[typing.Union[None, typing.List[str]]]) -> typing.List[FileOp]:
    """ Validate multiple file operations. """

    return [validate(operation) for operation in operations]

def exec_file_operations(operations: typing.List[FileOp], base_dir: str) -> None:
    """ Execute multiple file operations in the given directory. """

    for operation in operations:
        execute(operation, base_dir)

def _resolve_path(path: str, base_dir: str) -> str:
    """ Resolve a path (which may be relative) in the given base directory. """

    if (os.path.isabs(path)):
        return os.path.normpath(path)

    return os.path.normpath(os.path.join(base_dir, path))

def _handle_glob_file_operation(source_path_glob: str, dest_path: str, operation: typing.Callable, **kwargs: typing.Any) -> None:
    """ Resolve a path that may contain globs, and perform the given file system operation. """

    source_paths = _prep_for_globs(source_path_glob, dest_path)

    for source_path in source_paths:
        if (source_path == dest_path):
            continue

        resolved_dest_path = dest_path

        # Check for an operation into a dir.
        if (os.path.isdir(dest_path)):
            resolved_dest_path = os.path.join(dest_path, os.path.basename(source_path))

        operation(source_path, resolved_dest_path, **kwargs)

def _handle_glob_remove(path_glob: str) -> None:
    """ Resolve a path that may contain a glob and remove the resolved paths. """

    paths = glob.glob(path_glob)

    for path in paths:
        edq.util.dirent.remove(path)

def _prep_for_globs(source_path_glob: str, dest_path: str) -> typing.List[str]:
    """
    Prepare for executing an operation in the presence of globs.

    Do the following actions:
    1) Resolve the source paths for globs.
    2) Ensure that the source path matches at least one existing path.
    3) If multiple source paths match, ensure that the dest exists and is a dir.
    4) Return the resolved source paths.
    """

    source_paths = glob.glob(source_path_glob)

    if (len(source_paths) == 0):
        raise FileNotFoundError(f"No such file or directory: '{source_path_glob}'.")

    if (len(source_paths) > 1):
        os.makedirs(dest_path, exist_ok = True)

    return source_paths
