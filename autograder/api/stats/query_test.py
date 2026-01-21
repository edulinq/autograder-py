import autograder.api.config
import autograder.api.stats.query
import autograder.testing.server

class TestStatsQuery(autograder.testing.server.ServerTest):
    """ Test query server stats. """

    def test_base(self):
        """ Test base functionality. """

        # [(config (and overrides), kwargs, expected, error substring), ...]
        test_cases = [
            # Base
            (
                {
                    autograder.api.config.PARAM_USER_EMAIL.config_key: 'server-admin@test.edulinq.org',
                    autograder.api.config.PARAM_USER_PASS.config_key: 'server-admin',

                    autograder.api.config.PARAM_QUERY_METRIC_TYPE.config_key: 'grading-time',
                    autograder.api.config.PARAM_QUERY_LIMIT.config_key: None,
                    autograder.api.config.PARAM_QUERY_AFTER.config_key: None,
                    autograder.api.config.PARAM_QUERY_BEFORE.config_key: None,
                    autograder.api.config.PARAM_QUERY_SORT.config_key: None,
                    autograder.api.config.PARAM_QUERY_WHERE.config_key: None,
                },
                {},
                {
                    "results": [],
                },
                None,
            ),

            # Parse Timestamp - Int
            (
                {
                    autograder.api.config.PARAM_USER_EMAIL.config_key: 'server-admin@test.edulinq.org',
                    autograder.api.config.PARAM_USER_PASS.config_key: 'server-admin',

                    autograder.api.config.PARAM_QUERY_METRIC_TYPE.config_key: 'grading-time',
                    autograder.api.config.PARAM_QUERY_LIMIT.config_key: None,
                    autograder.api.config.PARAM_QUERY_AFTER.config_key: 123,
                    autograder.api.config.PARAM_QUERY_BEFORE.config_key: None,
                    autograder.api.config.PARAM_QUERY_SORT.config_key: None,
                    autograder.api.config.PARAM_QUERY_WHERE.config_key: None,
                },
                {},
                {
                    "results": [],
                },
                None,
            ),

            # Parse Timestamp - String Int
            (
                {
                    autograder.api.config.PARAM_USER_EMAIL.config_key: 'server-admin@test.edulinq.org',
                    autograder.api.config.PARAM_USER_PASS.config_key: 'server-admin',

                    autograder.api.config.PARAM_QUERY_METRIC_TYPE.config_key: 'grading-time',
                    autograder.api.config.PARAM_QUERY_LIMIT.config_key: None,
                    autograder.api.config.PARAM_QUERY_AFTER.config_key: '123',
                    autograder.api.config.PARAM_QUERY_BEFORE.config_key: None,
                    autograder.api.config.PARAM_QUERY_SORT.config_key: None,
                    autograder.api.config.PARAM_QUERY_WHERE.config_key: None,
                },
                {},
                {
                    "results": [],
                },
                None,
            ),

            # Parse Timestamp - String
            (
                {
                    autograder.api.config.PARAM_USER_EMAIL.config_key: 'server-admin@test.edulinq.org',
                    autograder.api.config.PARAM_USER_PASS.config_key: 'server-admin',

                    autograder.api.config.PARAM_QUERY_METRIC_TYPE.config_key: 'grading-time',
                    autograder.api.config.PARAM_QUERY_LIMIT.config_key: None,
                    autograder.api.config.PARAM_QUERY_AFTER.config_key: '2023-09-28T04:00:20Z',
                    autograder.api.config.PARAM_QUERY_BEFORE.config_key: None,
                    autograder.api.config.PARAM_QUERY_SORT.config_key: None,
                    autograder.api.config.PARAM_QUERY_WHERE.config_key: None,
                },
                {},
                {
                    "results": [],
                },
                None,
            ),
        ]

        self.base_api_test(autograder.api.stats.query.send, test_cases)
