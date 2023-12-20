"""
Handle interfacing with git repos.
"""

import os
import re

import git

def ensure_repo(url, path,
        username = None, token = None,
        update = False, ref = None):
    if (os.path.isfile(path)):
        raise ValueError("Target git path exists and is a file: '%s'." % (path))

    if (not os.path.exists(path)):
        clone(url, path, username = username, token = token)

    repo = get_repo(path)

    if (update):
        update_repo(repo)

    if (ref is not None):
        checkout_repo(repo, ref)

def get_repo(path):
    return git.Repo(path)

def clone(url, path, username = None, token = None):
    # If we have a username or password, we need to rewrite the URL.
    # This is not very robust, but should work.
    # After clone, the credentials are saved in the local git config.
    if (username is not None):
        if (token is None):
            raise ValueError("If username is specified, token must also be specified.")

        auth_text = "%s:%s" % (username, token)
        url = re.sub(r'(http(s?)://)', r'\1%s@' % (auth_text), url)

    return git.Repo.clone_from(url, path)

def checkout_repo(repo, ref):
    repo.git.checkout(ref)

def update_repo(repo):
    fetch_results = repo.remotes.origin.pull()

    for fetch_result in fetch_results:
        if (fetch_result.ref.name != ("origin/%s" % (repo.active_branch.name))):
            continue

        if (fetch_result.flags == git.remote.FetchInfo.HEAD_UPTODATE):
            return False
        else:
            return True
