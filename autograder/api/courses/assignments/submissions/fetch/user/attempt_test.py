import sys
import unittest

import edq.util.dirent

import autograder.api.config
import autograder.api.courses.assignments.submissions.fetch.testing
import autograder.api.courses.assignments.submissions.fetch.user.attempt
import autograder.testing.server
import autograder.util.submission

class TestCourseAssignmentsFetchUserAttempt(autograder.testing.server.ServerTest):
    """ Test fetching user submission attempt. """

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
                    autograder.api.courses.assignments.submissions.fetch.testing.SUBMISSIONS['course-student@test.edulinq.org'][2],
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

        self.base_api_test(autograder.api.courses.assignments.submissions.fetch.user.attempt.send, test_cases)

    @unittest.skipIf(sys.platform.startswith("win"), "Windows file hashes create different HTTP exchange queries")
    def test_write_output(self):
        """ Ensure that the attempt is properly written to a directory. """

        submission = autograder.api.courses.assignments.submissions.fetch.testing.SUBMISSIONS['course-student@test.edulinq.org'][2]

        temp_dir = edq.util.dirent.get_temp_dir('autograder-testing-')
        autograder.util.submission.output_grading_result(submission, base_dir = temp_dir)

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
