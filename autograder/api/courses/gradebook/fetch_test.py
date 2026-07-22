import typing

import edq.util.crypto
import edq.util.time
import lms.model.assignments
import lms.model.scores
import lms.model.users

import autograder.api.config
import autograder.api.courses.gradebook.fetch
import autograder.model.config
import autograder.testing.server

class TestCoursesGradebookFetch(autograder.testing.server.ServerTest):
    """ Test fetching a course gradebook. """

    def test_base(self) -> None:
        """ Test base functionality. """

        # [(config (and overrides), kwargs, expected, error substring), ...]
        test_cases: typing.List[typing.Tuple[
            autograder.model.config.Config,
            typing.Dict[str, typing.Any],
            typing.Any,
            typing.Union[str, None],
        ]] = [
            # Full Gradebook
            (
                autograder.model.config.Config(
                    auth_user = 'course-grader@test.edulinq.org',
                    auth_pass = edq.util.crypto.Secret('course-grader'),
                    course = 'course-languages',
                ),
                {},
                BASE_GRADEBOOK,
                None,
            ),

            # Filtered Gradebook
            (
                autograder.model.config.Config(
                    auth_user = 'course-grader@test.edulinq.org',
                    auth_pass = edq.util.crypto.Secret('course-grader'),
                    course = 'course-languages',
                    target_users = ['student'],
                    target_assignments = ['cpp', 'java'],
                ),
                {},
                FILTERED_GRADEBOOK,
                None,
            ),
        ]

        self.base_api_test(autograder.api.courses.gradebook.fetch.send, test_cases)

BASE_GRADEBOOK: lms.model.scores.Gradebook = lms.model.scores.Gradebook(
    [
        lms.model.assignments.AssignmentQuery(id = 'bash'),
        lms.model.assignments.AssignmentQuery(id = 'cpp'),
        lms.model.assignments.AssignmentQuery(id = 'java'),
    ],
    [
        lms.model.users.UserQuery(id = 'course-admin@test.edulinq.org'),
        lms.model.users.UserQuery(id = 'course-grader@test.edulinq.org'),
        lms.model.users.UserQuery(id = 'course-other@test.edulinq.org'),
        lms.model.users.UserQuery(id = 'course-owner@test.edulinq.org'),
        lms.model.users.UserQuery(id = 'course-student@test.edulinq.org'),
    ],
)

BASE_GRADEBOOK.add(lms.model.scores.AssignmentScore(
    assignment = lms.model.assignments.AssignmentQuery(id = 'bash'),
    user = lms.model.users.UserQuery(id = 'course-student@test.edulinq.org'),
    id = 'course-languages::bash::course-student@test.edulinq.org::1768603685',
    score = 10,
    comment = '',
    graded_date = edq.util.time.Timestamp(1768603685040),
    submission_date = edq.util.time.Timestamp(1768603685040),
))

FILTERED_GRADEBOOK: lms.model.scores.Gradebook = lms.model.scores.Gradebook(
    [
        lms.model.assignments.AssignmentQuery(id = 'cpp'),
        lms.model.assignments.AssignmentQuery(id = 'java'),
    ],
    [
        lms.model.users.UserQuery(id = 'course-student@test.edulinq.org'),
    ],
)
