import autograder.api.config
import autograder.api.users.password.reset
import autograder.testing.server

class TestUsersPasswordReset(autograder.testing.server.ServerTest):
    """ Test resetting passwords. """

    def test_base(self):
        """ Test base functionality. """

        # [(config (and overrides), kwargs, expected, error substring), ...]
        test_cases = [
            # Base
            (
                {
                    autograder.api.config.PARAM_USER_EMAIL.config_key: 'server-user@test.edulinq.org',
                },
                {},
                {},
                None,
            ),

            # Missing
            (
                {
                    autograder.api.config.PARAM_USER_EMAIL.config_key: 'ZZZ',
                },
                {},
                {},
                None,
            ),
        ]

        self.base_api_test(autograder.api.users.password.reset.send, test_cases)
