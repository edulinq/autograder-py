import typing

import autograder.api.config
import autograder.api.courses.get
import autograder.model.config
import autograder.testing.model
import autograder.testing.server

class TestCoursesGet(autograder.testing.server.ServerTest):
    """ Test getting courses. """

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
                    course = 'course101',
                    auth_user = 'server-admin@test.edulinq.org',
                    auth_pass = 'server-admin',
                ),
                {},
                autograder.testing.model.COURSES['Course 101'],
                None,
            ),
            (
                autograder.model.config.Config(
                    course = 'course-languages',
                    auth_user = 'server-admin@test.edulinq.org',
                    auth_pass = 'server-admin',
                ),
                {},
                autograder.testing.model.COURSES['Course Using Different Languages'],
                None,
            ),

            # Missing
            (
                autograder.model.config.Config(
                    course = 'ZZZ',
                    auth_user = 'server-admin@test.edulinq.org',
                    auth_pass = 'server-admin',
                ),
                {},
                None,
                'Could not find course',
            ),
        ]

        # Add a get for each user of each course (this helps users of the test data).
        for (course_name, users) in autograder.testing.model.COURSE_USERS.items():
            if (course_name == 'Extra Course'):
                continue

            for user in users.values():
                test_cases.append((
                    autograder.model.config.Config(
                        course = autograder.testing.model.COURSES[course_name].id,
                        auth_user = user.email,
                        auth_pass = user.name,
                    ),
                    {},
                    autograder.testing.model.COURSES[course_name],
                    None,
                ))

        self.base_api_test(autograder.api.courses.get.send, test_cases)
