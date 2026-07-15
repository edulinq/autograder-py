import typing

import edq.util.crypto
import edq.util.time

import autograder.api.config
import autograder.api.stats.query
import autograder.model.config
import autograder.model.stats
import autograder.testing.server

class TestStatsQuery(autograder.testing.server.ServerTest):
    """ Test query server stats. """

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

                    query_metric_type = 'grading-time',
                ),
                {},
                [],
                None,
            ),

            # Testing Data - Single
            (
                autograder.model.config.Config(
                    auth_user = 'server-admin@test.edulinq.org',
                    auth_pass = edq.util.crypto.Secret('server-admin'),

                    query_use_testing_data = True,

                    query_metric_type = 'grading-time',
                ),
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
                autograder.model.config.Config(
                    auth_user = 'server-admin@test.edulinq.org',
                    auth_pass = edq.util.crypto.Secret('server-admin'),

                    query_use_testing_data = True,

                    query_metric_type = 'cpu-usage',
                ),
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
                autograder.model.config.Config(
                    auth_user = 'server-admin@test.edulinq.org',
                    auth_pass = edq.util.crypto.Secret('server-admin'),

                    query_use_testing_data = False,

                    query_metric_type = 'grading-time',
                    query_after = edq.util.time.Timestamp.guess(123),
                ),
                {},
                [],
                None,
            ),

            # Parse Timestamp - String Int
            (
                autograder.model.config.Config(
                    auth_user = 'server-admin@test.edulinq.org',
                    auth_pass = edq.util.crypto.Secret('server-admin'),

                    query_use_testing_data = False,

                    query_metric_type = 'grading-time',
                    query_after = edq.util.time.Timestamp.guess('123'),
                ),
                {},
                [],
                None,
            ),

            # Parse Timestamp - String
            (
                autograder.model.config.Config(
                    auth_user = 'server-admin@test.edulinq.org',
                    auth_pass = edq.util.crypto.Secret('server-admin'),

                    query_use_testing_data = False,

                    query_metric_type = 'grading-time',
                    query_after = edq.util.time.Timestamp.guess('2023-09-28T04:00:20Z'),
                ),
                {},
                [],
                None,
            ),
        ]

        self.base_api_test(autograder.api.stats.query.send, test_cases)
