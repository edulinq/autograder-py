import typing

import lms.model.scores

import autograder.api.config
import autograder.api.courses.assignments.submissions.fetch.user.history
import autograder.testing.server

class TestCourseAssignmentsFetchUserHistory(autograder.testing.server.ServerTest):
    """ Test fetching user submission history. """

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
                    SCORES,
                ),
                None,
            ),

            # No History, Self
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
                    [],
                ),
                None,
            ),

            # No User
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
                    [],
                ),
                None,
            ),
        ]

        self.base_api_test(autograder.api.courses.assignments.submissions.fetch.user.history.send, test_cases)

SCORES: typing.List[lms.model.scores.AssignmentScore] = [
    lms.model.scores.AssignmentScore(
        assignment = 'hw0',
        comment = '',
        graded_date = 1697406256000,
        id = 'course101::hw0::course-student@test.edulinq.org::1697406256',
        score = 0,
        submission_date = 1697406256000,
        user = 'course-student@test.edulinq.org',
    ),
    lms.model.scores.AssignmentScore(
        assignment = 'hw0',
        comment = '',
        graded_date = 1697406266000,
        id = 'course101::hw0::course-student@test.edulinq.org::1697406265',
        score = 1,
        submission_date = 1697406266000,
        user = 'course-student@test.edulinq.org',
    ),
    lms.model.scores.AssignmentScore(
        assignment = 'hw0',
        comment = '',
        graded_date = 1697406273000,
        id = 'course101::hw0::course-student@test.edulinq.org::1697406272',
        score = 2,
        submission_date = 1697406273000,
        user = 'course-student@test.edulinq.org',
    ),
]
