import typing

import edq.util.crypto

import autograder.api.config
import autograder.api.courses.users.get
import autograder.model.config
import autograder.model.user
import autograder.testing.model
import autograder.testing.server

class TestUsersGet(autograder.testing.server.ServerTest):
    """ Test getting course users. """

    def test_base(self) -> None:
        """ Test base functionality. """

        # [(config (and overrides), kwargs, expected, error substring), ...]
        test_cases: typing.List[typing.Tuple[
            autograder.model.config.Config,
            typing.Dict[str, typing.Any],
            typing.Any,
            typing.Union[str, None],
        ]] = [
            # Base - Other
            (
                autograder.model.config.Config(
                    course = 'course101',
                    auth_user = 'course-grader@test.edulinq.org',
                    auth_pass = edq.util.crypto.Secret('course-grader'),
                    target_email = 'course-student@test.edulinq.org',
                ),
                {},
                autograder.testing.model.COURSE_USERS['Course 101']['course-student'],
                None,
            ),

            # Base - Self (Admin)
            (
                autograder.model.config.Config(
                    course = 'course101',
                    auth_user = 'course-grader@test.edulinq.org',
                    auth_pass = edq.util.crypto.Secret('course-grader'),
                ),
                {},
                autograder.testing.model.COURSE_USERS['Course 101']['course-grader'],
                None,
            ),

            # Base - Self (Non-Admin)
            (
                autograder.model.config.Config(
                    course = 'course101',
                    auth_user = 'course-student@test.edulinq.org',
                    auth_pass = edq.util.crypto.Secret('course-student'),
                ),
                {},
                autograder.testing.model.COURSE_USERS['Course 101']['course-student'],
                None,
            ),

            # Missing
            (
                autograder.model.config.Config(
                    course = 'course101',
                    auth_user = 'course-grader@test.edulinq.org',
                    auth_pass = edq.util.crypto.Secret('course-grader'),
                    target_email = 'server-user@test.edulinq.org',
                ),
                {},
                None,
                None,
            ),

            # Bad Permissions
            (
                autograder.model.config.Config(
                    course = 'course101',
                    auth_user = 'course-other@test.edulinq.org',
                    auth_pass = edq.util.crypto.Secret('course-other'),
                    target_email = 'course-student@test.edulinq.org',
                ),
                {
                    'exit_on_error': False,
                },
                None,
                'You have insufficient permissions',
            ),

            # User Promotion
            (
                autograder.model.config.Config(
                    course = 'course101',
                    auth_user = 'server-admin@test.edulinq.org',
                    auth_pass = edq.util.crypto.Secret('server-admin'),
                ),
                {},
                autograder.model.user.promote_server_user(autograder.testing.model.SERVER_USERS['server-admin']),
                None,
            ),
        ]

        self.base_api_test(autograder.api.courses.users.get.send, test_cases)
