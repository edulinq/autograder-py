"""
Filespecs (File Specifications) are objects in assignment configs that describe
files that need to exist.
These files can come from local files (path FileSpec), URLs (url FileSpec),
or git repos (git FileSpec).
"""

import os
import urllib.parse

import autograder.util.dirent
import autograder.util.git
import autograder.util.http

FILESPEC_TYPE_EMPTY = "empty"
FILESPEC_TYPE_NIL = "nil"
FILESPEC_TYPE_PATH = "path"
FILESPEC_TYPE_GIT = "git"
FILESPEC_TYPE_URL = "url"

def parse(data):
    """
    Parse and validate a FileSpec.
    Return a properly formatted FileSpec.

    This parsing is more lenient than the parsing done by the autograder server:
    https://github.com/eriq-augustine/autograder-server/blob/main/common/filespec.go#L37
    """

    if (data is None):
        return get_empty()

    if (isinstance(data, str)):
        if (data == ""):
            return get_empty()

        return get_path(data)

    if (not isinstance(data, dict)):
        raise FileSpecError("FileSpec is not the correct type (str ot dict): '%s' (%s)." % (
            data, type(data)))

    if ('type' not in data):
        raise FileSpecError("FileSpec is missing 'type' field: '%s'." % (data))

    data['type'] = data['type'].strip().lower()

    spec_type = data['type']
    if (spec_type == FILESPEC_TYPE_EMPTY):
        return get_empty()
    elif (spec_type == FILESPEC_TYPE_NIL):
        return get_nil()
    elif (spec_type == FILESPEC_TYPE_PATH):
        path = data.get('path', '').strip()
        if (path == ''):
            raise FileSpecError("Path FileSpec must have a non-empty path: '%s'." % (data))

        return get_path(path, dest = data.get('dest', ''))
    elif (spec_type == FILESPEC_TYPE_GIT):
        path = data.get('path', '').strip()
        if (path == ''):
            raise FileSpecError("Git FileSpec must have a non-empty path: '%s'." % (data))

        return get_git(path,
            dest = data.get('dest', ''),
            reference = data.get('reference', ''),
            username = data.get('username', ''),
            token = data.get('token', ''))
    elif (spec_type == FILESPEC_TYPE_URL):
        path = data.get('path', '').strip()
        if (path == ''):
            raise FileSpecError("URL FileSpec must have a non-empty path: '%s'." % (data))

        return get_url(path, dest = data.get('dest', ''))
    else:
        raise FileSpecError("FileSpec has unkown type ('%s'): '%s'." % (spec_type, data))

def get_empty():
    return {
        "type": FILESPEC_TYPE_EMPTY,
    }

def get_nil():
    return {
        "type": FILESPEC_TYPE_NIL,
    }

def get_path(path, dest = ''):
    if (dest == ''):
        dest = os.path.basename(path)

    return {
        "type": FILESPEC_TYPE_PATH,
        "path": path,
        "dest": dest,
    }

def get_git(path, dest = '', reference = '', username = '', token = ''):
    if (dest == ''):
        dest = os.path.splitext(os.path.basename(path))[0]

    if ((username != '') and (token == '')):
        raise FileSpecError(("If username is specified on a Git FileSpec,"
            + " then token must also be specified."))

    return {
        "type": FILESPEC_TYPE_GIT,
        "path": path,
        "dest": dest,
        "reference": reference,
        "username": username,
        "token": token,
    }

def get_url(path, dest = ''):
    if (dest == ''):
        url = urllib.parse.urlparse(path)
        dest = os.path.basename(url.path)

    return {
        "type": FILESPEC_TYPE_URL,
        "path": path,
        "dest": dest,
    }

def copy(filespec, base_dir, dest_dir, only_contents):
    spec_type = filespec['type']
    if (spec_type in [FILESPEC_TYPE_EMPTY, FILESPEC_TYPE_NIL]):
        # no-op.
        return
    elif (spec_type == FILESPEC_TYPE_PATH):
        _copy_path(filespec['path'], filespec['dest'], base_dir, dest_dir, only_contents)
    elif (spec_type == FILESPEC_TYPE_GIT):
        _copy_git(filespec['path'], filespec['dest'], dest_dir,
                reference = filespec['reference'],
                username = filespec['username'],
                token = filespec['token'])
    elif (spec_type == FILESPEC_TYPE_URL):
        _copy_url(filespec['path'], filespec['dest'], dest_dir)
    else:
        raise FileSpecError("FileSpec has unkown type ('%s'): '%s'." % (spec_type, filespec))

def _copy_path(path, dest, base_dir, dest_dir, only_contents):
    source_path = path
    if ((not os.path.isabs(source_path)) and (base_dir != '')):
        source_path = os.path.join(base_dir, path)

    if (only_contents):
        dest_path = dest_dir

        if (dest != ''):
            dest_path = os.path.join(dest_dir, dest)
    else:
        filename = dest
        if (filename == ''):
            filename = os.path.basename(path)

        dest_path = os.path.join(dest_dir, filename)

    if (only_contents):
        autograder.util.dirent.copy_contents(source_path, dest_path)
    else:
        autograder.util.dirent.copy(source_path, dest_path)

def _copy_git(path, dest, dest_dir, reference = '', username = '', token = ''):
    if (reference == ''):
        reference = None

    if (username == ''):
        username = None

    if (token == ''):
        token = None

    dest_path = os.path.join(dest_dir, dest)

    autograder.util.git.ensure_repo(path, dest_path, update = True,
        ref = reference, username = username, token = token)

def _copy_url(path, dest, dest_dir):
    dest_path = os.path.join(dest_dir, dest)
    autograder.util.http.get(path, dest_path)

class FileSpecError(ValueError):
    pass
