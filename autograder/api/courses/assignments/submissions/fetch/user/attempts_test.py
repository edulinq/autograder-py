import typing

import autograder.api.config
import autograder.api.courses.assignments.submissions.fetch.user.attempts
import autograder.testing.server

class TestCourseAssignmentsFetchUserAttempts(autograder.testing.server.ServerTest):
    """ Test fetching user submission attempts. """

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
                    SUBMISSIONS,
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
                    [],
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
                    [],
                ),
                None,
            ),
        ]

        self.base_api_test(autograder.api.courses.assignments.submissions.fetch.user.attempts.send, test_cases)

# pylint: disable=line-too-long
SUBMISSIONS: typing.List[typing.Dict[str, typing.Any]] = [
    {
        "info": {
            "additional-info": None,
            "assignment-id": "hw0",
            "course-id": "course101",
            "grading_end_time": 1697406256000,
            "grading_start_time": 1697406256000,
            "id": "course101::hw0::course-student@test.edulinq.org::1697406256",
            "max_points": 2,
            "message": "",
            "name": "HW0",
            "questions": [
                {
                    "grading_end_time": 1697406256000,
                    "grading_start_time": 1697406256000,
                    "hard_fail": False,
                    "max_points": 1,
                    "message": "NotImplemented returned.",
                    "name": "Q1",
                    "score": 0,
                    "skipped": False
                },
                {
                    "grading_end_time": 1697406256000,
                    "grading_start_time": 1697406256000,
                    "hard_fail": False,
                    "max_points": 1,
                    "message": "NotImplemented returned.",
                    "name": "Q2",
                    "score": 0,
                    "skipped": False
                },
                {
                    "grading_end_time": 1697406256000,
                    "grading_start_time": 1697406256000,
                    "hard_fail": False,
                    "max_points": 0,
                    "message": "Style is clean!",
                    "name": "Style",
                    "score": 0,
                    "skipped": False
                }
            ],
            "score": 0,
            "short-id": "1697406256",
            "user": "course-student@test.edulinq.org"
        },
        "input-files-gzip": {
            "submission.py": "H4sICAAAAAAA/3N1Ym1pc3Npb24ucHkASklNU0grzUsuyczPM9TQtOJSUFBQKEotKS3KU/DLL/HMLchJzU3NK0lN4eJCVmukUZaYg1c5IAAA//8hrjgTWgAAAA=="
        },
        "output-files-gzip": {
            "result.json": "H4sICAAAAAAA/3Jlc3VsdC5qc29uAMySwWrDMAyG73kKzecy4rRrkz7BdhmMHXYYI5haBEMsd7YKG6XvPuIlGTFsWW7NSUj/J+UDnzMAAEHKotiDuH/Jxeq79X7CwMZREHt4ja3uO4/VhHuSPTZOrPqoj84Qd7xMhuHgfMflKYQhqCZufHT8YI8tWiRGDR755An1bXqn8UobaurAynPNJv6P3FbVbpOXhVxX6Y0BQNJDXEzyYsxfVrPexdV6r+e9J/EF1s/82eKf4qngP8TjUjABDi0qulnsu13iuynufnxj9dY/+7k7ZZkEf9m/yy7ZVwAAAP//do3jyV0DAAA="
        },
        "stderr": "Dummy Stderr\n",
        "stdout": "Autograder transcript for assignment: HW0.\nGrading started at 2023-11-11 22:13 and ended at 2023-11-11 22:13.\nQ1: 0 / 1\n   NotImplemented returned.\nQ2: 0 / 1\n   NotImplemented returned.\nStyle: 0 / 0\n   Style is clean!\n\nTotal: 0 / 2\n"
    },
    {
        "info": {
            "additional-info": None,
            "assignment-id": "hw0",
            "course-id": "course101",
            "grading_end_time": 1697406266000,
            "grading_start_time": 1697406266000,
            "id": "course101::hw0::course-student@test.edulinq.org::1697406265",
            "max_points": 2,
            "message": "",
            "name": "HW0",
            "questions": [
                {
                    "grading_end_time": 1697406266000,
                    "grading_start_time": 1697406266000,
                    "hard_fail": False,
                    "max_points": 1,
                    "message": "",
                    "name": "Q1",
                    "score": 1,
                    "skipped": False
                },
                {
                    "grading_end_time": 1697406266000,
                    "grading_start_time": 1697406266000,
                    "hard_fail": False,
                    "max_points": 1,
                    "message": "NotImplemented returned.",
                    "name": "Q2",
                    "score": 0,
                    "skipped": False
                },
                {
                    "grading_end_time": 1697406266000,
                    "grading_start_time": 1697406266000,
                    "hard_fail": False,
                    "max_points": 0,
                    "message": "Style is clean!",
                    "name": "Style",
                    "score": 0,
                    "skipped": False
                }
            ],
            "score": 1,
            "short-id": "1697406265",
            "user": "course-student@test.edulinq.org"
        },
        "input-files-gzip": {
            "submission.py": "H4sICAAAAAAA/3N1Ym1pc3Npb24ucHkASklNU0grzUsuyczPM9TQtOJSUFBQKEotKS3KUwgpKk3l4kJWYaRRlpiDqsgvv8QztyAnNTc1ryQ1hQsQAAD//6rUxttQAAAA"
        },
        "output-files-gzip": {
            "result.json": "H4sICAAAAAAA/3Jlc3VsdC5qc29uAJySzWrDMBCE736Krc6hSE5/7DxBeymUHnooxYhoMQJrlUobaAl59xI1uFTEcRWfltmZMd+iXQUAIEg7FCsQD69SLH6kjy1Gtp6iWMFbkg7fbpz+5J7VMTZunP7sNt4SH/IqW8a1D3hCdxij7lNj3tcHbSz1XWQduGOb/qvu2vb+Rja1atvbiQCSOWkf3fvFLF19EZ2cpnvy/Og2AzokRgMBeRsIzXUxdVNG3RRQv/DXgGfBc8B/gKdSsBHWA2q6KuOtpcxvfY63lkv5y5um9+Pjnr3rMjNO9KtqX30HAAD//xSSgptDAwAA"
        },
        "stderr": "",
        "stdout": "Autograder transcript for assignment: HW0.\nGrading started at 2023-11-11 22:13 and ended at 2023-11-11 22:13.\nQ1: 1 / 1\nQ2: 0 / 1\n   NotImplemented returned.\nStyle: 0 / 0\n   Style is clean!\n\nTotal: 1 / 2\n"
    },
    {
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
]
