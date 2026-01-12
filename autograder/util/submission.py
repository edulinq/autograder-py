import os
import types
import typing

import edq.util.dirent
import edq.util.gzip
import edq.util.json

import autograder.code

ALL_SUBMISSION_KEY: str = '__all__'
ALLOWED_EXTENSIONS: typing.List[str] = ['.py', '.ipynb']

def prepare(path: str, raise_on_collision: bool = False) -> object:
    """
    Get a submission from a path, prepare it for grading,
    and return a submission namespace that contains all parsed entities.

    Directories will be fully recursively descended and each python or notebook will be prepared.

    Entries that begin with two underscores will not be included.

    The following things will be done to each file:
        1) The code will be parsed and sanitized.
        2) The sanitized code will be imported as a module into a namespace.
        3) The namespace will be made available in the returned namespace
            in a structure that matches its package structure.
            E.g. "./a/b/c.py" will be available from `prepare('.').a.b.c`,
            and "foo.py" will be available from `prepare('foo.py').foo`.
        4) All entries in the module will be put in the ALL_SUBMISSION_KEY attribute of the
            returned namespace.
            If raise_on_collision is True, an error will be raised if a key already exists.
    """

    submission: typing.Dict[str, typing.Any] = {}

    if (os.path.isfile(path)):
        _prepare_submission_file(submission, path, [], raise_on_collision)
    else:
        _prepare_submission_dir(submission, path, [], raise_on_collision)

    return _dict_to_namespace(submission)

def _prepare_submission_dir(
        submission: typing.Dict[str, typing.Any],
        path: str,
        prefix: typing.List[str],
        raise_on_collision: bool,
        ) -> None:
    """ Prepare a submission directory. """

    if (not os.path.isdir(path)):
        raise ValueError(f"Preparation target must be a dir: '{path}'.")

    for dirent in os.listdir(path):
        dirent_path = os.path.join(path, dirent)

        if (os.path.isfile(dirent_path)):
            if (os.path.splitext(dirent)[1] not in ALLOWED_EXTENSIONS):
                continue

            _prepare_submission_file(submission, dirent_path, prefix, raise_on_collision)
        else:
            _prepare_submission_dir(submission, dirent_path, prefix + [dirent], raise_on_collision)

def _prepare_submission_file(
        submission: typing.Dict[str, typing.Any],
        path: str,
        prefix: typing.List[str],
        raise_on_collision: bool,
        ) -> None:
    """ Prepare a submission file. """

    if (not os.path.isfile(path)):
        raise ValueError(f"Preparation target must be a file: '{path}'.")

    basename = os.path.splitext(os.path.basename(path))[0]

    defs = vars(autograder.code.sanitize_and_import_path(path))

    for (name, value) in defs.items():
        if (name.startswith('__')):
            continue

        if ((name in submission) and (raise_on_collision)):
            raise ValueError(f"Name collision ('{name}') when importing all keys for '{path}'.")

        if (ALL_SUBMISSION_KEY not in submission):
            submission[ALL_SUBMISSION_KEY] = {}

        submission[ALL_SUBMISSION_KEY][name] = value

    # Place the defs into a structure that matches the path.
    context = submission
    for part in prefix + [basename]:
        if ((part in context) and (not isinstance(context[part], dict))):
            raise ValueError(f"Name collision ('{part}') when importing all keys for '{path}'.")

        if (part not in context):
            context[part] = {}

        context = context[part]

    context.update(defs)

def _dict_to_namespace(root: typing.Union[typing.Dict, object]) -> object:
    """ Recursively convert a dict to a namespace. """

    if (not isinstance(root, dict)):
        return root

    for (key, value) in root.items():
        root[key] = _dict_to_namespace(value)

    return types.SimpleNamespace(**root)

def output_grading_result(result: typing.Dict[str, typing.Any], base_dir: str = '.', short_id: bool = False) -> str:
    """
    Write out an API grading result (model.GradingResult) to a directory inside the given base directory.
    Any existing directory will be removed (and re-created).
    Return the path to the created directory.
    """

    if (short_id):
        out_dir = os.path.join(base_dir, result['info']['short-id'])
    else:
        long_id = result['info']['id']

        # Windows doesn't like colons in filenames.
        if (os.name == 'nt'):
            long_id = long_id.replace(':', '_')

        out_dir = os.path.join(base_dir, long_id)

    edq.util.dirent.remove(out_dir)
    edq.util.dirent.mkdir(out_dir)

    stdout_path = os.path.join(out_dir, 'stdout.txt')
    edq.util.dirent.write_file(stdout_path, result['stdout'])

    stderr_path = os.path.join(out_dir, 'stderr.txt')
    edq.util.dirent.write_file(stderr_path, result['stderr'])

    result_path = os.path.join(out_dir, 'info.json')
    edq.util.json.dump_path(result['info'], result_path, indent = 4)

    grading_input_dir = os.path.join(out_dir, 'input')
    _output_grading_result_dir(grading_input_dir, result['input-files-gzip'])

    grading_output_dir = os.path.join(out_dir, 'output')
    _output_grading_result_dir(grading_output_dir, result['output-files-gzip'])

    return out_dir

def _output_grading_result_dir(out_dir: str, files: typing.Dict[str, str]) -> None:
    """ Write a collection of gzipped (base64) files to a directory. """

    edq.util.dirent.mkdir(out_dir)

    for (relpath, gzip_contents) in files.items():
        path = os.path.join(out_dir, *relpath.split('/'))
        edq.util.dirent.mkdir(os.path.dirname(path))

        contents = edq.util.gzip.uncompress_base64(gzip_contents)
        edq.util.dirent.write_file_bytes(path, contents)
