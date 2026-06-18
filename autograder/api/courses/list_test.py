import typing

import autograder.api.config
import autograder.api.courses.list
import autograder.model.config
import autograder.testing.model
import autograder.testing.server

class TestCoursesList(autograder.testing.server.ServerTest):
    """ Test listing courses. """

    def test_base(self) -> None:
        """ Test base functionality. """

        # [(config (and overrides), kwargs, expected, error substring), ...]
        test_cases: typing.List[typing.Tuple[
            autograder.model.config.Config,
            typing.Dict[str, typing.Any],
            typing.Any,
            typing.Union[str, None],
        ]] = [
            (
                autograder.model.config.Config(
                    auth_user = 'server-admin@test.edulinq.org',
                    auth_pass = 'server-admin',
                ),
                {},
                autograder.testing.model.COURSES_LIST,
                None,
            ),
        ]

        self.base_api_test(autograder.api.courses.list.send, test_cases)
