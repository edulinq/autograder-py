import autograder.api.config
import autograder.api.users.tokens.create
import autograder.testing.asserts
import autograder.testing.server

class TestUsersTokensCreate(autograder.testing.server.ServerTest):
    """ Test creating tokens. """

    def test_base(self):
        """ Test base functionality. """

        # [(config (and overrides), kwargs, expected, error substring), ...]
        test_cases = [
            # Self - No Name
            (
                {
                    autograder.api.config.PARAM_USER_EMAIL.config_key: 'server-user@test.edulinq.org',
                    autograder.api.config.PARAM_USER_PASS.config_key: 'server-user',
                },
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
                {
                    autograder.api.config.PARAM_USER_EMAIL.config_key: 'server-user@test.edulinq.org',
                    autograder.api.config.PARAM_USER_PASS.config_key: 'server-user',
                    autograder.api.config.PARAM_NAME.config_key: 'new-token',
                },
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
                {
                    autograder.api.config.PARAM_USER_EMAIL.config_key: 'server-admin@test.edulinq.org',
                    autograder.api.config.PARAM_USER_PASS.config_key: 'server-admin',
                    autograder.api.config.PARAM_TARGET_USER_OR_SELF.config_key: 'course-student@test.edulinq.org',
                },
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
                {
                    autograder.api.config.PARAM_USER_EMAIL.config_key: 'server-user@test.edulinq.org',
                    autograder.api.config.PARAM_USER_PASS.config_key: 'server-user',
                    autograder.api.config.PARAM_TARGET_USER_OR_SELF.config_key: 'course-student@test.edulinq.org',
                },
                {},
                None,
                "You have insufficient permissions for the requested operation",
            ),

            # Other - Missing User
            (
                {
                    autograder.api.config.PARAM_USER_EMAIL.config_key: 'server-admin@test.edulinq.org',
                    autograder.api.config.PARAM_USER_PASS.config_key: 'server-admin',
                    autograder.api.config.PARAM_TARGET_USER_OR_SELF.config_key: 'ZZZ@test.edulinq.org',
                },
                {},
                {
                    "found-user": False,
                    "token-cleartext": autograder.testing.constants.TEST_TOKEN_CLEARTEXT,
                    "token-info": None,
                },
                None,
            ),
        ]

        self.base_api_test(autograder.api.users.tokens.create.send, test_cases, actual_clean_func = autograder.testing.asserts.normalize_dict)
