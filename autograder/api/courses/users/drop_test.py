import typing

import edq.util.crypto

import autograder.api.config
import autograder.api.courses.users.drop
import autograder.model.config
import autograder.testing.server

class TestUsersDrop(autograder.testing.server.ServerTest):
    """ Test dropping course users. """

    def test_base(self) -> None:
        """ Test base functionality. """

        # [(config (and overrides), kwargs, expected, error substring), ...]
        test_cases: typing.List[typing.Tuple[
            autograder.model.config.Config,
            typing.Dict[str, typing.Any],
            typing.Any,
            typing.Union[str, None],
        ]] = [
            # Enrolled User
            (
                autograder.model.config.Config(
                    course = 'course101',
                    auth_user = 'server-admin@test.edulinq.org',
                    auth_pass = edq.util.crypto.Secret('server-admin'),

                    target_email = 'course-student@test.edulinq.org',
                ),
                {},
                {
                    "found-user": True,
                },
                None,
            ),

            # Non-Enrolled User
            (
                autograder.model.config.Config(
                    course = 'course101',
                    auth_user = 'server-admin@test.edulinq.org',
                    auth_pass = edq.util.crypto.Secret('server-admin'),

                    target_email = 'server-user@test.edulinq.org',
                ),
                {},
                {
                    "found-user": False,
                },
                None,
            ),

            # Unknown User
            (
                autograder.model.config.Config(
                    course = 'course101',
                    auth_user = 'server-admin@test.edulinq.org',
                    auth_pass = edq.util.crypto.Secret('server-admin'),

                    target_email = 'ZZZ@test.edulinq.org',
                ),
                {},
                {
                    "found-user": False,
                },
                None,
            ),
        ]

        self.base_api_test(autograder.api.courses.users.drop.send, test_cases)
