import enum
import typing

import lms.model.users

class CourseRole(enum.Enum):
    """
    Different roles a user can have on an autograder course.
    """

    UNKNOWN = 'unknown'
    OTHER = 'other'
    STUDENT = 'student'
    GRADER = 'grader'
    ADMIN = 'admin'
    OWNER = 'owner'

    def __str__(self) -> str:
        return str(self.value)

    def __lt__(self, other: object) -> bool:
        if (not isinstance(other, CourseRole)):
            return False

        return COURSE_ROLE_NUMERIC_VALUES[self] < COURSE_ROLE_NUMERIC_VALUES[other]

    @classmethod
    def has_value(cls, value: typing.Any) -> bool:
        """
        Check if a value is present in the enum.
        Required for older versions of Python.
        """

        return (value is not None) and (str(value).upper() in cls.__members__)

class ServerRole(enum.Enum):
    """
    Different roles a user can have on an autograder server.
    """

    UNKNOWN = 'unknown'
    USER = 'user'
    CREATOR = 'creator'
    ADMIN = 'admin'
    OWNER = 'owner'
    ROOT = 'root'

    def __str__(self) -> str:
        return str(self.value)

    def __lt__(self, other: object) -> bool:
        if (not isinstance(other, ServerRole)):
            return False

        return SERVER_ROLE_NUMERIC_VALUES[self] < SERVER_ROLE_NUMERIC_VALUES[other]

    @classmethod
    def has_value(cls, value: typing.Any) -> bool:
        """
        Check if a value is present in the enum.
        Required for older versions of Python.
        """

        return (value is not None) and (str(value).upper() in cls.__members__)

COURSE_ROLE_NUMERIC_VALUES: typing.Dict[CourseRole, int] = {
    CourseRole.UNKNOWN: 0,
    CourseRole.OTHER: 10,
    CourseRole.STUDENT: 20,
    CourseRole.GRADER: 30,
    CourseRole.ADMIN: 40,
    CourseRole.OWNER: 50,
}

SERVER_ROLE_NUMERIC_VALUES: typing.Dict[ServerRole, int] = {
    ServerRole.UNKNOWN: 0,
    ServerRole.USER: 10,
    ServerRole.CREATOR: 20,
    ServerRole.ADMIN: 30,
    ServerRole.OWNER: 40,
    ServerRole.ROOT: 50,
}

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

    raw_user['role'] = ServerRole(raw_user['role'])

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
        role = lms.model.users.CourseRole(CourseRole.OWNER.value),
        **vars(user),
    )
