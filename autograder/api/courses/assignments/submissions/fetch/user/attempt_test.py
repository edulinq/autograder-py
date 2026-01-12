import sys
import typing

import edq.util.dirent

import autograder.api.config
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

        self.base_api_test(autograder.api.courses.assignments.submissions.fetch.user.attempt.send, test_cases)

    def test_write_output(self):
        """ Ensure that the attempt is properly written to a directory. """

        temp_dir = edq.util.dirent.get_temp_dir('autograder-testing-')
        autograder.util.submission.output_grading_result(SUBMISSION, base_dir = temp_dir)

        expected = {
            "autograder-testing": {
                "course101::hw0::course-student@test.edulinq.org::1697406272": {
                    "info.json": "0acd6cd5eea896d61999e02c3d3e793a6469d147b72599c9d93b15e9d200b4b6",
                    "input": {
                        "submission.py": "0556802ad831fa40d1ab3d5bfd21e59887b9f4caf29dfd46d5357755cf51ab25"
                    },
                    "output": {
                        "result.json": "3e763894ef9ec385e80887d4fd3398c11d1d31d02b28258d0b674e384298b731"
                    },
                    "stderr.txt": "01ba4719c80b6fe911b091a7c05124b64eeece964e09c058ef8f9805daca546b",
                    "stdout.txt": "cb2815272d73a630f099b902301f5a098485b42c1a639c9b3be138ae2e589e54"
                }
            }
        }

        # Windows will have different hashes.
        if (sys.platform == 'win32'):
            expected = {
                "autograder-testing": {
                    "course101__hw0__course-student@test.edulinq.org__1697406272": {
                        "info.json": "93f23186058de5439da828b3510552cfbdfe3626397d024dc249300734a08c60",
                        "input": {
                            "submission.py": "0556802ad831fa40d1ab3d5bfd21e59887b9f4caf29dfd46d5357755cf51ab25"
                        },
                        "output": {
                            "result.json": "3e763894ef9ec385e80887d4fd3398c11d1d31d02b28258d0b674e384298b731"
                        },
                        "stderr.txt": "7eb70257593da06f682a3ddda54a9d260d4fc514f645237f5ca74b08f8da61a6",
                        "stdout.txt": "836491292efe503863b01b0ead71a3418a8364ef62bc1fdc7408671005b294f2"
                    }
                }
            }

        actual = edq.util.dirent.tree(temp_dir, hash_files = True)

        # Normalize the top-level key.
        key = list(actual.keys())[0]
        actual['autograder-testing'] = actual.pop(key)

        self.assertJSONEqual(expected, actual)

# pylint: disable=line-too-long
SUBMISSION: typing.Dict[str, typing.Any] = {
    "info": {
        "additional-info": None,
        "assignment-id": "hw0",
        "course-id": "course101",
        "grading_end_time": 1697406273000,
        "grading_start_time": 1697406273000,
        "id": "course101::hw0::course-student@test.edulinq.org::1697406272",
        "max_points": 2,
        "message": "",
        "name": "HW0",
        "questions": [
            {
                "grading_end_time": 1697406273000,
                "grading_start_time": 1697406273000,
                "hard_fail": False,
                "max_points": 1,
                "message": "",
                "name": "Q1",
                "score": 1,
                "skipped": False
            },
            {
                "grading_end_time": 1697406273000,
                "grading_start_time": 1697406273000,
                "hard_fail": False,
                "max_points": 1,
                "message": "",
                "name": "Q2",
                "score": 1,
                "skipped": False
            },
            {
                "grading_end_time": 1697406273000,
                "grading_start_time": 1697406273000,
                "hard_fail": False,
                "max_points": 0,
                "message": "Style is clean!",
                "name": "Style",
                "score": 0,
                "skipped": False
            }
        ],
        "score": 2,
        "short-id": "1697406272",
        "user": "course-student@test.edulinq.org"
    },
    "input-files-gzip": {
        "submission.py": "H4sICAAAAAAA/3N1Ym1pc3Npb24ucHkASklNU0grzUsuyczPM9TQtOJSUFBQKEotKS3KUwgpKk3l4kJWYaRRlpiDqqgsMUdBW8GQCxAAAP//PpwmbkkAAAA="
    },
    "output-files-gzip": {
        "result.json": "H4sICAAAAAAA/3Jlc3VsdC5qc29uAMSSvQqDMBSFd5/iNrNDDPUnPkHX0qFDKRI0SEBja1JoEd+9mIptg1YyNdPl3HPO5YN0HgAAkqzmKAW0O2Lkv6TrjSstGqlQCicjDa+bpq/cPhhj06Zm9+zSCKmHfGAtVd60fEavuVKsNI12X9myQsgyU5q1OtPC3A0iSuMtTggJKVkIcFnM2id376/Skb/ThW50oQPdQT8q/hMQLwDa+gegKQWhIK84kxtn3sSFNyLxm9dM5/ETr97BlnGhn3q99wwAAP//PProBisDAAA="
    },
    "stderr": "",
    "stdout": "Autograder transcript for assignment: HW0.\nGrading started at 2023-11-11 22:13 and ended at 2023-11-11 22:13.\nQ1: 1 / 1\nQ2: 1 / 1\nStyle: 0 / 0\n   Style is clean!\n\nTotal: 2 / 2\n"
}
