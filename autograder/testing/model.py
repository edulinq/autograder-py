"""
Data for tests.
Most model data will be copied over from the LMS toolkit and updated for the autograder.
"""

import typing

import lms.model.testdata.users
import lms.model.users

def _clean_server_user(user: lms.model.users.ServerUser) -> None:
    """
    Clean the server user for use with the autograder.
    Replace the ID with email.
    """

    user.id = str(user.email)

def _clean_server_users() -> typing.Dict[str, lms.model.users.ServerUser]:
    """ Copy over the LMS Toolkit test server users, but clean users. """

    users = lms.model.testdata.users.SERVER_USERS.copy()
    for user in users.values():
        _clean_server_user(user)

    return users

def _clean_course_users() -> typing.Dict[str, typing.Dict[str, lms.model.users.CourseUser]]:
    """ Copy over the LMS Toolkit test course users, but clean users. """

    course_users = {}

    for name, raw_users in lms.model.testdata.users.COURSE_USERS.items():
        users = raw_users.copy()
        for user in users.values():
            _clean_server_user(user)

        course_users[name] = users

    return course_users

# {name: user, ...}
SERVER_USERS: typing.Dict[str, lms.model.users.ServerUser] = _clean_server_users()

# {course_name: {user_name: user, ...}, ...}
COURSE_USERS: typing.Dict[str, typing.Dict[str, lms.model.users.CourseUser]] = _clean_course_users()
