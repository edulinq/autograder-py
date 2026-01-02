import autograder.api.config
import autograder.api.courses.users.enroll
import autograder.testing.server

class TestUsersEnroll(autograder.testing.server.ServerTest):
    """ Test getting course users. """

    def test_base(self):
        """ Test base functionality. """

        # [(config (and overrides), kwargs, expected, error substring), ...]
        test_cases = [
            # Enroll Only
            (
                {
                    autograder.api.config.PARAM_COURSE.config_key: 'course101',
                    autograder.api.config.PARAM_USER_EMAIL.config_key: 'server-admin@test.edulinq.org',
                    autograder.api.config.PARAM_USER_PASS.config_key: 'server-admin',

                    autograder.api.config.PARAM_DRY_RUN.config_key: False,
                    autograder.api.config.PARAM_SKIP_INSERTS.config_key: False,
                    autograder.api.config.PARAM_SKIP_UPDATES.config_key: False,
                    autograder.api.config.PARAM_SEND_EMAILS.config_key: False,

                    autograder.api.config.PARAM_RAW_COURSE_USERS.config_key: [
                        {
                            'email': 'server-user@test.edulinq.org',
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
                        }
                    ]
                },
                None,
            ),

            # Add and Enroll
            (
                {
                    autograder.api.config.PARAM_COURSE.config_key: 'course101',
                    autograder.api.config.PARAM_USER_EMAIL.config_key: 'server-admin@test.edulinq.org',
                    autograder.api.config.PARAM_USER_PASS.config_key: 'server-admin',

                    autograder.api.config.PARAM_DRY_RUN.config_key: False,
                    autograder.api.config.PARAM_SKIP_INSERTS.config_key: False,
                    autograder.api.config.PARAM_SKIP_UPDATES.config_key: False,
                    autograder.api.config.PARAM_SEND_EMAILS.config_key: False,

                    autograder.api.config.PARAM_RAW_COURSE_USERS.config_key: [
                        {
                            'email': 'ZZZ@test.edulinq.org',
                            'course-role': 'student',
                        },
                    ],
                },
                {},
                {
                    "results": [
                        {
                            "added": True,
                            "email": "ZZZ@test.edulinq.org",
                            "enrolled": [
                                "course101",
                            ],
                        }
                    ]
                },
                None,
            ),

            # Multiple: Mixed
            (
                {
                    autograder.api.config.PARAM_COURSE.config_key: 'course101',
                    autograder.api.config.PARAM_USER_EMAIL.config_key: 'server-admin@test.edulinq.org',
                    autograder.api.config.PARAM_USER_PASS.config_key: 'server-admin',

                    autograder.api.config.PARAM_DRY_RUN.config_key: False,
                    autograder.api.config.PARAM_SKIP_INSERTS.config_key: False,
                    autograder.api.config.PARAM_SKIP_UPDATES.config_key: False,
                    autograder.api.config.PARAM_SEND_EMAILS.config_key: False,

                    autograder.api.config.PARAM_RAW_COURSE_USERS.config_key: [
                        {
                            'email': 'server-user@test.edulinq.org',
                            'course-role': 'student',
                        },
                        {
                            'email': 'ZZZ@test.edulinq.org',
                            'course-role': 'student',
                        },
                    ],
                },
                {},
                {
                    "results": [
                        {
                            "added": True,
                            "email": "ZZZ@test.edulinq.org",
                            "enrolled": [
                                "course101",
                            ],
                        },
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
        ]

        self.base_api_test(autograder.api.courses.users.enroll.send, test_cases)
