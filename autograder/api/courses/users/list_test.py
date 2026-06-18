import typing

import autograder.api.config
import autograder.api.courses.users.list
import autograder.model.config
import autograder.testing.model
import autograder.testing.server

class TestUsersList(autograder.testing.server.ServerTest):
    """ Test listing course users. """

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
                    course = 'course101',
                    auth_user = 'server-admin@test.edulinq.org',
                    auth_pass = 'server-admin',
                ),
                {},
                sorted(autograder.testing.model.COURSE_USERS['Course 101'].values()),
                None,
            ),
            (
                autograder.model.config.Config(
                    course = 'course101',
                    auth_user = 'course-admin@test.edulinq.org',
                    auth_pass = 'course-admin',
                ),
                {},
                sorted(autograder.testing.model.COURSE_USERS['Course 101'].values()),
                None,
            ),
            (
                autograder.model.config.Config(
                    course = 'course101',
                    auth_user = 'course-grader@test.edulinq.org',
                    auth_pass = 'course-grader',
                ),
                {},
                sorted(autograder.testing.model.COURSE_USERS['Course 101'].values()),
                None,
            ),
        ]

        self.base_api_test(autograder.api.courses.users.list.send, test_cases)
