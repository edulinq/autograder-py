import autograder.api.config
import autograder.api.courses.users.get
import autograder.model.user
import autograder.testing.model
import autograder.testing.server

class TestUsersGet(autograder.testing.server.ServerTest):
    """ Test getting course users. """

    def test_base(self):
        """ Test base functionality. """

        # [(config (and overrides), kwargs, expected, error substring), ...]
        test_cases = [
            # Base - Other
            (
                {
                    autograder.api.config.PARAM_COURSE.config_key: 'course101',
                    autograder.api.config.PARAM_USER_EMAIL.config_key: 'course-grader@test.edulinq.org',
                    autograder.api.config.PARAM_USER_PASS.config_key: 'course-grader',
                    autograder.api.config.PARAM_TARGET_EMAIL_OR_SELF.config_key: 'course-student@test.edulinq.org',
                },
                {},
                autograder.testing.model.COURSE_USERS['Course 101']['course-student'],
                None,
            ),

            # Base - Self (Admin)
            (
                {
                    autograder.api.config.PARAM_COURSE.config_key: 'course101',
                    autograder.api.config.PARAM_USER_EMAIL.config_key: 'course-grader@test.edulinq.org',
                    autograder.api.config.PARAM_USER_PASS.config_key: 'course-grader',
                },
                {},
                autograder.testing.model.COURSE_USERS['Course 101']['course-grader'],
                None,
            ),

            # Base - Self (Non-Admin)
            (
                {
                    autograder.api.config.PARAM_COURSE.config_key: 'course101',
                    autograder.api.config.PARAM_USER_EMAIL.config_key: 'course-student@test.edulinq.org',
                    autograder.api.config.PARAM_USER_PASS.config_key: 'course-student',
                },
                {},
                autograder.testing.model.COURSE_USERS['Course 101']['course-student'],
                None,
            ),

            # Missing
            (
                {
                    autograder.api.config.PARAM_COURSE.config_key: 'course101',
                    autograder.api.config.PARAM_USER_EMAIL.config_key: 'course-grader@test.edulinq.org',
                    autograder.api.config.PARAM_USER_PASS.config_key: 'course-grader',
                    autograder.api.config.PARAM_TARGET_EMAIL_OR_SELF.config_key: 'server-user@test.edulinq.org',
                },
                {},
                None,
                None,
            ),

            # Bad Permissions
            (
                {
                    autograder.api.config.PARAM_COURSE.config_key: 'course101',
                    autograder.api.config.PARAM_USER_EMAIL.config_key: 'course-other@test.edulinq.org',
                    autograder.api.config.PARAM_USER_PASS.config_key: 'course-other',
                    autograder.api.config.PARAM_TARGET_EMAIL_OR_SELF.config_key: 'course-student@test.edulinq.org',
                },
                {
                    'exit_on_error': False,
                },
                None,
                'You have insufficient permissions',
            ),

            # User Promotion
            (
                {
                    autograder.api.config.PARAM_COURSE.config_key: 'course101',
                    autograder.api.config.PARAM_USER_EMAIL.config_key: 'server-admin@test.edulinq.org',
                    autograder.api.config.PARAM_USER_PASS.config_key: 'server-admin',
                },
                {},
                autograder.model.user.promote_server_user(autograder.testing.model.SERVER_USERS['server-admin']),
                None,
            ),
        ]

        self.base_api_test(autograder.api.courses.users.get.send, test_cases)
