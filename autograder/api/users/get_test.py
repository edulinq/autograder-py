import typing

import autograder.api.users.get
import autograder.model.user
import autograder.testing.model
import autograder.testing.server

class TestUsersGet(autograder.testing.server.ServerTest):
    """ Test getting server users. """

    def test_base(self) -> None:
        """ Test base functionality. """

        # [(config (and overrides), kwargs, expected, error substring), ...]
        test_cases: typing.List[typing.Tuple[
            autograder.model.config.Config,
            typing.Dict[str, typing.Any],
            typing.Any,
            typing.Union[str, None],
        ]] = [
            # Base - Other
            (
                autograder.model.config.Config(
                    auth_user = 'server-admin@test.edulinq.org',
                    auth_pass = 'server-admin',
                    target_email = 'course-student@test.edulinq.org',
                ),
                {},
                autograder.testing.model.SERVER_USERS['course-student'],
                None,
            ),

            # Base - Self
            (
                autograder.model.config.Config(
                    auth_user = 'server-admin@test.edulinq.org',
                    auth_pass = 'server-admin',
                ),
                {},
                autograder.testing.model.SERVER_USERS['server-admin'],
                None,
            ),

            # Missing
            (
                autograder.model.config.Config(
                    auth_user = 'server-admin@test.edulinq.org',
                    auth_pass = 'server-admin',
                    target_email = 'ZZZ@test.edulinq.org',
                ),
                {},
                None,
                None,
            ),

            # Bad Permissions
            (
                autograder.model.config.Config(
                    auth_user = 'course-admin@test.edulinq.org',
                    auth_pass = 'course-admin',
                    target_email = 'course-student@test.edulinq.org',
                ),
                {
                    'exit_on_error': False,
                },
                None,
                'You have insufficient permissions',
            ),
        ]

        # Add a test case for each user, this helps others using the generated test data.
        for user in autograder.testing.model.SERVER_USERS.values():
            test_cases.append((
                autograder.model.config.Config(
                    auth_user = user.email,
                    auth_pass = user.name,
                ),
                {},
                user,
                None,
            ))

        self.base_api_test(autograder.api.users.get.send, test_cases)
