import autograder.api.config
import autograder.api.courses.get
import autograder.testing.model
import autograder.testing.server

class TestCoursesGet(autograder.testing.server.ServerTest):
    """ Test getting courses. """

    def test_base(self):
        """ Test base functionality. """

        # [(config (and overrides), kwargs, expected, error substring), ...]
        test_cases = [
            # Base
            (
                {
                    autograder.api.config.PARAM_COURSE.config_key: 'course101',
                    autograder.api.config.PARAM_USER_EMAIL.config_key: 'server-admin@test.edulinq.org',
                    autograder.api.config.PARAM_USER_PASS.config_key: 'server-admin',
                },
                {},
                autograder.testing.model.COURSES['Course 101'],
                None,
            ),
            (
                {
                    autograder.api.config.PARAM_COURSE.config_key: 'course-languages',
                    autograder.api.config.PARAM_USER_EMAIL.config_key: 'server-admin@test.edulinq.org',
                    autograder.api.config.PARAM_USER_PASS.config_key: 'server-admin',
                },
                {},
                autograder.testing.model.COURSES['Course Using Different Languages'],
                None,
            ),

            # Missing
            (
                {
                    autograder.api.config.PARAM_COURSE.config_key: 'ZZZ',
                    autograder.api.config.PARAM_USER_EMAIL.config_key: 'server-admin@test.edulinq.org',
                    autograder.api.config.PARAM_USER_PASS.config_key: 'server-admin',
                },
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
                    {
                        autograder.api.config.PARAM_COURSE.config_key: autograder.testing.model.COURSES[course_name].id,
                        autograder.api.config.PARAM_USER_EMAIL.config_key: user.email,
                        autograder.api.config.PARAM_USER_PASS.config_key: user.name,
                    },
                    {},
                    autograder.testing.model.COURSES[course_name],
                    None,
                ))

        self.base_api_test(autograder.api.courses.get.send, test_cases)
