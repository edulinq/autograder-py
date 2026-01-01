import autograder.api.config
import autograder.api.courses.users.list
import autograder.testing.model
import autograder.testing.server

class TestUsersList(autograder.testing.server.ServerTest):
    """ Test getting course users. """

    def test_base(self):
        """ Test base functionality. """

        # [(config (and overrides), kwargs, expected, error substring), ...]
        test_cases = [
            (
                {
                    autograder.api.config.PARAM_COURSE.config_key: 'course101',
                    autograder.api.config.PARAM_USER_EMAIL.config_key: 'server-admin@test.edulinq.org',
                    autograder.api.config.PARAM_USER_PASS.config_key: 'server-admin',
                },
                {},
                sorted(autograder.testing.model.COURSE_USERS['Course 101'].values()),
                None,
            ),
            (
                {
                    autograder.api.config.PARAM_COURSE.config_key: 'course101',
                    autograder.api.config.PARAM_USER_EMAIL.config_key: 'course-grader@test.edulinq.org',
                    autograder.api.config.PARAM_USER_PASS.config_key: 'course-grader',
                },
                {},
                sorted(autograder.testing.model.COURSE_USERS['Course 101'].values()),
                None,
            ),
        ]

        self.base_api_test(autograder.api.courses.users.list.send, test_cases)
