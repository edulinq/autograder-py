import typing

import edq.util.crypto

import autograder.api.config
import autograder.api.courses.stats.query
import autograder.model.config
import autograder.testing.server

class TestCoursesStatsQuery(autograder.testing.server.ServerTest):
    """ Test query course stats. """

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

                    course = 'course101',

                    query_metric_type = 'grading-time',
                ),
                {},
                {
                    "results": [],
                },
                None,
            ),

        ]

        self.base_api_test(autograder.api.courses.stats.query.send, test_cases)
