import enum
import typing

import lms.model.users
import lms.model.scores

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

    def __str__(self) -> str:
        return str(self.value)

    @classmethod
    def has_value(cls, value: typing.Any) -> bool:
        """
        Check if a value is present in the enum.
        Required for older versions of Python.
        """

        return (value is not None) and (str(value).upper() in cls.__members__)

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
        role = lms.model.users.CourseRole(CourseRole.OWNER.value),
        **vars(user),
    )

def make_assignment_score(raw_score: typing.Dict[str, typing.Any]) -> lms.model.scores.AssignmentScore:
    """
    Create an LMS Toolkit assignment score from raw data coming from the autograder.
    The raw data from the server should be a model.SubmissionHistoryItem.
    """

    data = {
        'id': raw_score['id'],
        'score': raw_score['score'],
        'submission_date': raw_score['grading_start_time'],
        'graded_date': raw_score['grading_start_time'],
        'comment': raw_score['message'],
        'assignment_query': raw_score['assignment-id'],
        'user_query': raw_score['user'],
    }

    return lms.model.scores.AssignmentScore(**data)
