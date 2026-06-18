import autograder.api.config
import autograder.api.users.tokens.create
import autograder.testing.asserts
import autograder.testing.model
import autograder.testing.server

class TestUsersTokensCreate(autograder.testing.server.ServerTest):
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
            # Self - No Name
            (
                autograder.model.config.Config(
                    auth_user = 'server-user@test.edulinq.org',
                    auth_pass = 'server-user',
                ),
                {},
                {
                    "found-user": True,
                    "token-cleartext": autograder.testing.constants.TEST_TOKEN_CLEARTEXT,
                    "token-info": {
                        "access-time": autograder.testing.constants.TEST_TIMESTAMP,
                        "creation-time": autograder.testing.constants.TEST_TIMESTAMP,
                        "id": autograder.testing.constants.TEST_TOKEN_ID,
                        "name": "",
                        "source": "user"
                    },
                },
                None,
            ),

            # Self - Name
            (
                autograder.model.config.Config(
                    auth_user = 'server-user@test.edulinq.org',
                    auth_pass = 'server-user',
                    name = 'new-token',
                ),
                {},
                {
                    "found-user": True,
                    "token-cleartext": autograder.testing.constants.TEST_TOKEN_CLEARTEXT,
                    "token-info": {
                        "access-time": autograder.testing.constants.TEST_TIMESTAMP,
                        "creation-time": autograder.testing.constants.TEST_TIMESTAMP,
                        "id": autograder.testing.constants.TEST_TOKEN_ID,
                        "name": "new-token",
                        "source": "user"
                    },
                },
                None,
            ),

            # Other
            (
                autograder.model.config.Config(
                    auth_user = 'server-admin@test.edulinq.org',
                    auth_pass = 'server-admin',
                    target_user = 'course-student@test.edulinq.org',
                ),
                {},
                {
                    "found-user": True,
                    "token-cleartext": autograder.testing.constants.TEST_TOKEN_CLEARTEXT,
                    "token-info": {
                        "access-time": autograder.testing.constants.TEST_TIMESTAMP,
                        "creation-time": autograder.testing.constants.TEST_TIMESTAMP,
                        "id": autograder.testing.constants.TEST_TOKEN_ID,
                        "name": "",
                        "source": "user"
                    },
                },
                None,
            ),

            # Other - Bad Permissions
            (
                autograder.model.config.Config(
                    auth_user = 'server-user@test.edulinq.org',
                    auth_pass = 'server-user',
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
                    auth_pass = 'server-admin',
                    target_user = 'ZZZ@test.edulinq.org',
                ),
                {},
                {
                    "found-user": False,
                    "token-cleartext": autograder.testing.constants.TEST_TOKEN_CLEARTEXT,
                    "token-info": None,
                },
                None,
            ),
        ]

        # Add a test case for each user, this helps others using the generated test data.
        for user in autograder.testing.model.SERVER_USERS.values():
            test_cases.append((
                autograder.model.config.Config(
                    auth_user = user.email,
                    auth_pass = user.name,
                ),
                {},
                {
                    "found-user": True,
                    "token-cleartext": autograder.testing.constants.TEST_TOKEN_CLEARTEXT,
                    "token-info": {
                        "access-time": autograder.testing.constants.TEST_TIMESTAMP,
                        "creation-time": autograder.testing.constants.TEST_TIMESTAMP,
                        "id": autograder.testing.constants.TEST_TOKEN_ID,
                        "name": "",
                        "source": "user"
                    },
                },
                None,
            ))

        self.base_api_test(autograder.api.users.tokens.create.send, test_cases, actual_clean_func = autograder.testing.asserts.normalize_dict)
