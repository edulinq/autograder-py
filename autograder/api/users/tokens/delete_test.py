import typing

import edq.util.crypto

import autograder.api.config
import autograder.api.users.tokens.delete
import autograder.testing.model
import autograder.testing.server

class TestUsersTokensDelete(autograder.testing.server.ServerTest):
    """ Test deleting tokens. """

    def test_base(self) -> None:
        """ Test base functionality. """

        # [(config (and overrides), kwargs, expected, error substring), ...]
        test_cases: typing.List[typing.Tuple[
            autograder.model.config.Config,
            typing.Dict[str, typing.Any],
            typing.Any,
            typing.Union[str, None],
        ]] = [
            # Self - Base
            (
                autograder.model.config.Config(
                    auth_user = 'course-admin@test.edulinq.org',
                    auth_pass = edq.util.crypto.Secret('course-admin'),
                    token_id = 'df0a1f16-9cd8-4395-8509-10ae314fe6fc',
                ),
                {},
                {
                    "found-user": True,
                    "found-token": True,
                },
                None,
            ),

            # Self - Bad ID
            (
                autograder.model.config.Config(
                    auth_user = 'course-admin@test.edulinq.org',
                    auth_pass = edq.util.crypto.Secret('course-admin'),
                    token_id = 'ZZZ',
                ),
                {},
                {
                    "found-user": True,
                    "found-token": False,
                },
                None,
            ),

            # Other - Base
            (
                autograder.model.config.Config(
                    auth_user = 'server-admin@test.edulinq.org',
                    auth_pass = edq.util.crypto.Secret('server-admin'),
                    target_user = 'course-student@test.edulinq.org',
                    token_id = 'dddbc97c-36e4-43fc-b5a0-478aade61c53',
                ),
                {},
                {
                    "found-user": True,
                    "found-token": True,
                },
                None,
            ),

            # Other - Bad Permissions
            (
                autograder.model.config.Config(
                    auth_user = 'course-admin@test.edulinq.org',
                    auth_pass = edq.util.crypto.Secret('course-admin'),
                    target_user = 'course-student@test.edulinq.org',
                    token_id = 'dddbc97c-36e4-43fc-b5a0-478aade61c53',
                ),
                {},
                None,
                "You have insufficient permissions for the requested operation",
            ),

            # Other - Missing User
            (
                autograder.model.config.Config(
                    auth_user = 'server-admin@test.edulinq.org',
                    auth_pass = edq.util.crypto.Secret('server-admin'),
                    target_user = 'ZZZ@test.edulinq.org',
                    token_id = 'dddbc97c-36e4-43fc-b5a0-478aade61c53',
                ),
                {},
                {
                    "found-user": False,
                    "found-token": False,
                },
                None,
            ),

            # Other - Missing Token
            (
                autograder.model.config.Config(
                    auth_user = 'server-admin@test.edulinq.org',
                    auth_pass = edq.util.crypto.Secret('server-admin'),
                    target_user = 'course-student@test.edulinq.org',
                    token_id = 'ZZZ',
                ),
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
                autograder.model.config.Config(
                    auth_user = user['email'],
                    auth_pass = user['name'],
                    token_id = user['tokens'][0]['id'],
                ),
                {},
                {
                    "found-user": True,
                    "found-token": True,
                },
                None,
            ))

        self.base_api_test(autograder.api.users.tokens.delete.send, test_cases)
