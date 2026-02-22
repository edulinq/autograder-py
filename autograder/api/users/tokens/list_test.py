import autograder.api.config
import autograder.api.users.tokens.list
import autograder.testing.asserts
import autograder.testing.server

class TestUsersTokensList(autograder.testing.server.ServerTest):
    """ Test creating tokens. """

    def test_base(self):
        """ Test base functionality. """

        # [(config (and overrides), kwargs, expected, error substring), ...]
        test_cases = [
            # Self
            (
                {
                    autograder.api.config.PARAM_USER_EMAIL.config_key: 'server-user@test.edulinq.org',
                    autograder.api.config.PARAM_USER_PASS.config_key: 'server-user',
                },
                {},
                {
                    "found-user": True,
                    "tokens": [
                        {
                            "access-time": autograder.testing.constants.TEST_TIMESTAMP,
                            "creation-time": autograder.testing.constants.TEST_TIMESTAMP,
                            "id": autograder.testing.constants.TEST_TOKEN_ID,
                            "name": "test",
                            "source": "user"
                        },
                    ]
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
                    "tokens": [
                        {
                            "access-time": autograder.testing.constants.TEST_TIMESTAMP,
                            "creation-time": autograder.testing.constants.TEST_TIMESTAMP,
                            "id": autograder.testing.constants.TEST_TOKEN_ID,
                            "name": "test",
                            "source": "user"
                        },
                    ]
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
                    "tokens": None,
                },
                None,
            ),
        ]

        self.base_api_test(autograder.api.users.tokens.list.send, test_cases, actual_clean_func = autograder.testing.asserts.normalize_dict)
