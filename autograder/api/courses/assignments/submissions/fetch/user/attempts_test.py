import typing

import autograder.api.config
import autograder.api.courses.assignments.submissions.fetch.testing
import autograder.api.courses.assignments.submissions.fetch.user.attempts
import autograder.model.config
import autograder.testing.server

class TestCourseAssignmentsFetchUserAttempts(autograder.testing.server.ServerTest):
    """ Test fetching user submission attempts. """

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
                    auth_pass = 'server-admin',
                    course = 'course101',
                    assignment = 'hw0',
                    target_email = 'course-student@test.edulinq.org',
                ),
                {},
                (
                    True,
                    autograder.api.courses.assignments.submissions.fetch.testing.SUBMISSIONS['course-student@test.edulinq.org'],
                ),
                None,
            ),

            # Missing User
            (
                autograder.model.config.Config(
                    auth_user = 'server-admin@test.edulinq.org',
                    auth_pass = 'server-admin',
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

            # No Submissions (Self)
            (
                autograder.model.config.Config(
                    auth_user = 'server-admin@test.edulinq.org',
                    auth_pass = 'server-admin',
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
        ]

        self.base_api_test(autograder.api.courses.assignments.submissions.fetch.user.attempts.send, test_cases)
