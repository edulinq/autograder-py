import autograder.api.config
import autograder.api.users.tokens.delete
import autograder.testing.server

class TestUsersTokensDelete(autograder.testing.server.ServerTest):
    """ Test deleting tokens. """

    def test_base(self):
        """ Test base functionality. """

        # [(config (and overrides), kwargs, expected, error substring), ...]
        test_cases = [
            # Base
            (
                {
                    autograder.api.config.PARAM_USER_EMAIL.config_key: 'course-admin@test.edulinq.org',
                    autograder.api.config.PARAM_USER_PASS.config_key: 'course-admin',
                    autograder.api.config.PARAM_TOKEN_ID.config_key: 'df0a1f16-9cd8-4395-8509-10ae314fe6fc',
                },
                {},
                {
                    "found": True,
                },
                None,
            ),

            # Bad ID
            (
                {
                    autograder.api.config.PARAM_USER_EMAIL.config_key: 'course-admin@test.edulinq.org',
                    autograder.api.config.PARAM_USER_PASS.config_key: 'course-admin',
                    autograder.api.config.PARAM_TOKEN_ID.config_key: 'ZZZ',
                },
                {},
                {
                    "found": False,
                },
                None,
            ),
        ]

        self.base_api_test(autograder.api.users.tokens.delete.send, test_cases)
