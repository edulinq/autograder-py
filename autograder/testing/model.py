"""
Data for tests.
Most model data will be copied over from the LMS toolkit and updated for the autograder.
"""

import typing

import lms.model.testdata.users
import lms.model.users

def _clean_server_users() -> typing.Dict[str, lms.model.users.ServerUser]:
    """ Copy over the LMS Toolkit test server users, but replace the ID with email. """

    users = lms.model.testdata.users.SERVER_USERS.copy()
    for user in users.values():
        user.id = user.email

    return users

# {name: user, ...}
SERVER_USERS: typing.Dict[str, lms.model.users.ServerUser] = _clean_server_users()
