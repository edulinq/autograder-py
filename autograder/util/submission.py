import os
import types

import autograder.code

ALL_SUBMISSION_KEY = '__all__'

def prepare(path, raise_on_collision = False):
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

    submission = {}

    if (os.path.isfile(path)):
        _prepare_submission_file(submission, path, [], raise_on_collision)
    else:
        _prepare_submission_dir(submission, path, [], raise_on_collision)

    return _dict_to_namespace(submission)

def _prepare_submission_dir(submission, path, prefix, raise_on_collision):
    if (not os.path.isdir(path)):
        raise ValueError("Preparation target must be a dir: '%s'." % path)

    for dirent in os.listdir(path):
        dirent_path = os.path.join(path, dirent)

        if (os.path.isfile(dirent_path)):
            if (os.path.splitext(dirent)[1] not in autograder.code.ALLOWED_EXTENSIONS):
                continue

            _prepare_submission_file(submission, dirent_path, prefix, raise_on_collision)
        else:
            _prepare_submission_dir(submission, dirent_path, prefix + [dirent], raise_on_collision)

def _prepare_submission_file(submission, path, prefix, raise_on_collision):
    if (not os.path.isfile(path)):
        raise ValueError("Preparation target must be a file: '%s'." % path)

    basename = os.path.splitext(os.path.basename(path))[0]

    defs = autograder.code.sanitize_and_import_path(path, as_dict = True)

    for (name, value) in defs.items():
        if (name.startswith('__')):
            continue

        if ((name in submission) and (raise_on_collision)):
            raise ValueError("Name collision ('%s') when importing all keys for '%s'." % (
                name, path))

        if (ALL_SUBMISSION_KEY not in submission):
            submission[ALL_SUBMISSION_KEY] = {}

        submission[ALL_SUBMISSION_KEY][name] = defs[name]

    # Place the defs into a structure that matches the path.
    context = submission
    for part in prefix + [basename]:
        if ((part in context) and (not isinstance(context[part], dict))):
            raise ValueError("Name collision ('%s') when importing all keys for '%s'." % (
                part, path))

        if (part not in context):
            context[part] = {}

        context = context[part]

    context.update(defs)

def _dict_to_namespace(root):
    if (not isinstance(root, dict)):
        return root

    for (key, value) in root.items():
        root[key] = _dict_to_namespace(value)

    return types.SimpleNamespace(**root)
