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
                autograder.testing.model.COURSES['course101'],
                None,
            ),
            (
                {
                    autograder.api.config.PARAM_COURSE.config_key: 'course-languages',
                    autograder.api.config.PARAM_USER_EMAIL.config_key: 'server-admin@test.edulinq.org',
                    autograder.api.config.PARAM_USER_PASS.config_key: 'server-admin',
                },
                {},
                autograder.testing.model.COURSES['course-languages'],
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

        self.base_api_test(autograder.api.courses.get.send, test_cases)
