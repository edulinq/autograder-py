import typing

import autograder.api.config
import autograder.api.users.password.reset
import autograder.testing.server

class TestUsersPasswordReset(autograder.testing.server.ServerTest):
    """ Test resetting passwords. """

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
                ),
                {},
                {},
                None,
            ),

            # Missing
            (
                autograder.model.config.Config(
                    auth_user = 'ZZZ',
                ),
                {},
                {},
                None,
            ),
        ]

        self.base_api_test(autograder.api.users.password.reset.send, test_cases)
