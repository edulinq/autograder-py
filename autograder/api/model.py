import typing

import lms.model.users

def make_course_user(raw_user: typing.Dict[str, typing.Any]) -> lms.model.users.CourseUser:
    """
    Create an LMS Toolkit course user from raw data coming from the autograder.
    """

    raw_user = raw_user.copy()

    raw_user['id'] = raw_user['email']
    raw_user['raw_role'] = raw_user['role']
    raw_user['role'] = lms.model.users.CourseRole(raw_user['raw_role'])

    return lms.model.users.CourseUser(**raw_user)

def make_server_user(raw_user: typing.Dict[str, typing.Any]) -> lms.model.users.ServerUser:
    """
    Create an LMS Toolkit server user from raw data coming from the autograder.
    """

    return lms.model.users.ServerUser(
        id = raw_user['email'],
        **raw_user,
    )

def promote_server_user(user: lms.model.users.ServerUser) -> lms.model.users.CourseUser:
    """
    A a server admin that has been "promoted" to a course user.
    """

    return lms.model.users.CourseUser(
        raw_role = 'owner',
        role = lms.model.users.CourseRole.OWNER,
        **vars(user),
    )
