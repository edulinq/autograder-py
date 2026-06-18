import typing

import autograder.api.config
import autograder.api.courses.users.enroll
import autograder.model.config
import autograder.testing.server

class TestUsersEnroll(autograder.testing.server.ServerTest):
    """ Test enrolling course users. """

    def test_base(self) -> None:
        """ Test base functionality. """

        # [(config (and overrides), kwargs, expected, error substring), ...]
        test_cases: typing.List[typing.Tuple[
            autograder.model.config.Config,
            typing.Dict[str, typing.Any],
            typing.Any,
            typing.Union[str, None],
        ]] = [
            # Enroll Only
            (
                autograder.model.config.Config(
                    course = 'course101',
                    auth_user = 'server-admin@test.edulinq.org',
                    auth_pass = 'server-admin',

                    dry_run = False,
                    skip_inserts = False,
                    skip_updates = False,
                    send_emails = False,

                    raw_course_users = [
                        {
                            'email': 'server-user@test.edulinq.org',
                            'course-role': 'student',
                        },
                    ],
                ),
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
                autograder.model.config.Config(
                    course = 'course101',
                    auth_user = 'server-admin@test.edulinq.org',
                    auth_pass = 'server-admin',

                    dry_run = False,
                    skip_inserts = False,
                    skip_updates = False,
                    send_emails = False,

                    raw_course_users = [
                        {
                            'email': 'ZZZ@test.edulinq.org',
                            'course-role': 'student',
                        },
                    ],
                ),
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
                autograder.model.config.Config(
                    course = 'course101',
                    auth_user = 'server-admin@test.edulinq.org',
                    auth_pass = 'server-admin',

                    dry_run = False,
                    skip_inserts = False,
                    skip_updates = False,
                    send_emails = False,

                    raw_course_users = [
                        {
                            'email': 'server-user@test.edulinq.org',
                            'course-role': 'student',
                        },
                        {
                            'email': 'ZZZ@test.edulinq.org',
                            'course-role': 'student',
                        },
                    ],
                ),
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
