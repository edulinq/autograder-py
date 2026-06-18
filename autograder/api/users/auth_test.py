import typing

import autograder.api.users.auth
import autograder.model.config
import autograder.testing.server

class TestUsersAuth(autograder.testing.server.ServerTest):
    """ Test authenticating users. """

    def test_base(self) -> None:
        """ Test base functionality. """

        # [(config, kwargs, expected, error substring), ...]
        test_cases: typing.List[typing.Tuple[
            autograder.model.config.Config,
            typing.Dict[str, typing.Any],
            typing.Any,
            typing.Union[str, None],
        ]] = [
            # Base - Auth
            (
                autograder.model.config.Config(
                    auth_user = 'server-admin@test.edulinq.org',
                    auth_pass = 'server-admin',
                ),
                {},
                True,
                None,
            ),

            # Base - No Auth
            (
                autograder.model.config.Config(
                    auth_user = 'server-admin@test.edulinq.org',
                    auth_pass = 'ZZZ',
                ),
                {
                    'exit_on_error': False,
                },
                None,
                'Authentication failure',
            ),

            # Missing
            (
                autograder.model.config.Config(
                    auth_user = 'ZZZ',
                    auth_pass = 'ZZZ',
                ),
                {
                    'exit_on_error': False,
                },
                None,
                'Authentication failure',
            ),
        ]

        self.base_api_test(autograder.api.users.auth.send, test_cases)
