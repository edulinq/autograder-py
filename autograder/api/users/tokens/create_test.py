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
            # No Name
            (
                {
                    autograder.api.config.PARAM_USER_EMAIL.config_key: 'server-user@test.edulinq.org',
                    autograder.api.config.PARAM_USER_PASS.config_key: 'server-user',
                },
                {},
                {
                    "token-cleartext": autograder.testing.constants.TEST_TOKEN_CLEARTEXT,
                    "token-id": autograder.testing.constants.TEST_TOKEN_ID,
                },
                None,
            ),

            # Name
            (
                {
                    autograder.api.config.PARAM_USER_EMAIL.config_key: 'server-user@test.edulinq.org',
                    autograder.api.config.PARAM_USER_PASS.config_key: 'server-user',
                    autograder.api.config.PARAM_NAME.config_key: 'new-token',
                },
                {},
                {
                    "token-cleartext": autograder.testing.constants.TEST_TOKEN_CLEARTEXT,
                    "token-id": autograder.testing.constants.TEST_TOKEN_ID,
                },
                None,
            ),
        ]

        self.base_api_test(autograder.api.users.tokens.create.send, test_cases, actual_clean_func = autograder.testing.asserts.normalize_dict)
