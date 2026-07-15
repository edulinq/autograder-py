import typing

import edq.util.crypto

import autograder.api.config
import autograder.api.courses.assignments.submissions.fetch.course.attempts
import autograder.api.courses.assignments.submissions.fetch.testing
import autograder.model.config
import autograder.testing.server

class TestCourseAssignmentsFetchCourseAttempts(autograder.testing.server.ServerTest):
    """ Test fetching course submission attempts. """

    def test_base(self) -> None:
        """ Test base functionality. """

        submission = autograder.api.courses.assignments.submissions.fetch.testing.SUBMISSIONS['course-student@test.edulinq.org'][2]

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
                {
                    "course-admin@test.edulinq.org": None,
                    "course-grader@test.edulinq.org": None,
                    "course-other@test.edulinq.org": None,
                    "course-owner@test.edulinq.org": None,
                    "course-student@test.edulinq.org": submission,
                },
                None,
            ),

            # Reference
            (
                autograder.model.config.Config(
                    auth_user = 'server-admin@test.edulinq.org',
                    auth_pass = edq.util.crypto.Secret('server-admin'),
                    course = 'course101',
                    assignment = 'hw0',
                    target_users = [
                        'course-admin@test.edulinq.org',
                        'course-student@test.edulinq.org',
                    ],
                ),
                {},
                {
                    "course-admin@test.edulinq.org": None,
                    "course-student@test.edulinq.org": submission,
                },
                None,
            ),
        ]

        self.base_api_test(autograder.api.courses.assignments.submissions.fetch.course.attempts.send, test_cases)
