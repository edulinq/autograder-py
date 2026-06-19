import typing

import edq.util.crypto

import autograder.api.config
import autograder.api.logs.query
import autograder.testing.model
import autograder.testing.server

class TestLogsQuery(autograder.testing.server.ServerTest):
    """ Test query server logs. """

    def test_base(self) -> None:
        """ Test base functionality. """

        # [(config (and overrides), kwargs, expected, error substring), ...]
        test_cases: typing.List[typing.Tuple[
            autograder.model.config.Config,
            typing.Dict[str, typing.Any],
            typing.Any,
            typing.Union[str, None],
        ]] = [
            # Base
            (
                autograder.model.config.Config(
                    auth_user = 'server-admin@test.edulinq.org',
                    auth_pass = edq.util.crypto.Secret('server-admin'),

                    query_use_testing_data = False,

                    query_level = 'ERROR',
                    query_after = None,
                    query_past = None,
                    query_target_course = None,
                    query_target_assignment = None,
                    query_target_email = None,
                ),
                {},
                (
                    None,
                    [],
                ),
                None,
            ),

            # Testing Logs
            (
                autograder.model.config.Config(
                    auth_user = 'server-admin@test.edulinq.org',
                    auth_pass = edq.util.crypto.Secret('server-admin'),

                    query_use_testing_data = True,

                    query_level = 'TRACE',
                    query_after = None,
                    query_past = None,
                    query_target_course = None,
                    query_target_assignment = None,
                    query_target_email = None,
                ),
                {},
                (
                    None,
                    autograder.testing.model.PARSED_LOGS,
                ),
                None,
            ),

            # Bad Permissions
            (
                autograder.model.config.Config(
                    auth_user = 'server-user@test.edulinq.org',
                    auth_pass = edq.util.crypto.Secret('server-user'),

                    query_use_testing_data = False,

                    query_level = 'ERROR',
                    query_after = None,
                    query_past = None,
                    query_target_course = "course101",
                    query_target_assignment = None,
                    query_target_email = None,
                ),
                {},
                (
                    "Error: 'You do not have the correct permissions to execute this log query.', Locator: ''.",
                    [],
                ),
                None,
            ),
        ]

        self.base_api_test(autograder.api.logs.query.send, test_cases)
