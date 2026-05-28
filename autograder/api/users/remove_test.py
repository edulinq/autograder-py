import autograder.api.config
import autograder.api.users.remove
import autograder.testing.server

class TestUsersRemove(autograder.testing.server.ServerTest):
    """ Test removing users. """

    def test_base(self):
        """ Test base functionality. """

        # [(config (and overrides), kwargs, expected, error substring), ...]
        test_cases = [
            # Base
            (
                {
                    autograder.api.config.PARAM_USER_EMAIL.config_key: 'server-admin@test.edulinq.org',
                    autograder.api.config.PARAM_USER_PASS.config_key: 'server-admin',

                    autograder.api.config.PARAM_TARGET_EMAIL.config_key: 'course-student@test.edulinq.org',
                },
                {},
                {
                    "found-user": True,
                },
                None,
            ),

            # Unknown User
            (
                {
                    autograder.api.config.PARAM_USER_EMAIL.config_key: 'server-admin@test.edulinq.org',
                    autograder.api.config.PARAM_USER_PASS.config_key: 'server-admin',

                    autograder.api.config.PARAM_TARGET_EMAIL.config_key: 'ZZZ@test.edulinq.org',
                },
                {},
                {
                    "found-user": False,
                },
                None,
            ),

            # Bad Permissions
            (
                {
                    autograder.api.config.PARAM_USER_EMAIL.config_key: 'course-owner@test.edulinq.org',
                    autograder.api.config.PARAM_USER_PASS.config_key: 'course-owner',

                    autograder.api.config.PARAM_TARGET_EMAIL_OR_SELF.config_key: 'course-student@test.edulinq.org',
                },
                {
                    'exit_on_error': False,
                },
                None,
                'You have insufficient permissions',
            ),
        ]

        self.base_api_test(autograder.api.users.remove.send, test_cases)
