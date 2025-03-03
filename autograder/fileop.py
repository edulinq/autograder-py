"""
File Operations (file ops) are simple operations on files
intended to be easy to implement on any platform.

See:
 - https://github.com/edulinq/autograder-server/blob/main/docs/types.md#file-operation-fileop
 - https://github.com/edulinq/autograder-server/blob/main/internal/util/fileop.go
"""

import fnmatch
import glob
import os
import re

import autograder.util.dir
import autograder.util.dirent
import autograder.util.path

FILE_OP_LONG_COPY = "copy"
FILE_OP_SHORT_COPY = "cp"

FILE_OP_LONG_MOVE = "move"
FILE_OP_SHORT_MOVE = "mv"

FILE_OP_LONG_MKDIR = "make-dir"
FILE_OP_SHORT_MKDIR = "mkdir"

FILE_OP_LONG_REMOVE = "remove"
FILE_OP_SHORT_REMOVE = "rm"

# The long name is the canonical name.
fileop_normal_name = {
    FILE_OP_SHORT_COPY: FILE_OP_LONG_COPY,
    FILE_OP_LONG_COPY: FILE_OP_LONG_COPY,

    FILE_OP_SHORT_MOVE: FILE_OP_LONG_MOVE,
    FILE_OP_LONG_MOVE: FILE_OP_LONG_MOVE,

    FILE_OP_SHORT_MKDIR: FILE_OP_LONG_MKDIR,
    FILE_OP_LONG_MKDIR: FILE_OP_LONG_MKDIR,

    FILE_OP_SHORT_REMOVE: FILE_OP_LONG_REMOVE,
    FILE_OP_LONG_REMOVE: FILE_OP_LONG_REMOVE,
}

# The number of operations for each file operation.
fileop_num_args = {
    FILE_OP_LONG_COPY: 2,
    FILE_OP_LONG_MOVE: 2,
    FILE_OP_LONG_MKDIR: 1,
    FILE_OP_LONG_REMOVE: 1,
}

def validate(operation):
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
            raise ValueError(f"Argument at index {i} ('{operation[i]}')"
                + f" is an invalid glob pattern: {error}.")

        operation[i] = path

    return operation

# Execute operation operation in the given directory.
def execute(operation, base_dir):
    validate(operation)

    command = operation[0]

    if (command == FILE_OP_LONG_COPY):
        source_path = _resolve_path(operation[1], base_dir)
        dest_path = _resolve_path(operation[2], base_dir)

        _handle_glob_file_operation(
            source_path, dest_path, autograder.util.dirent.copy, dirs_exist_ok = True
        )
    elif (command == FILE_OP_LONG_MOVE):
        source_path = _resolve_path(operation[1], base_dir)
        dest_path = _resolve_path(operation[2], base_dir)

        _handle_glob_file_operation(source_path, dest_path, autograder.util.dirent.move)
    elif (command == FILE_OP_LONG_MKDIR):
        path = _resolve_path(operation[1], base_dir)

        autograder.util.dir.mkdir(path)
    elif (command == FILE_OP_LONG_REMOVE):
        path_glob = _resolve_path(operation[1], base_dir)

        _handle_glob_remove(path_glob)
    else:
        raise ValueError(f"Unknown file operation: '{command}'.")

def validate_file_operations(operations):
    for operation in operations:
        validate(operation)

def exec_file_operations(operations, base_dir):
    for operation in operations:
        execute(operation, base_dir)

def _resolve_path(path, base_dir):
    if (os.path.isabs(path)):
        return os.path.normpath(path)

    return os.path.normpath(os.path.join(base_dir, path))

def _handle_glob_file_operation(source_path_glob, dest_path, operation, **kwargs):
    source_paths = _prep_for_globs(source_path_glob, dest_path)

    for source_path in source_paths:
        if (source_path == dest_path):
            continue

        operation(source_path, dest_path, **kwargs)

def _handle_glob_remove(path_glob):
    paths = glob.glob(path_glob)

    for path in paths:
        autograder.util.dirent.remove(path)

def _prep_for_globs(source_path_glob, dest_path):
    source_paths = glob.glob(source_path_glob)

    if (len(source_paths) == 0):
        raise FileNotFoundError(f"No such file or directory: '{source_path_glob}'.")

    if (len(source_paths) > 1):
        os.makedirs(dest_path, exist_ok = True)

    return source_paths
