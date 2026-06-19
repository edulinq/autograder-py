import typing

import edq.util.crypto
import edq.util.time
import lms.model.assignments
import lms.model.scores
import lms.model.users

import autograder.api.config
import autograder.api.courses.assignments.submissions.fetch.user.history
import autograder.model.config
import autograder.testing.server

class TestCourseAssignmentsFetchUserHistory(autograder.testing.server.ServerTest):
    """ Test fetching user submission history. """

    def test_base(self) -> None:
        """ Test base functionality. """

        # [(config (and overrides), kwargs, expected, error substring), ...]
        test_cases: typing.List[typing.Tuple[
            autograder.model.config.Config,
            typing.Dict[str, typing.Any],
            typing.Any,
            typing.Union[str, None],
        ]] = [
            # Base
            (
                autograder.model.config.Config(
                    auth_user = 'server-admin@test.edulinq.org',
                    auth_pass = edq.util.crypto.Secret('server-admin'),
                    course = 'course101',
                    assignment = 'hw0',
                    target_email = 'course-student@test.edulinq.org',
                ),
                {},
                (
                    True,
                    SCORES,
                ),
                None,
            ),
            (
                autograder.model.config.Config(
                    auth_user = 'course-admin@test.edulinq.org',
                    auth_pass = edq.util.crypto.Secret('course-admin'),
                    course = 'course101',
                    assignment = 'hw0',
                    target_email = 'course-student@test.edulinq.org',
                ),
                {},
                (
                    True,
                    SCORES,
                ),
                None,
            ),

            # No History, Self
            (
                autograder.model.config.Config(
                    auth_user = 'server-admin@test.edulinq.org',
                    auth_pass = edq.util.crypto.Secret('server-admin'),
                    course = 'course101',
                    assignment = 'hw0',
                ),
                {},
                (
                    True,
                    [],
                ),
                None,
            ),

            # No User
            (
                autograder.model.config.Config(
                    auth_user = 'server-admin@test.edulinq.org',
                    auth_pass = edq.util.crypto.Secret('server-admin'),
                    course = 'course101',
                    assignment = 'hw0',
                    target_email = 'ZZZ@test.edulinq.org',
                ),
                {},
                (
                    False,
                    [],
                ),
                None,
            ),
        ]

        self.base_api_test(autograder.api.courses.assignments.submissions.fetch.user.history.send, test_cases)

SCORES: typing.List[lms.model.scores.AssignmentScore] = [
    lms.model.scores.AssignmentScore(
        assignment = lms.model.assignments.AssignmentQuery('hw0'),
        comment = '',
        graded_date = edq.util.time.Timestamp(1697406256000),
        id = 'course101::hw0::course-student@test.edulinq.org::1697406256',
        score = 0,
        submission_date = edq.util.time.Timestamp(1697406256000),
        user = lms.model.users.UserQuery(email = 'course-student@test.edulinq.org'),
    ),
    lms.model.scores.AssignmentScore(
        assignment = lms.model.assignments.AssignmentQuery('hw0'),
        comment = '',
        graded_date = edq.util.time.Timestamp(1697406266000),
        id = 'course101::hw0::course-student@test.edulinq.org::1697406265',
        score = 1,
        submission_date = edq.util.time.Timestamp(1697406266000),
        user = lms.model.users.UserQuery(email = 'course-student@test.edulinq.org'),
    ),
    lms.model.scores.AssignmentScore(
        assignment = lms.model.assignments.AssignmentQuery('hw0'),
        comment = '',
        graded_date = edq.util.time.Timestamp(1697406273000),
        id = 'course101::hw0::course-student@test.edulinq.org::1697406272',
        score = 2,
        submission_date = edq.util.time.Timestamp(1697406273000),
        user = lms.model.users.UserQuery(email = 'course-student@test.edulinq.org'),
    ),
]
