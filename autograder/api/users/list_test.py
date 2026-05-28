import autograder.api.config
import autograder.api.users.list
import autograder.testing.model
import autograder.testing.server

class TestUsersList(autograder.testing.server.ServerTest):
    """ Test getting server users. """

    def test_base(self):
        """ Test base functionality. """

        # [(config (and overrides), kwargs, expected, error substring), ...]
        test_cases = [
            (
                {
                    autograder.api.config.PARAM_USER_EMAIL.config_key: 'server-admin@test.edulinq.org',
                    autograder.api.config.PARAM_USER_PASS.config_key: 'server-admin',
                },
                {},
                sorted(autograder.testing.model.SERVER_USERS.values()),
                None,
            ),
        ]

        self.base_api_test(autograder.api.users.list.send, test_cases)
