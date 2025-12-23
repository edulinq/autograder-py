"""
Handle interfacing with git repos.
"""

import os
import re
import typing

import git

def ensure_repo(
        url: str,
        path: str,
        username: typing.Union[str, None] = None,
        token: typing.Union[str, None] = None,
        update: bool = False,
        ref: typing.Union[str, None] = None,
        ) -> None:
    """
    Ensure that a git repo exists locally.
    Clone the repo if it does not exist.
    Optionally update (pull) the repo.
    """

    if (os.path.isfile(path)):
        raise ValueError(f"Target git path exists and is a file: '{path}'.")

    if (not os.path.exists(path)):
        clone(url, path, username = username, token = token)

    repo = get_repo(path)

    if (update):
        update_repo(repo)

    if (ref is not None):
        checkout_repo(repo, ref)

def get_repo(path: str) -> git.Repo:
    """ Get a reference to a git repo. """

    return git.Repo(path)

def clone(
        url: str,
        path: str,
        username: typing.Union[str, None] = None,
        token: typing.Union[str, None] = None,
        ) -> git.Repo:
    """ Clone a git repo to the target location and return a reference to it. """

    # If we have a username or password, we need to rewrite the URL.
    # This is not very robust, but should work.
    # After clone, the credentials are saved in the local git config.
    if (username is not None):
        if (token is None):
            raise ValueError("If username is specified, a token must also be specified.")

        auth_text = f"{username}:{token}"
        url = re.sub(r'(http(s?)://)', rf"\1{auth_text}@", url)

    return git.Repo.clone_from(url, path)

def checkout_repo(repo: git.Repo, ref: str) -> None:
    """ Checkout the given reference on the given repo. """

    repo.git.checkout(ref)

def update_repo(repo: git.Repo) -> bool:
    """
    Update (pull) the given repo.
    Return true if an update occurred.
    """

    fetch_results = repo.remotes.origin.pull()

    for fetch_result in fetch_results:
        if (fetch_result.ref.name != f"origin/{repo.active_branch.name}"):
            continue

        if (fetch_result.flags == git.remote.FetchInfo.HEAD_UPTODATE):
            return False

        return True

    return False
