import autograder.api.config
import autograder.api.courses.assignments.submissions.fetch.course.attempts
import autograder.api.courses.assignments.submissions.fetch.user.attempt_test
import autograder.testing.server

class TestCourseAssignmentsFetchCourseAttempts(autograder.testing.server.ServerTest):
    """ Test fetching course submission attempts. """

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
                },
                {},
                {
                    "course-admin@test.edulinq.org": None,
                    "course-grader@test.edulinq.org": None,
                    "course-other@test.edulinq.org": None,
                    "course-owner@test.edulinq.org": None,
                    "course-student@test.edulinq.org": autograder.api.courses.assignments.submissions.fetch.user.attempt_test.SUBMISSION,
                },
                None,
            ),

            # Reference
            (
                {
                    autograder.api.config.PARAM_USER_EMAIL.config_key: 'server-admin@test.edulinq.org',
                    autograder.api.config.PARAM_USER_PASS.config_key: 'server-admin',
                    autograder.api.config.PARAM_COURSE.config_key: 'course101',
                    autograder.api.config.PARAM_ASSIGNMENT.config_key: 'hw0',
                    autograder.api.config.PARAM_COURSE_USER_REFERENCES.config_key: [
                        'course-admin@test.edulinq.org',
                        'course-student@test.edulinq.org',
                    ],
                },
                {},
                {
                    "course-admin@test.edulinq.org": None,
                    "course-student@test.edulinq.org": autograder.api.courses.assignments.submissions.fetch.user.attempt_test.SUBMISSION,
                },
                None,
            ),
        ]

        self.base_api_test(autograder.api.courses.assignments.submissions.fetch.course.attempts.send, test_cases)
