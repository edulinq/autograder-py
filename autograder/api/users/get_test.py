import autograder.api.config
import autograder.api.users.get
import autograder.model.user
import autograder.testing.model
import autograder.testing.server

class TestUsersGet(autograder.testing.server.ServerTest):
    """ Test getting server users. """

    def test_base(self):
        """ Test base functionality. """

        # [(config (and overrides), kwargs, expected, error substring), ...]
        test_cases = [
            # Base - Other
            (
                {
                    autograder.api.config.PARAM_USER_EMAIL.config_key: 'server-admin@test.edulinq.org',
                    autograder.api.config.PARAM_USER_PASS.config_key: 'server-admin',
                    autograder.api.config.PARAM_TARGET_EMAIL_OR_SELF.config_key: 'course-student@test.edulinq.org',
                },
                {},
                autograder.testing.model.SERVER_USERS['course-student'],
                None,
            ),

            # Base - Self
            (
                {
                    autograder.api.config.PARAM_USER_EMAIL.config_key: 'server-admin@test.edulinq.org',
                    autograder.api.config.PARAM_USER_PASS.config_key: 'server-admin',
                },
                {},
                autograder.testing.model.SERVER_USERS['server-admin'],
                None,
            ),

            # Missing
            (
                {
                    autograder.api.config.PARAM_USER_EMAIL.config_key: 'server-admin@test.edulinq.org',
                    autograder.api.config.PARAM_USER_PASS.config_key: 'server-admin',
                    autograder.api.config.PARAM_TARGET_EMAIL_OR_SELF.config_key: 'ZZZ@test.edulinq.org',
                },
                {},
                None,
                None,
            ),

            # Bad Permissions
            (
                {
                    autograder.api.config.PARAM_USER_EMAIL.config_key: 'course-admin@test.edulinq.org',
                    autograder.api.config.PARAM_USER_PASS.config_key: 'course-admin',
                    autograder.api.config.PARAM_TARGET_EMAIL_OR_SELF.config_key: 'course-student@test.edulinq.org',
                },
                {
                    'exit_on_error': False,
                },
                None,
                'You have insufficient permissions',
            ),
        ]

        self.base_api_test(autograder.api.users.get.send, test_cases)
