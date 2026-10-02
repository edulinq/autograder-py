import typing

import edq.util.crypto

import autograder.api.courses.status.list
import autograder.model.config
import autograder.testing.asserts
import autograder.testing.constants
import autograder.testing.server

class TestCoursesStatusList(autograder.testing.server.ServerTest):
    """ Test listing course statuses. """

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
                    auth_user = 'course-other@test.edulinq.org',
                    auth_pass = edq.util.crypto.Secret('course-other'),
                    course = 'course101',
                ),
                {},
                {
                    "statuses": {
                        "course-admin@test.edulinq.org": {
                            "active": True,
                            "owner": "course-admin@test.edulinq.org",
                            "set-time": autograder.testing.constants.TEST_TIMESTAMP,
                            "source": "course"
                        }
                    }
                },
                None,
            ),

            # Course Without Statuses
            (
                autograder.model.config.Config(
                    auth_user = 'course-other@test.edulinq.org',
                    auth_pass = edq.util.crypto.Secret('course-other'),
                    course = 'course-languages',
                ),
                {},
                {
                    "statuses": {}
                },
                None,
            )
        ]

        self.base_api_test(autograder.api.courses.status.list.send, test_cases, actual_clean_func = autograder.testing.asserts.normalize_dict)
