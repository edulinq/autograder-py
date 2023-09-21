"""
Handle interfacing with git repos.
"""

import os

import git

def ensure_repo(url, path, update = False, ref = None):
    if (os.path.isfile(path)):
        raise ValueError("Target git path exists and is a file: '%s'." % (path))

    if (not os.path.exists(path)):
        clone(url, path)

    repo = get_repo(path)

    if (update):
        update_repo(repo)

    if (ref is not None):
        checkout_repo(repo, ref)

def get_repo(path):
    return git.Repo(path)

def clone(url, path):
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
