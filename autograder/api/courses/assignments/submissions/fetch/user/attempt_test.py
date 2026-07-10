import sys
import typing
import unittest

import edq.util.crypto
import edq.util.dirent

import autograder.api.config
import autograder.api.courses.assignments.submissions.fetch.testing
import autograder.api.courses.assignments.submissions.fetch.user.attempt
import autograder.model.config
import autograder.testing.server
import autograder.util.grading

class TestCourseAssignmentsFetchUserAttempt(autograder.testing.server.ServerTest):
    """ Test fetching user submission attempt. """

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
                    autograder.api.courses.assignments.submissions.fetch.testing.SUBMISSIONS['course-student@test.edulinq.org'][2],
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
            (
                autograder.model.config.Config(
                    auth_user = 'course-admin@test.edulinq.org',
                    auth_pass = edq.util.crypto.Secret('course-admin'),
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

            # Target Submissions
            (
                autograder.model.config.Config(
                    auth_user = 'course-admin@test.edulinq.org',
                    auth_pass = edq.util.crypto.Secret('course-admin'),
                    course = 'course101',
                    assignment = 'hw0',
                    target_email = 'course-student@test.edulinq.org',
                    target_submission = '1697406265',
                ),
                {},
                (
                    True,
                    True,
                    autograder.api.courses.assignments.submissions.fetch.testing.SUBMISSIONS['course-student@test.edulinq.org'][1],
                ),
                None,
            ),
        ]

        self.base_api_test(autograder.api.courses.assignments.submissions.fetch.user.attempt.send, test_cases)

    @unittest.skipIf(sys.platform.startswith("win"), "Windows file hashes create different HTTP exchange queries")
    def test_write_output(self) -> None:
        """ Ensure that the attempt is properly written to a directory. """

        submission = autograder.api.courses.assignments.submissions.fetch.testing.SUBMISSIONS['course-student@test.edulinq.org'][2]

        temp_dir = edq.util.dirent.get_temp_dir('autograder-testing-')
        autograder.util.grading.output_grading_result(submission, base_dir = temp_dir)

        expected = {
            "autograder-testing": {
                "course101::hw0::course-student@test.edulinq.org::1697406272": {
                    "info.json": "8e82f4f1d0ab94630f33ec228e309e8095358900c358736b86bd2aef4bbba454",
                    "input": {
                        "submission.py": "0556802ad831fa40d1ab3d5bfd21e59887b9f4caf29dfd46d5357755cf51ab25"
                    },
                    "output": {
                        "result.json": "64a907f42bfe209830b6204a9cf8ea97a2e1e24661dd7dd1f89bd2a808b7e154"
                    },
                    "stderr.txt": "01ba4719c80b6fe911b091a7c05124b64eeece964e09c058ef8f9805daca546b",
                    "stdout.txt": "87864e5833cd38179a7d146f2dce1395a4b83234e7be96d379cb7f37c4ef8645"
                }
            }
        }

        actual = edq.util.dirent.tree(temp_dir, hash_files = True)

        # Normalize the top-level key.
        key = list(actual.keys())[0]
        actual['autograder-testing'] = actual.pop(key)

        self.assertJSONEqual(expected, actual)
