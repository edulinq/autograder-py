import typing

import edq.util.crypto

import autograder.api.users.upsert
import autograder.testing.server

class TestUsersUpsert(autograder.testing.server.ServerTest):
    """ Test upserting server users. """

    def test_base(self) -> None:
        """ Test base functionality. """

        # [(config (and overrides), kwargs, expected, error substring), ...]
        test_cases: typing.List[typing.Tuple[
            autograder.model.config.Config,
            typing.Dict[str, typing.Any],
            typing.Any,
            typing.Union[str, None],
        ]] = [
            # Insert
            (
                autograder.model.config.Config(
                    auth_user = 'server-admin@test.edulinq.org',
                    auth_pass = edq.util.crypto.Secret('server-admin'),

                    dry_run = False,
                    skip_inserts = False,
                    skip_updates = False,
                    send_emails = False,

                    raw_server_users = [
                        {
                            'email': 'new-user@test.edulinq.org',
                            'role': 'user',
                        },
                    ],
                ),
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
                autograder.model.config.Config(
                    auth_user = 'server-admin@test.edulinq.org',
                    auth_pass = edq.util.crypto.Secret('server-admin'),

                    dry_run = False,
                    skip_inserts = False,
                    skip_updates = False,
                    send_emails = False,

                    raw_server_users = [
                        {
                            'email': 'server-admin@test.edulinq.org',
                            'name': 'New Name',
                        },
                    ],
                ),
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
                autograder.model.config.Config(
                    auth_user = 'server-admin@test.edulinq.org',
                    auth_pass = edq.util.crypto.Secret('server-admin'),

                    dry_run = False,
                    skip_inserts = False,
                    skip_updates = False,
                    send_emails = False,

                    raw_server_users = [
                        {
                            'email': 'server-user@test.edulinq.org',
                            'course': 'course101',
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
                        },
                    ]
                },
                None,
            ),

            # Mixed
            (
                autograder.model.config.Config(
                    auth_user = 'server-admin@test.edulinq.org',
                    auth_pass = edq.util.crypto.Secret('server-admin'),

                    dry_run = False,
                    skip_inserts = False,
                    skip_updates = False,
                    send_emails = False,

                    raw_server_users = [
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
                ),
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
