import autograder.api.config
import autograder.api.courses.list
import autograder.testing.model
import autograder.testing.server

class TestCoursesList(autograder.testing.server.ServerTest):
    """ Test listing courses. """

    def test_base(self):
        """ Test base functionality. """

        # [(config (and overrides), kwargs, expected, error substring), ...]
        test_cases = [
            (
                {
                    autograder.api.config.PARAM_USER_EMAIL.config_key: 'server-admin@test.edulinq.org',
                    autograder.api.config.PARAM_USER_PASS.config_key: 'server-admin',
                },
                {},
                autograder.testing.model.COURSES_LIST,
                None,
            ),
        ]

        self.base_api_test(autograder.api.courses.list.send, test_cases)
