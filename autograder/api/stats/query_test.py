import autograder.api.config
import autograder.api.stats.query
import autograder.model.stats
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

                    autograder.api.config.PARAM_QUERY_USE_TESTING_DATA.config_key: False,

                    autograder.api.config.PARAM_QUERY_METRIC_TYPE.config_key: 'grading-time',
                    autograder.api.config.PARAM_QUERY_LIMIT.config_key: None,
                    autograder.api.config.PARAM_QUERY_AFTER.config_key: None,
                    autograder.api.config.PARAM_QUERY_BEFORE.config_key: None,
                    autograder.api.config.PARAM_QUERY_SORT.config_key: None,
                    autograder.api.config.PARAM_QUERY_WHERE.config_key: None,
                },
                {},
                [],
                None,
            ),

            # Testing Data - Single
            (
                {
                    autograder.api.config.PARAM_USER_EMAIL.config_key: 'server-admin@test.edulinq.org',
                    autograder.api.config.PARAM_USER_PASS.config_key: 'server-admin',

                    autograder.api.config.PARAM_QUERY_USE_TESTING_DATA.config_key: True,

                    autograder.api.config.PARAM_QUERY_METRIC_TYPE.config_key: 'grading-time',
                    autograder.api.config.PARAM_QUERY_LIMIT.config_key: None,
                    autograder.api.config.PARAM_QUERY_AFTER.config_key: None,
                    autograder.api.config.PARAM_QUERY_BEFORE.config_key: None,
                    autograder.api.config.PARAM_QUERY_SORT.config_key: None,
                    autograder.api.config.PARAM_QUERY_WHERE.config_key: None,
                },
                {},
                [
                    autograder.model.stats.Metric.from_api({
                        "attributes": {
                            "assignment": "hw0",
                            "course": "course101",
                            "user": "course-student@test.edulinq.org"
                        },
                        "timestamp": 1200,
                        "type": "grading-time",
                        "value": 150
                    }),
                ],
                None,
            ),

            # Testing Data - Multiple
            (
                {
                    autograder.api.config.PARAM_USER_EMAIL.config_key: 'server-admin@test.edulinq.org',
                    autograder.api.config.PARAM_USER_PASS.config_key: 'server-admin',

                    autograder.api.config.PARAM_QUERY_USE_TESTING_DATA.config_key: True,

                    autograder.api.config.PARAM_QUERY_METRIC_TYPE.config_key: 'cpu-usage',
                    autograder.api.config.PARAM_QUERY_LIMIT.config_key: None,
                    autograder.api.config.PARAM_QUERY_AFTER.config_key: None,
                    autograder.api.config.PARAM_QUERY_BEFORE.config_key: None,
                    autograder.api.config.PARAM_QUERY_SORT.config_key: None,
                    autograder.api.config.PARAM_QUERY_WHERE.config_key: None,
                },
                {},
                [
                    autograder.model.stats.Metric.from_api({
                        "timestamp": 1800,
                        "type": "cpu-usage",
                        "value": 5
                    }),
                    autograder.model.stats.Metric.from_api({
                        "timestamp": 2200,
                        "type": "cpu-usage",
                        "value": 10
                    }),
                ],
                None,
            ),

            # Parse Timestamp - Int
            (
                {
                    autograder.api.config.PARAM_USER_EMAIL.config_key: 'server-admin@test.edulinq.org',
                    autograder.api.config.PARAM_USER_PASS.config_key: 'server-admin',

                    autograder.api.config.PARAM_QUERY_USE_TESTING_DATA.config_key: False,

                    autograder.api.config.PARAM_QUERY_METRIC_TYPE.config_key: 'grading-time',
                    autograder.api.config.PARAM_QUERY_LIMIT.config_key: None,
                    autograder.api.config.PARAM_QUERY_AFTER.config_key: 123,
                    autograder.api.config.PARAM_QUERY_BEFORE.config_key: None,
                    autograder.api.config.PARAM_QUERY_SORT.config_key: None,
                    autograder.api.config.PARAM_QUERY_WHERE.config_key: None,
                },
                {},
                [],
                None,
            ),

            # Parse Timestamp - String Int
            (
                {
                    autograder.api.config.PARAM_USER_EMAIL.config_key: 'server-admin@test.edulinq.org',
                    autograder.api.config.PARAM_USER_PASS.config_key: 'server-admin',

                    autograder.api.config.PARAM_QUERY_USE_TESTING_DATA.config_key: False,

                    autograder.api.config.PARAM_QUERY_METRIC_TYPE.config_key: 'grading-time',
                    autograder.api.config.PARAM_QUERY_LIMIT.config_key: None,
                    autograder.api.config.PARAM_QUERY_AFTER.config_key: '123',
                    autograder.api.config.PARAM_QUERY_BEFORE.config_key: None,
                    autograder.api.config.PARAM_QUERY_SORT.config_key: None,
                    autograder.api.config.PARAM_QUERY_WHERE.config_key: None,
                },
                {},
                [],
                None,
            ),

            # Parse Timestamp - String
            (
                {
                    autograder.api.config.PARAM_USER_EMAIL.config_key: 'server-admin@test.edulinq.org',
                    autograder.api.config.PARAM_USER_PASS.config_key: 'server-admin',

                    autograder.api.config.PARAM_QUERY_USE_TESTING_DATA.config_key: False,

                    autograder.api.config.PARAM_QUERY_METRIC_TYPE.config_key: 'grading-time',
                    autograder.api.config.PARAM_QUERY_LIMIT.config_key: None,
                    autograder.api.config.PARAM_QUERY_AFTER.config_key: '2023-09-28T04:00:20Z',
                    autograder.api.config.PARAM_QUERY_BEFORE.config_key: None,
                    autograder.api.config.PARAM_QUERY_SORT.config_key: None,
                    autograder.api.config.PARAM_QUERY_WHERE.config_key: None,
                },
                {},
                [],
                None,
            ),
        ]

        self.base_api_test(autograder.api.stats.query.send, test_cases)
