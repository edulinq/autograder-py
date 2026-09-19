import typing

import edq.util.crypto

import autograder.api.courses.status.set
import autograder.model.config
import autograder.testing.constants
import autograder.testing.server

class TestCoursesStatusSet(autograder.testing.server.ServerTest):
    """ Test setting a course status. """

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
                    auth_user = 'course-admin@test.edulinq.org',
                    auth_pass = edq.util.crypto.Secret('course-admin'),
                    course = 'course101',
                    active = True,
                ),
                {},
                {
                    "status": {
                        "active": True,
                        "owner": "course-admin@test.edulinq.org",
                        "set-time": autograder.testing.constants.TEST_TIMESTAMP,
                        "source": "course",
                    },
                },
                None,
            ),
        ]

        self.base_api_test(autograder.api.courses.status.set.send, test_cases)
