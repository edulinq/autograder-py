import typing

import edq.util.crypto

import autograder.api.config
import autograder.api.courses.assignments.submissions.proxy.regrade
import autograder.model.config
import autograder.testing.asserts
import autograder.testing.server

class TestCoursesAssignmentsSubmissionsProxyRegrade(autograder.testing.server.ServerTest):
    """ Test proxy regrades. """

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
                    course = 'course-languages',
                    assignment = 'bash',

                    dry_run = False,
                    overwrite_records = False,
                    wait_for_completion = False,
                ),
                {},
                {
                    "complete": False,
                    "options": {
                        "dry-run": False,
                        "overwrite-records": False,
                        "regrade-cutoff": autograder.testing.constants.TEST_TIMESTAMP,
                        "target-users": [
                            "*"
                        ],
                        "wait-for-completion": False
                    },
                    "resolved-users": [
                        "course-admin@test.edulinq.org",
                        "course-grader@test.edulinq.org",
                        "course-other@test.edulinq.org",
                        "course-owner@test.edulinq.org",
                        "course-student@test.edulinq.org"
                    ],
                    "results": {},
                    "work-errors": {},
                },
                None,
            ),

            # Users
            (
                autograder.model.config.Config(
                    auth_user = 'server-admin@test.edulinq.org',
                    auth_pass = edq.util.crypto.Secret('server-admin'),
                    course = 'course-languages',
                    assignment = 'bash',

                    target_users = [
                        'student',
                    ],

                    dry_run = False,
                    overwrite_records = False,
                    wait_for_completion = False,
                ),
                {},
                {
                    "complete": False,
                    "options": {
                        "dry-run": False,
                        "overwrite-records": False,
                        "regrade-cutoff": autograder.testing.constants.TEST_TIMESTAMP,
                        "target-users": [
                            "student",
                        ],
                        "wait-for-completion": False
                    },
                    "resolved-users": [
                        "course-student@test.edulinq.org"
                    ],
                    "results": {},
                    "work-errors": {},
                },
                None,
            ),
            (
                autograder.model.config.Config(
                    auth_user = 'course-admin@test.edulinq.org',
                    auth_pass = edq.util.crypto.Secret('course-admin'),
                    course = 'course-languages',
                    assignment = 'bash',

                    target_users = [
                        'student',
                    ],

                    dry_run = False,
                    overwrite_records = False,
                    wait_for_completion = False,
                ),
                {},
                {
                    "complete": False,
                    "options": {
                        "dry-run": False,
                        "overwrite-records": False,
                        "regrade-cutoff": autograder.testing.constants.TEST_TIMESTAMP,
                        "target-users": [
                            "student",
                        ],
                        "wait-for-completion": False
                    },
                    "resolved-users": [
                        "course-student@test.edulinq.org"
                    ],
                    "results": {},
                    "work-errors": {},
                },
                None,
            ),

            # Wait and Cutoff
            (
                autograder.model.config.Config(
                    auth_user = 'server-admin@test.edulinq.org',
                    auth_pass = edq.util.crypto.Secret('server-admin'),
                    course = 'course-languages',
                    assignment = 'bash',

                    regrade_cutoff = autograder.testing.constants.TEST_TIMESTAMP,

                    dry_run = False,
                    overwrite_records = False,
                    wait_for_completion = True,
                ),
                {},
                {
                    "complete": True,
                    "options": {
                        "dry-run": False,
                        "overwrite-records": False,
                        "regrade-cutoff": autograder.testing.constants.TEST_TIMESTAMP,
                        "target-users": [
                            "*"
                        ],
                        "wait-for-completion": True
                    },
                    "resolved-users": [
                        "course-admin@test.edulinq.org",
                        "course-grader@test.edulinq.org",
                        "course-other@test.edulinq.org",
                        "course-owner@test.edulinq.org",
                        "course-student@test.edulinq.org"
                    ],
                    "results": {
                        "course-admin@test.edulinq.org": None,
                        "course-grader@test.edulinq.org": None,
                        "course-other@test.edulinq.org": None,
                        "course-owner@test.edulinq.org": None,
                        "course-student@test.edulinq.org": {
                            "assignment-id": "bash",
                            "course-id": "course-languages",
                            "grading_start_time": autograder.testing.constants.TEST_TIMESTAMP,
                            "id": "course-languages::bash::course-student@test.edulinq.org::1768603685",
                            "max_points": 10,
                            "message": "",
                            "score": 10,
                            "short-id": "1768603685",
                            "user": "course-student@test.edulinq.org"
                        }
                    },
                    "work-errors": {},
                },
                None,
            ),
        ]

        self.base_api_test(autograder.api.courses.assignments.submissions.proxy.regrade.send, test_cases,
                actual_clean_func = _clean_response)

def _clean_response(actual: typing.Dict[str, typing.Any]) -> typing.Any:
    """ Clean the response. """

    actual['options']['regrade-cutoff'] = autograder.testing.constants.TEST_TIMESTAMP

    for result in actual['results'].values():
        if (result is None):
            continue

        result['grading_start_time'] = autograder.testing.constants.TEST_TIMESTAMP

    return actual
