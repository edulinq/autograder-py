import autograder.api.config
import autograder.api.courses.users.drop
import autograder.testing.server

class TestUsersDrop(autograder.testing.server.ServerTest):
    """ Test dropping course users. """

    def test_base(self):
        """ Test base functionality. """

        # [(config (and overrides), kwargs, expected, error substring), ...]
        test_cases = [
            # Enrolled User
            (
                {
                    autograder.api.config.PARAM_COURSE.config_key: 'course101',
                    autograder.api.config.PARAM_USER_EMAIL.config_key: 'server-admin@test.edulinq.org',
                    autograder.api.config.PARAM_USER_PASS.config_key: 'server-admin',

                    autograder.api.config.PARAM_TARGET_EMAIL.config_key: 'course-student@test.edulinq.org',
                },
                {},
                {
                    "found-user": True,
                },
                None,
            ),

            # Non-Enrolled User
            (
                {
                    autograder.api.config.PARAM_COURSE.config_key: 'course101',
                    autograder.api.config.PARAM_USER_EMAIL.config_key: 'server-admin@test.edulinq.org',
                    autograder.api.config.PARAM_USER_PASS.config_key: 'server-admin',

                    autograder.api.config.PARAM_TARGET_EMAIL.config_key: 'server-user@test.edulinq.org',
                },
                {},
                {
                    "found-user": False,
                },
                None,
            ),

            # Unknown User
            (
                {
                    autograder.api.config.PARAM_COURSE.config_key: 'course101',
                    autograder.api.config.PARAM_USER_EMAIL.config_key: 'server-admin@test.edulinq.org',
                    autograder.api.config.PARAM_USER_PASS.config_key: 'server-admin',

                    autograder.api.config.PARAM_TARGET_EMAIL.config_key: 'ZZZ@test.edulinq.org',
                },
                {},
                {
                    "found-user": False,
                },
                None,
            ),
        ]

        self.base_api_test(autograder.api.courses.users.drop.send, test_cases)
