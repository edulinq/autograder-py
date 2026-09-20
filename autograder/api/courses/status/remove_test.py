import typing

import edq.util.crypto

import autograder.api.courses.status.remove
import autograder.model.config
import autograder.testing.server

class TestCoursesStatusRemove(autograder.testing.server.ServerTest):
    """ Test removing a course status. """

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
                    auth_user = 'course-admin@test.edulinq.org',
                    auth_pass = edq.util.crypto.Secret('course-admin'),
                    course = 'course101',
                ),
                {},
                {
                    "removed": {},
                },
                None,
            ),

            # Bad Permissions
            (
                autograder.model.config.Config(
                    auth_user = 'course-grader@test.edulinq.org',
                    auth_pass = edq.util.crypto.Secret('course-grader'),
                    course = 'course101',
                ),
                {
                    'exit_on_error': False,
                },
                None,
                'You have insufficient permissions',
            ),
        ]

        self.base_api_test(autograder.api.courses.status.remove.send, test_cases)
