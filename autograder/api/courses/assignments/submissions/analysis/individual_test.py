import copy
import typing

import autograder.api.config
import autograder.api.courses.assignments.submissions.analysis.individual
import autograder.testing.asserts
import autograder.testing.server

class TestCoursesAssignmentsSubmissionsAnalysisIndividual(autograder.testing.server.ServerTest):
    """ Test individual analysis. """

    def test_base(self):
        """ Test base functionality. """

        dry_run_analysis = copy.deepcopy(BASE_TEST_ANALYSIS)
        dry_run_analysis['options']['dry-run'] = True

        # [(config (and overrides), kwargs, expected, error substring), ...]
        test_cases = [
            # Base
            (
                {
                    autograder.api.config.PARAM_USER_EMAIL.config_key: 'server-admin@test.edulinq.org',
                    autograder.api.config.PARAM_USER_PASS.config_key: 'server-admin',

                    autograder.api.config.PARAM_SUBMISSION_SPECS.config_key: [
                        'course101::hw0::course-student@test.edulinq.org::1697406256',
                        'course101::hw0::course-student@test.edulinq.org::1697406265',
                    ],

                    autograder.api.config.PARAM_DRY_RUN.config_key: False,
                    autograder.api.config.PARAM_OVERWRITE_RECORDS.config_key: False,
                    autograder.api.config.PARAM_WAIT_FOR_COMPLETION.config_key: False,
                },
                {},
                BASE_TEST_ANALYSIS,
                None,
            ),

            # Dry Run
            (
                {
                    autograder.api.config.PARAM_USER_EMAIL.config_key: 'server-admin@test.edulinq.org',
                    autograder.api.config.PARAM_USER_PASS.config_key: 'server-admin',

                    autograder.api.config.PARAM_SUBMISSION_SPECS.config_key: [
                        'course101::hw0::course-student@test.edulinq.org::1697406256',
                        'course101::hw0::course-student@test.edulinq.org::1697406265',
                    ],

                    autograder.api.config.PARAM_DRY_RUN.config_key: True,
                    autograder.api.config.PARAM_OVERWRITE_RECORDS.config_key: False,
                    autograder.api.config.PARAM_WAIT_FOR_COMPLETION.config_key: False,
                },
                {},
                dry_run_analysis,
                None,
            ),

            # Wait for Completion
            (
                {
                    autograder.api.config.PARAM_USER_EMAIL.config_key: 'server-admin@test.edulinq.org',
                    autograder.api.config.PARAM_USER_PASS.config_key: 'server-admin',

                    autograder.api.config.PARAM_SUBMISSION_SPECS.config_key: [
                        'course101::hw0::course-student@test.edulinq.org::1697406256',
                        'course101::hw0::course-student@test.edulinq.org::1697406265',
                    ],

                    autograder.api.config.PARAM_DRY_RUN.config_key: False,
                    autograder.api.config.PARAM_OVERWRITE_RECORDS.config_key: False,
                    autograder.api.config.PARAM_WAIT_FOR_COMPLETION.config_key: True,
                },
                {},
                COMPLETE_TEST_ANALYSIS,
                None,
            ),
        ]

        self.base_api_test(autograder.api.courses.assignments.submissions.analysis.individual.send, test_cases,
                actual_clean_func = autograder.testing.asserts.normalize_analysis)

BASE_TEST_ANALYSIS: typing.Dict[str, typing.Any] = {
    "complete": False,
    "options": {
        "dry-run": False,
        "overwrite-records": False,
        "submissions": [
            "course101::hw0::course-student@test.edulinq.org::1697406256",
            "course101::hw0::course-student@test.edulinq.org::1697406265"
        ],
        "wait-for-completion": False
    },
    "results": {},
    "summary": {
        "aggregate-lines-of-code": {
            "count": 0,
            "max": 0,
            "mean": 0,
            "median": 0,
            "min": 0
        },
        "aggregate-lines-of-code-delta": {
            "count": 0,
            "max": 0,
            "mean": 0,
            "median": 0,
            "min": 0
        },
        "aggregate-lines-of-code-per-file": None,
        "aggregate-lines-of-code-per-hour": {
            "count": 0,
            "max": 0,
            "mean": 0,
            "median": 0,
            "min": 0
        },
        "aggregate-score": {
            "count": 0,
            "max": 0,
            "mean": 0,
            "median": 0,
            "min": 0
        },
        "aggregate-score-delta": {
            "count": 0,
            "max": 0,
            "mean": 0,
            "median": 0,
            "min": 0
        },
        "aggregate-score-per-hour": {
            "count": 0,
            "max": 0,
            "mean": 0,
            "median": 0,
            "min": 0
        },
        "aggregate-submission-time-delta": {
            "count": 0,
            "max": 0,
            "mean": 0,
            "median": 0,
            "min": 0
        },
        "complete": False,
        "complete-count": 0,
        "error-count": 0,
        "failure-count": 0,
        "first-timestamp": autograder.testing.asserts.TEST_TIMESTAMP,
        "last-timestamp": autograder.testing.asserts.TEST_TIMESTAMP,
        "pending-count": 2
    },
    "work-errors": {}
}

