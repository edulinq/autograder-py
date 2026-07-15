import typing

import edq.util.crypto

import autograder.api.config
import autograder.api.courses.assignments.submissions.fetch.user.peek
import autograder.model.config
import autograder.testing.server

class TestCourseAssignmentsFetchUserPeek(autograder.testing.server.ServerTest):
    """ Test fetching user submission peek. """

    def test_base(self) -> None:
        """ Test base functionality. """

        # [(config (and overrides), kwargs, expected, error substring), ...]
        test_cases: typing.List[typing.Tuple[
            autograder.model.config.Config,
            typing.Dict[str, typing.Any],
            typing.Any,
            typing.Union[str, None],
        ]] = [
            # Base
            (
                autograder.model.config.Config(
                    auth_user = 'server-admin@test.edulinq.org',
                    auth_pass = edq.util.crypto.Secret('server-admin'),
                    course = 'course101',
                    assignment = 'hw0',
                    target_email = 'course-student@test.edulinq.org',
                ),
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
                autograder.model.config.Config(
                    auth_user = 'server-admin@test.edulinq.org',
                    auth_pass = edq.util.crypto.Secret('server-admin'),
                    course = 'course101',
                    assignment = 'hw0',
                    target_email = 'ZZZ@test.edulinq.org',
                ),
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
                autograder.model.config.Config(
                    auth_user = 'server-admin@test.edulinq.org',
                    auth_pass = edq.util.crypto.Secret('server-admin'),
                    course = 'course101',
                    assignment = 'hw0',
                    target_email = 'course-student@test.edulinq.org',
                    target_submission = 'ZZZ',
                ),
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
                autograder.model.config.Config(
                    auth_user = 'server-admin@test.edulinq.org',
                    auth_pass = edq.util.crypto.Secret('server-admin'),
                    course = 'course101',
                    assignment = 'hw0',
                ),
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
