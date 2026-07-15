import typing

import edq.util.crypto

import autograder.api.users.list
import autograder.testing.model
import autograder.testing.server

class TestUsersList(autograder.testing.server.ServerTest):
    """ Test getting server users. """

    def test_base(self) -> None:
        """ Test base functionality. """

        # [(config (and overrides), kwargs, expected, error substring), ...]
        test_cases: typing.List[typing.Tuple[
            autograder.model.config.Config,
            typing.Dict[str, typing.Any],
            typing.Any,
            typing.Union[str, None],
        ]] = [
            (
                autograder.model.config.Config(
                    auth_user = 'server-admin@test.edulinq.org',
                    auth_pass = edq.util.crypto.Secret('server-admin'),
                ),
                {},
                sorted(autograder.testing.model.SERVER_USERS.values()),
                None,
            ),
        ]

        self.base_api_test(autograder.api.users.list.send, test_cases)