COMPLETE_TEST_ANALYSIS: typing.Dict[str, typing.Any] = {
    "complete": True,
    "options": {
        "dry-run": False,
        "overwrite-records": False,
        "submissions": [
            "course101::hw0::course-student@test.edulinq.org::1697406256",
            "course101::hw0::course-student@test.edulinq.org::1697406265"
        ],
        "wait-for-completion": True
    },
    "results": {
        "course101::hw0::course-student@test.edulinq.org::1697406256": {
            "analysis-timestamp": autograder.testing.asserts.TEST_TIMESTAMP,
            "assignment-id": "hw0",
            "course-id": "course101",
            "files": [
                {
                    "filename": "submission.py",
                    "lines-of-code": 4
                }
            ],
            "lines-of-code": 4,
            "options": {
                "engine-options": {
                    "dolos": {
                        "kgram-length": 22,
                        "kgrams-in-window": 18
                    },
                    "jplag": {
                        "min-tokens": 5
                    }
                },
                "include-patterns": [
                    "submission.py"
                ],
                "template-files": [
                    {
                        "path": "test-submissions/not_implemented/submission.py",
                        "type": "path"
                    }
                ]
            },
            "short-id": "1697406256",
            "submission-id": "course101::hw0::course-student@test.edulinq.org::1697406256",
            "submission-start-time": 1697406256000,
            "user-email": "course-student@test.edulinq.org"
        },
        "course101::hw0::course-student@test.edulinq.org::1697406265": {
            "analysis-timestamp": autograder.testing.asserts.TEST_TIMESTAMP,
            "assignment-id": "hw0",
            "course-id": "course101",
            "files": [
                {
                    "filename": "submission.py",
                    "lines-of-code": 4
                }
            ],
            "lines-of-code": 4,
            "options": {
                "engine-options": {
                    "dolos": {
                        "kgram-length": 22,
                        "kgrams-in-window": 18
                    },
                    "jplag": {
                        "min-tokens": 5
                    }
                },
                "include-patterns": [
                    "submission.py"
                ],
                "template-files": [
                    {
                        "path": "test-submissions/not_implemented/submission.py",
                        "type": "path"
                    }
                ]
            },
            "score": 1,
            "score-delta": 1,
            "score-per-hour": 360,
            "short-id": "1697406265",
            "submission-id": "course101::hw0::course-student@test.edulinq.org::1697406265",
            "submission-start-time": 1697406266000,
            "submission-time-delta": 10000,
            "user-email": "course-student@test.edulinq.org"
        }
    },
    "summary": {
        "aggregate-lines-of-code": {
            "count": 2,
            "max": 4,
            "mean": 4,
            "median": 4,
            "min": 4
        },
        "aggregate-lines-of-code-delta": {
            "count": 2,
            "max": 0,
            "mean": 0,
            "median": 0,
            "min": 0
        },
        "aggregate-lines-of-code-per-file": {
            "submission.py": {
                "count": 2,
                "max": 4,
                "mean": 4,
                "median": 4,
                "min": 4
            }
        },
        "aggregate-lines-of-code-per-hour": {
            "count": 2,
            "max": 0,
            "mean": 0,
            "median": 0,
            "min": 0
        },
        "aggregate-score": {
            "count": 2,
            "max": 1,
            "mean": 0.5,
            "median": 0.5,
            "min": 0
        },
        "aggregate-score-delta": {
            "count": 2,
            "max": 1,
            "mean": 0.5,
            "median": 0.5,
            "min": 0
        },
        "aggregate-score-per-hour": {
            "count": 2,
            "max": 360,
            "mean": 180,
            "median": 180,
            "min": 0
        },
        "aggregate-submission-time-delta": {
            "count": 2,
            "max": 10000,
            "mean": 5000,
            "median": 5000,
            "min": 0
        },
        "complete": True,
        "complete-count": 2,
        "error-count": 0,
        "failure-count": 0,
        "first-timestamp": autograder.testing.asserts.TEST_TIMESTAMP,
        "last-timestamp": autograder.testing.asserts.TEST_TIMESTAMP,
        "pending-count": 0
    },
    "work-errors": {}
}
