import typing

import autograder.api.config
import autograder.api.courses.assignments.submissions.proxy.regrade
import autograder.testing.server

TEST_CUTOFF: int = 100

class TestCoursesAssignmentsSubmissionsProxyRegrade(autograder.testing.server.ServerTest):
    """ Test proxy regrades. """

    def test_base(self):
        """ Test base functionality. """

        # [(config (and overrides), kwargs, expected, error substring), ...]
        test_cases = [
            # Base
            (
                {
                    autograder.api.config.PARAM_USER_EMAIL.config_key: 'server-admin@test.edulinq.org',
                    autograder.api.config.PARAM_USER_PASS.config_key: 'server-admin',
                    autograder.api.config.PARAM_COURSE.config_key: 'course-languages',
                    autograder.api.config.PARAM_ASSIGNMENT.config_key: 'bash',

                    autograder.api.config.PARAM_DRY_RUN.config_key: False,
                    autograder.api.config.PARAM_OVERWRITE_RECORDS.config_key: False,
                    autograder.api.config.PARAM_WAIT_FOR_COMPLETION.config_key: False,
                },
                {},
                {
                    "complete": False,
                    "options": {
                        "dry-run": False,
                        "overwrite-records": False,
                        "regrade-cutoff": TEST_CUTOFF,
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
                {
                    autograder.api.config.PARAM_USER_EMAIL.config_key: 'server-admin@test.edulinq.org',
                    autograder.api.config.PARAM_USER_PASS.config_key: 'server-admin',
                    autograder.api.config.PARAM_COURSE.config_key: 'course-languages',
                    autograder.api.config.PARAM_ASSIGNMENT.config_key: 'bash',

                    autograder.api.config.PARAM_COURSE_USER_REFERENCES.config_key: [
                        'student',
                    ],

                    autograder.api.config.PARAM_DRY_RUN.config_key: False,
                    autograder.api.config.PARAM_OVERWRITE_RECORDS.config_key: False,
                    autograder.api.config.PARAM_WAIT_FOR_COMPLETION.config_key: False,
                },
                {},
                {
                    "complete": False,
                    "options": {
                        "dry-run": False,
                        "overwrite-records": False,
                        "regrade-cutoff": TEST_CUTOFF,
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
                {
                    autograder.api.config.PARAM_USER_EMAIL.config_key: 'server-admin@test.edulinq.org',
                    autograder.api.config.PARAM_USER_PASS.config_key: 'server-admin',
                    autograder.api.config.PARAM_COURSE.config_key: 'course-languages',
                    autograder.api.config.PARAM_ASSIGNMENT.config_key: 'bash',

                    autograder.api.config.PARAM_REGRADE_CUTOFF.config_key: 10,

                    autograder.api.config.PARAM_DRY_RUN.config_key: False,
                    autograder.api.config.PARAM_OVERWRITE_RECORDS.config_key: False,
                    autograder.api.config.PARAM_WAIT_FOR_COMPLETION.config_key: True,
                },
                {},
                {
                    "complete": True,
                    "options": {
                        "dry-run": False,
                        "overwrite-records": False,
                        "regrade-cutoff": 10,
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
                            "grading_start_time": 1768603685040,
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

            # Wait for Completion
        ]

        self.base_api_test(autograder.api.courses.assignments.submissions.proxy.regrade.send, test_cases,
                actual_clean_func = _clean_response)

def _clean_response(actual: typing.Dict[str, typing.Any]) -> typing.Any:
    """ Clean the response. """

    if (actual['options']['regrade-cutoff'] > TEST_CUTOFF):
        actual['options']['regrade-cutoff'] = TEST_CUTOFF

    return actual
