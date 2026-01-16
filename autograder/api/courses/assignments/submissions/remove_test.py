import autograder.api.config
import autograder.api.courses.assignments.submissions.remove
import autograder.testing.server

class TestCourseAssignmentsRemove(autograder.testing.server.ServerTest):
    """ Test removing a user submission. """

    def test_base(self):
        """ Test base functionality. """

        # [(config (and overrides), kwargs, expected, error substring), ...]
        test_cases = [
            # Base
            (
                {
                    autograder.api.config.PARAM_USER_EMAIL.config_key: 'server-admin@test.edulinq.org',
                    autograder.api.config.PARAM_USER_PASS.config_key: 'server-admin',
                    autograder.api.config.PARAM_COURSE.config_key: 'course101',
                    autograder.api.config.PARAM_ASSIGNMENT.config_key: 'hw0',
                    autograder.api.config.PARAM_TARGET_EMAIL_OR_SELF.config_key: 'course-student@test.edulinq.org',
                },
                {},
                (
                    True,
                    True,
                ),
                None,
            ),

            # Missing User
            (
                {
                    autograder.api.config.PARAM_USER_EMAIL.config_key: 'server-admin@test.edulinq.org',
                    autograder.api.config.PARAM_USER_PASS.config_key: 'server-admin',
                    autograder.api.config.PARAM_COURSE.config_key: 'course101',
                    autograder.api.config.PARAM_ASSIGNMENT.config_key: 'hw0',
                    autograder.api.config.PARAM_TARGET_EMAIL_OR_SELF.config_key: 'ZZZ@test.edulinq.org',
                },
                {},
                (
                    False,
                    False,
                ),
                None,
            ),

            # Missing Submission
            (
                {
                    autograder.api.config.PARAM_USER_EMAIL.config_key: 'server-admin@test.edulinq.org',
                    autograder.api.config.PARAM_USER_PASS.config_key: 'server-admin',
                    autograder.api.config.PARAM_COURSE.config_key: 'course101',
                    autograder.api.config.PARAM_ASSIGNMENT.config_key: 'hw0',
                    autograder.api.config.PARAM_TARGET_EMAIL_OR_SELF.config_key: 'course-student@test.edulinq.org',
                    autograder.api.config.PARAM_TARGET_SUBMISSION_OR_RECENT.config_key: 'ZZZ',
                },
                {},
                (
                    True,
                    False,
                ),
                None,
            ),

            # No Submissions (Self)
            (
                {
                    autograder.api.config.PARAM_USER_EMAIL.config_key: 'server-admin@test.edulinq.org',
                    autograder.api.config.PARAM_USER_PASS.config_key: 'server-admin',
                    autograder.api.config.PARAM_COURSE.config_key: 'course101',
                    autograder.api.config.PARAM_ASSIGNMENT.config_key: 'hw0',
                },
                {},
                (
                    True,
                    False,
                ),
                None,
            ),
        ]

        self.base_api_test(autograder.api.courses.assignments.submissions.remove.send, test_cases)
