import typing

import edq.util.crypto

import autograder.api.config
import autograder.api.users.tokens.list
import autograder.testing.asserts
import autograder.testing.server

class TestUsersTokensList(autograder.testing.server.ServerTest):
    """ Test creating tokens. """

    def test_base(self) -> None:
        """ Test base functionality. """

        # [(config (and overrides), kwargs, expected, error substring), ...]
        test_cases: typing.List[typing.Tuple[
            autograder.model.config.Config,
            typing.Dict[str, typing.Any],
            typing.Any,
            typing.Union[str, None],
        ]] = [
            # Self
            (
                autograder.model.config.Config(
                    auth_user = 'server-user@test.edulinq.org',
                    auth_pass = edq.util.crypto.Secret('server-user'),
                ),
                {},
                {
                    "found-user": True,
                    "tokens": [
                        {
                            "access-time": autograder.testing.constants.TEST_TIMESTAMP,
                            "creation-time": autograder.testing.constants.TEST_TIMESTAMP,
                            "id": autograder.testing.constants.TEST_TOKEN_ID,
                            "name": "test",
                            "source": "user"
                        },
                    ]
                },
                None,
            ),

            # Other
            (
                autograder.model.config.Config(
                    auth_user = 'server-admin@test.edulinq.org',
                    auth_pass = edq.util.crypto.Secret('server-admin'),
                    target_user = 'course-student@test.edulinq.org',
                ),
                {},
                {
                    "found-user": True,
                    "tokens": [
                        {
                            "access-time": autograder.testing.constants.TEST_TIMESTAMP,
                            "creation-time": autograder.testing.constants.TEST_TIMESTAMP,
                            "id": autograder.testing.constants.TEST_TOKEN_ID,
                            "name": "test",
                            "source": "user"
                        },
                    ]
                },
                None,
            ),

            # Other - Bad Permissions
            (
                autograder.model.config.Config(
                    auth_user = 'server-user@test.edulinq.org',
                    auth_pass = edq.util.crypto.Secret('server-user'),
                    target_user = 'course-student@test.edulinq.org',
                ),
                {},
                None,
                "You have insufficient permissions for the requested operation",
            ),

            # Other - Missing User
            (
                autograder.model.config.Config(
                    auth_user = 'server-admin@test.edulinq.org',
                    auth_pass = edq.util.crypto.Secret('server-admin'),
                    target_user = 'ZZZ@test.edulinq.org',
                ),
                {},
                {
                    "found-user": False,
                    "tokens": None,
                },
                None,
            ),
        ]

        self.base_api_test(autograder.api.users.tokens.list.send, test_cases, actual_clean_func = autograder.testing.asserts.normalize_dict)
