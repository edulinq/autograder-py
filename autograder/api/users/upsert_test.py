import autograder.api.config
import autograder.api.users.upsert
import autograder.testing.server

class TestUsersUpsert(autograder.testing.server.ServerTest):
    """ Test upserting server users. """

    def test_base(self):
        """ Test base functionality. """

        # [(config (and overrides), kwargs, expected, error substring), ...]
        test_cases = [
            # Insert
            (
                {
                    autograder.api.config.PARAM_USER_EMAIL.config_key: 'server-admin@test.edulinq.org',
                    autograder.api.config.PARAM_USER_PASS.config_key: 'server-admin',

                    autograder.api.config.PARAM_DRY_RUN.config_key: False,
                    autograder.api.config.PARAM_SKIP_INSERTS.config_key: False,
                    autograder.api.config.PARAM_SKIP_UPDATES.config_key: False,
                    autograder.api.config.PARAM_SEND_EMAILS.config_key: False,

                    autograder.api.config.PARAM_RAW_SERVER_USERS.config_key: [
                        {
                            'email': 'new-user@test.edulinq.org',
                            'role': 'user',
                        },
                    ],
                },
                {},
                {
                    "results": [
                        {
                            "added": True,
                            "email": "new-user@test.edulinq.org",
                        },
                    ]
                },
                None,
            ),

            # Update
            (
                {
                    autograder.api.config.PARAM_USER_EMAIL.config_key: 'server-admin@test.edulinq.org',
                    autograder.api.config.PARAM_USER_PASS.config_key: 'server-admin',

                    autograder.api.config.PARAM_DRY_RUN.config_key: False,
                    autograder.api.config.PARAM_SKIP_INSERTS.config_key: False,
                    autograder.api.config.PARAM_SKIP_UPDATES.config_key: False,
                    autograder.api.config.PARAM_SEND_EMAILS.config_key: False,

                    autograder.api.config.PARAM_RAW_SERVER_USERS.config_key: [
                        {
                            'email': 'server-admin@test.edulinq.org',
                            'name': 'New Name',
                        },
                    ],
                },
                {},
                {
                    "results": [
                        {
                            "email": "server-admin@test.edulinq.org",
                            "modified": True,
                        },
                    ]
                },
                None,
            ),

            # Enroll
            (
                {
                    autograder.api.config.PARAM_USER_EMAIL.config_key: 'server-admin@test.edulinq.org',
                    autograder.api.config.PARAM_USER_PASS.config_key: 'server-admin',

                    autograder.api.config.PARAM_DRY_RUN.config_key: False,
                    autograder.api.config.PARAM_SKIP_INSERTS.config_key: False,
                    autograder.api.config.PARAM_SKIP_UPDATES.config_key: False,
                    autograder.api.config.PARAM_SEND_EMAILS.config_key: False,

                    autograder.api.config.PARAM_RAW_SERVER_USERS.config_key: [
                        {
                            'email': 'server-user@test.edulinq.org',
                            'course': 'course101',
                            'course-role': 'student',
                        },
                    ],
                },
                {},
                {
                    "results": [
                        {
                            "email": "server-user@test.edulinq.org",
                            "enrolled": [
                                "course101",
                            ],
                            "modified": True,
                        },
                    ]
                },
                None,
            ),

            # Mixed
            (
                {
                    autograder.api.config.PARAM_USER_EMAIL.config_key: 'server-admin@test.edulinq.org',
                    autograder.api.config.PARAM_USER_PASS.config_key: 'server-admin',

                    autograder.api.config.PARAM_DRY_RUN.config_key: False,
                    autograder.api.config.PARAM_SKIP_INSERTS.config_key: False,
                    autograder.api.config.PARAM_SKIP_UPDATES.config_key: False,
                    autograder.api.config.PARAM_SEND_EMAILS.config_key: False,

                    autograder.api.config.PARAM_RAW_SERVER_USERS.config_key: [
                        {
                            'email': 'new-user@test.edulinq.org',
                            'pass': 'password123',
                            'role': 'user',
                        },
                        {
                            'email': 'server-admin@test.edulinq.org',
                            'name': 'New Name',
                        },
                    ],
                },
                {},
                {
                    "results": [
                        {
                            "added": True,
                            "email": "new-user@test.edulinq.org",
                        },
                        {
                            "email": "server-admin@test.edulinq.org",
                            "modified": True,
                        },
                    ]
                },
                None,
            ),


        ]

        self.base_api_test(autograder.api.users.upsert.send, test_cases)
