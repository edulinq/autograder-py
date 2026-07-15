import typing

import edq.util.crypto
import edq.util.time
import lms.model.assignments
import lms.model.scores
import lms.model.users

import autograder.api.config
import autograder.api.courses.assignments.submissions.fetch.course.scores
import autograder.model.config
import autograder.testing.model
import autograder.testing.server

class TestCourseAssignmentsFetchCourseScores(autograder.testing.server.ServerTest):
    """ Test fetching course scores. """

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
                ),
                {},
                FULL_SCORES,
                None,
            ),

            # Query
            (
                autograder.model.config.Config(
                    auth_user = 'server-admin@test.edulinq.org',
                    auth_pass = edq.util.crypto.Secret('server-admin'),
                    course = 'course101',
                    assignment = 'hw0',
                    target_users = [
                        'student',
                    ],
                ),
                {},
                [STUDENT_SCORE],
                None,
            ),

            # Query (Empty)
            (
                autograder.model.config.Config(
                    auth_user = 'server-admin@test.edulinq.org',
                    auth_pass = edq.util.crypto.Secret('server-admin'),
                    course = 'course101',
                    assignment = 'hw0',
                    target_users = [
                        'ZZZ@test.edulinq.org',
                    ],
                ),
                {},
                [],
                None,
            ),

            # Course Admin
            (
                autograder.model.config.Config(
                    auth_user = 'course-admin@test.edulinq.org',
                    auth_pass = edq.util.crypto.Secret('course-admin'),
                    course = 'course101',
                    assignment = 'hw0',
                    target_users = [
                        'student',
                    ],
                ),
                {},
                [STUDENT_SCORE],
                None,
            ),
        ]

        self.base_api_test(autograder.api.courses.assignments.submissions.fetch.course.scores.send, test_cases)

STUDENT_SCORE: lms.model.scores.AssignmentScore = lms.model.scores.AssignmentScore(
    assignment = lms.model.assignments.AssignmentQuery(id = 'hw0'),
    comment = '',
    graded_date = edq.util.time.Timestamp(1697406273000),
    id = 'course101::hw0::course-student@test.edulinq.org::1697406272',
    score = 2,
    submission_date = edq.util.time.Timestamp(1697406273000),
    user = lms.model.users.UserQuery(email = 'course-student@test.edulinq.org'),
)

FULL_SCORES: typing.List[lms.model.scores.AssignmentScore] = [
    lms.model.scores.AssignmentScore(
            assignment = lms.model.assignments.AssignmentQuery(id = 'hw0'),
            user = lms.model.users.UserQuery(email = 'course-admin@test.edulinq.org')),
    lms.model.scores.AssignmentScore(
            assignment = lms.model.assignments.AssignmentQuery(id = 'hw0'),
            user = lms.model.users.UserQuery(email = 'course-grader@test.edulinq.org')),
    lms.model.scores.AssignmentScore(
            assignment = lms.model.assignments.AssignmentQuery(id = 'hw0'),
            user = lms.model.users.UserQuery(email = 'course-other@test.edulinq.org')),
    lms.model.scores.AssignmentScore(
            assignment = lms.model.assignments.AssignmentQuery(id = 'hw0'),
            user = lms.model.users.UserQuery(email = 'course-owner@test.edulinq.org')),
    STUDENT_SCORE,
]
