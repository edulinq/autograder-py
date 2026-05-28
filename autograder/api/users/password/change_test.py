import autograder.api.config
import autograder.api.users.password.change
import autograder.testing.server

class TestUsersPasswordChange(autograder.testing.server.ServerTest):
    """ Test changing passwords. """

    def test_base(self):
        """ Test base functionality. """

        # [(config (and overrides), kwargs, expected, error substring), ...]
        test_cases = [
            # Base
            (
                {
                    autograder.api.config.PARAM_USER_EMAIL.config_key: 'server-user@test.edulinq.org',
                    autograder.api.config.PARAM_USER_PASS.config_key: 'server-user',

                    autograder.api.config.PARAM_NEW_PASS.config_key: 'abc123',
                },
                {},
                {
                    "duplicate": False,
                    "success": True,
                },
                None,
            ),

            # Duplicate
            (
                {
                    autograder.api.config.PARAM_USER_EMAIL.config_key: 'server-user@test.edulinq.org',
                    autograder.api.config.PARAM_USER_PASS.config_key: 'server-user',

                    autograder.api.config.PARAM_NEW_PASS.config_key: 'server-user',
                },
                {},
                {
                    "duplicate": True,
                    "success": True,
                },
                None,
            ),
        ]

        self.base_api_test(autograder.api.users.password.change.send, test_cases)
