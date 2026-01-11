import typing

import lms.model.scores

import autograder.api.config
import autograder.api.courses.assignments.submissions.fetch.course.scores
import autograder.testing.model
import autograder.testing.server

class TestCourseAssignmentsFetchCourseScores(autograder.testing.server.ServerTest):
    """ Test fetching course scores. """

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
                FULL_SCORES,
                None,
            ),

            # Query
            (
                {
                    autograder.api.config.PARAM_USER_EMAIL.config_key: 'server-admin@test.edulinq.org',
                    autograder.api.config.PARAM_USER_PASS.config_key: 'server-admin',
                    autograder.api.config.PARAM_COURSE.config_key: 'course101',
                    autograder.api.config.PARAM_ASSIGNMENT.config_key: 'hw0',
                    autograder.api.config.PARAM_COURSE_USER_REFERENCES.config_key: [
                        'student',
                    ],
                },
                {},
                [STUDENT_SCORE],
                None,
            ),

            # Query (Empty)
            (
                {
                    autograder.api.config.PARAM_USER_EMAIL.config_key: 'server-admin@test.edulinq.org',
                    autograder.api.config.PARAM_USER_PASS.config_key: 'server-admin',
                    autograder.api.config.PARAM_COURSE.config_key: 'course101',
                    autograder.api.config.PARAM_ASSIGNMENT.config_key: 'hw0',
                    autograder.api.config.PARAM_COURSE_USER_REFERENCES.config_key: [
                        'ZZZ@test.edulinq.org',
                    ],
                },
                {},
                [],
                None,
            ),
        ]

        self.base_api_test(autograder.api.courses.assignments.submissions.fetch.course.scores.send, test_cases)

STUDENT_SCORE: lms.model.scores.AssignmentScore = lms.model.scores.AssignmentScore(
    assignment_query = 'hw0',
    comment = '',
    graded_date = 1697406273000,
    id = 'course101::hw0::course-student@test.edulinq.org::1697406272',
    score = 2,
    submission_date = 1697406273000,
    user_query = 'course-student@test.edulinq.org',
)

FULL_SCORES: typing.List[lms.model.scores.AssignmentScore] = [
    lms.model.scores.AssignmentScore(assignment_query = 'hw0', user_query = 'course-admin@test.edulinq.org'),
    lms.model.scores.AssignmentScore(assignment_query = 'hw0', user_query = 'course-grader@test.edulinq.org'),
    lms.model.scores.AssignmentScore(assignment_query = 'hw0', user_query = 'course-other@test.edulinq.org'),
    lms.model.scores.AssignmentScore(assignment_query = 'hw0', user_query = 'course-owner@test.edulinq.org'),
    STUDENT_SCORE,
]
