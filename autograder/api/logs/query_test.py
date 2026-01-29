import autograder.api.config
import autograder.api.logs.query
import autograder.testing.model
import autograder.testing.server

class TestLogsQuery(autograder.testing.server.ServerTest):
    """ Test query server logs. """

    def test_base(self):
        """ Test base functionality. """

        # [(config (and overrides), kwargs, expected, error substring), ...]
        test_cases = [
            # Base
            (
                {
                    autograder.api.config.PARAM_USER_EMAIL.config_key: 'server-admin@test.edulinq.org',
                    autograder.api.config.PARAM_USER_PASS.config_key: 'server-admin',

                    autograder.api.config.PARAM_QUERY_USE_TESTING_DATA.config_key: False,

                    autograder.api.config.PARAM_QUERY_LOG_LEVEL.config_key: 'ERROR',
                    autograder.api.config.PARAM_QUERY_AFTER.config_key: None,
                    autograder.api.config.PARAM_QUERY_PAST.config_key: None,
                    autograder.api.config.PARAM_QUERY_TARGET_COURSE.config_key: None,
                    autograder.api.config.PARAM_QUERY_TARGET_ASSIGNMENT.config_key: None,
                    autograder.api.config.PARAM_QUERY_TARGET_EMAIL.config_key: None,
                },
                {},
                (
                    None,
                    [],
                ),
                None,
            ),

            # Testing Logs
            (
                {
                    autograder.api.config.PARAM_USER_EMAIL.config_key: 'server-admin@test.edulinq.org',
                    autograder.api.config.PARAM_USER_PASS.config_key: 'server-admin',

                    autograder.api.config.PARAM_QUERY_USE_TESTING_DATA.config_key: True,

                    autograder.api.config.PARAM_QUERY_LOG_LEVEL.config_key: 'TRACE',
                    autograder.api.config.PARAM_QUERY_AFTER.config_key: None,
                    autograder.api.config.PARAM_QUERY_PAST.config_key: None,
                    autograder.api.config.PARAM_QUERY_TARGET_COURSE.config_key: None,
                    autograder.api.config.PARAM_QUERY_TARGET_ASSIGNMENT.config_key: None,
                    autograder.api.config.PARAM_QUERY_TARGET_EMAIL.config_key: None,
                },
                {},
                (
                    None,
                    autograder.testing.model.PARSED_LOGS,
                ),
                None,
            ),

            # Bad Permissions
            (
                {
                    autograder.api.config.PARAM_USER_EMAIL.config_key: 'server-user@test.edulinq.org',
                    autograder.api.config.PARAM_USER_PASS.config_key: 'server-user',

                    autograder.api.config.PARAM_QUERY_USE_TESTING_DATA.config_key: False,

                    autograder.api.config.PARAM_QUERY_LOG_LEVEL.config_key: 'ERROR',
                    autograder.api.config.PARAM_QUERY_AFTER.config_key: None,
                    autograder.api.config.PARAM_QUERY_PAST.config_key: None,
                    autograder.api.config.PARAM_QUERY_TARGET_COURSE.config_key: "course101",
                    autograder.api.config.PARAM_QUERY_TARGET_ASSIGNMENT.config_key: None,
                    autograder.api.config.PARAM_QUERY_TARGET_EMAIL.config_key: None,
                },
                {},
                (
                    "Error: 'You do not have the correct permissions to execute this log query.', Locator: ''.",
                    [],
                ),
                None,
            ),
        ]

        self.base_api_test(autograder.api.logs.query.send, test_cases)
