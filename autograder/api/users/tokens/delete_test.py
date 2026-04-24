import autograder.api.config
import autograder.api.users.tokens.delete
import autograder.testing.model
import autograder.testing.server

class TestUsersTokensDelete(autograder.testing.server.ServerTest):
    """ Test deleting tokens. """

    def test_base(self):
        """ Test base functionality. """

        # [(config (and overrides), kwargs, expected, error substring), ...]
        test_cases = [
            # Self - Base
            (
                {
                    autograder.api.config.PARAM_USER_EMAIL.config_key: 'course-admin@test.edulinq.org',
                    autograder.api.config.PARAM_USER_PASS.config_key: 'course-admin',
                    autograder.api.config.PARAM_TOKEN_ID.config_key: 'df0a1f16-9cd8-4395-8509-10ae314fe6fc',
                },
                {},
                {
                    "found-user": True,
                    "found-token": True,
                },
                None,
            ),

            # Self - Bad ID
            (
                {
                    autograder.api.config.PARAM_USER_EMAIL.config_key: 'course-admin@test.edulinq.org',
                    autograder.api.config.PARAM_USER_PASS.config_key: 'course-admin',
                    autograder.api.config.PARAM_TOKEN_ID.config_key: 'ZZZ',
                },
                {},
                {
                    "found-user": True,
                    "found-token": False,
                },
                None,
            ),

            # Other - Base
            (
                {
                    autograder.api.config.PARAM_USER_EMAIL.config_key: 'server-admin@test.edulinq.org',
                    autograder.api.config.PARAM_USER_PASS.config_key: 'server-admin',
                    autograder.api.config.PARAM_TARGET_USER_OR_SELF.config_key: 'course-student@test.edulinq.org',
                    autograder.api.config.PARAM_TOKEN_ID.config_key: 'dddbc97c-36e4-43fc-b5a0-478aade61c53',
                },
                {},
                {
                    "found-user": True,
                    "found-token": True,
                },
                None,
            ),

            # Other - Bad Permissions
            (
                {
                    autograder.api.config.PARAM_USER_EMAIL.config_key: 'course-admin@test.edulinq.org',
                    autograder.api.config.PARAM_USER_PASS.config_key: 'course-admin',
                    autograder.api.config.PARAM_TARGET_USER_OR_SELF.config_key: 'course-student@test.edulinq.org',
                    autograder.api.config.PARAM_TOKEN_ID.config_key: 'dddbc97c-36e4-43fc-b5a0-478aade61c53',
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
                    autograder.api.config.PARAM_TOKEN_ID.config_key: 'dddbc97c-36e4-43fc-b5a0-478aade61c53',
                },
                {},
                {
                    "found-user": False,
                    "found-token": False,
                },
                None,
            ),

            # Other - Missing Token
            (
                {
                    autograder.api.config.PARAM_USER_EMAIL.config_key: 'server-admin@test.edulinq.org',
                    autograder.api.config.PARAM_USER_PASS.config_key: 'server-admin',
                    autograder.api.config.PARAM_TARGET_USER_OR_SELF.config_key: 'course-student@test.edulinq.org',
                    autograder.api.config.PARAM_TOKEN_ID.config_key: 'ZZZ',
                },
                {},
                {
                    "found-user": True,
                    "found-token": False,
                },
                None,
            ),
        ]

        # Add a test case for each user, this helps others using the generated test data.
        for user in autograder.testing.model.RAW_USER_DATA.values():
            test_cases.append((
                {
                    autograder.api.config.PARAM_USER_EMAIL.config_key: user['email'],
                    autograder.api.config.PARAM_USER_PASS.config_key: user['name'],
                    autograder.api.config.PARAM_TOKEN_ID.config_key: user['tokens'][0]['id'],
                },
                {},
                {
                    "found-user": True,
                    "found-token": True,
                },
                None,
            ))

        self.base_api_test(autograder.api.users.tokens.delete.send, test_cases)
