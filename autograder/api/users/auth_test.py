import autograder.api.config
import autograder.api.users.auth
import autograder.testing.server

class TestUsersAuth(autograder.testing.server.ServerTest):
    """ Test authenticating users. """

    def test_base(self):
        """ Test base functionality. """

        # [(config (and overrides), kwargs, expected, error substring), ...]
        test_cases = [
            # Base - Auth
            (
                {
                    autograder.api.config.PARAM_USER_EMAIL.config_key: 'server-admin@test.edulinq.org',
                    autograder.api.config.PARAM_USER_PASS.config_key: 'server-admin',
                },
                {},
                True,
                None,
            ),

            # Base - No Auth
            (
                {
                    autograder.api.config.PARAM_USER_EMAIL.config_key: 'server-admin@test.edulinq.org',
                    autograder.api.config.PARAM_USER_PASS.config_key: 'ZZZ',
                },
                {
                    'exit_on_error': False,
                },
                None,
                'Authentication failure',
            ),

            # Missing
            (
                {
                    autograder.api.config.PARAM_USER_EMAIL.config_key: 'ZZZ',
                    autograder.api.config.PARAM_USER_PASS.config_key: 'ZZZ',
                },
                {
                    'exit_on_error': False,
                },
                None,
                'Authentication failure',
            ),
        ]

        self.base_api_test(autograder.api.users.auth.send, test_cases)
