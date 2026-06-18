import typing

import autograder.api.users.remove
import autograder.testing.server

class TestUsersRemove(autograder.testing.server.ServerTest):
    """ Test removing users. """

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

                    target_email = 'course-student@test.edulinq.org',
                ),
                {},
                {
                    "found-user": True,
                },
                None,
            ),

            # Unknown User
            (
                autograder.model.config.Config(
                    auth_user = 'server-admin@test.edulinq.org',
                    auth_pass = 'server-admin',

                    target_email = 'ZZZ@test.edulinq.org',
                ),
                {},
                {
                    "found-user": False,
                },
                None,
            ),

            # Bad Permissions
            (
                autograder.model.config.Config(
                    auth_user = 'course-owner@test.edulinq.org',
                    auth_pass = 'course-owner',

                    target_email = 'course-student@test.edulinq.org',
                ),
                {
                    'exit_on_error': False,
                },
                None,
                'You have insufficient permissions',
            ),
        ]

        self.base_api_test(autograder.api.users.remove.send, test_cases)
