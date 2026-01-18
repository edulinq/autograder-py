import autograder.api.config
import autograder.api.courses.assignments.submissions.fetch.user.peek
import autograder.testing.server

class TestCourseAssignmentsFetchUserPeek(autograder.testing.server.ServerTest):
    """ Test fetching user submission peek. """

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
                    SUBMISSION,
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
                    None,
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
                    None,
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
                    None,
                ),
                None,
            ),
        ]

        self.base_api_test(autograder.api.courses.assignments.submissions.fetch.user.peek.send, test_cases)

SUBMISSION: autograder.assignment.GradedAssignment = autograder.assignment.GradedAssignment.from_dict({
    "id": "course101::hw0::course-student@test.edulinq.org::1697406272",
    "short-id": "1697406272",
    "course-id": "course101",
    "assignment-id": "hw0",
    "user": "course-student@test.edulinq.org",
    "message": "",
    "max_points": 2,
    "score": 2,
    "name": "HW0",
    "questions": [
        {
            "name": "Q1",
            "max_points": 1,
            "score": 1,
            "hard_fail": False,
            "skipped": False,
            "message": "",
            "grading_start_time": 1697406273000,
            "grading_end_time": 1697406273000
        },
        {
            "name": "Q2",
            "max_points": 1,
            "score": 1,
            "hard_fail": False,
            "skipped": False,
            "message": "",
            "grading_start_time": 1697406273000,
            "grading_end_time": 1697406273000
        }
    ],
    "grading_start_time": 1697406273000,
    "grading_end_time": 1697406273000,
    "additional-info": None,
})
