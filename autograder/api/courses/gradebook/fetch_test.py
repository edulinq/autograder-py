import typing

import edq.util.crypto

import autograder.api.config
import autograder.api.courses.gradebook.fetch
import autograder.model.config
import autograder.testing.server

class TestCoursesGradebookFetch(autograder.testing.server.ServerTest):
    """ Test fetching a course gradebook. """

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
                    auth_user = 'course-grader@test.edulinq.org',
                    auth_pass = edq.util.crypto.Secret('course-grader'),

                    course = 'course101',

                ),
                {},
                {},
                None,
            ),
        ]

        self.base_api_test(autograder.api.courses.gradebook.fetch.send, test_cases)
