import typing

import edq.util.crypto

import autograder.api.config
import autograder.api.users.password.change
import autograder.testing.server

class TestUsersPasswordChange(autograder.testing.server.ServerTest):
    """ Test changing passwords. """

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
                    auth_user = 'server-user@test.edulinq.org',
                    auth_pass = edq.util.crypto.Secret('server-user'),

                    new_pass = 'abc123',
                ),
                {},
                {
                    "duplicate": False,
                    "success": True,
                },
                None,
            ),

            # Duplicate
            (
                autograder.model.config.Config(
                    auth_user = 'server-user@test.edulinq.org',
                    auth_pass = edq.util.crypto.Secret('server-user'),

                    new_pass = 'server-user',
                ),
                {},
                {
                    "duplicate": True,
                    "success": True,
                },
                None,
            ),
        ]

        self.base_api_test(autograder.api.users.password.change.send, test_cases)
