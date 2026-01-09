import copy
import typing

import autograder.api.config
import autograder.api.courses.assignments.submissions.analysis.pairwise
import autograder.testing.asserts
import autograder.testing.server

class TestCoursesAssignmentsSubmissionsAnalysisPairwise(autograder.testing.server.ServerTest):
    """ Test pairwise analysis. """

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

        self.base_api_test(autograder.api.courses.assignments.submissions.analysis.pairwise.send, test_cases,
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
        "aggregate-mean-similarities": None,
        "aggregate-total-mean-similarity": {
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
        "pending-count": 1
    },
    "work-errors": {}
}

# pylint: disable=line-too-long
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
        "course101::hw0::course-student@test.edulinq.org::1697406256||course101::hw0::course-student@test.edulinq.org::1697406265": {
            "analysis-timestamp": autograder.testing.asserts.TEST_TIMESTAMP,
            "mean-similarities": {
                "submission.py": 0.13
            },
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
            "similarities": {
                "submission.py": [
                    {
                        "filename": "submission.py",
                        "score": 0.13,
                        "tool": "fake",
                        "version": "0.0.1"
                    }
                ]
            },
            "submission-ids": "course101::hw0::course-student@test.edulinq.org::1697406256||course101::hw0::course-student@test.edulinq.org::1697406265",
            "total-mean-similarity": 0.13
        }
    },
    "summary": {
        "aggregate-mean-similarities": {
            "submission.py": {
                "count": 1,
                "max": 0.13,
                "mean": 0.13,
                "median": 0.13,
                "min": 0.13
            }
        },
        "aggregate-total-mean-similarity": {
            "count": 1,
            "max": 0.13,
            "mean": 0.13,
            "median": 0.13,
            "min": 0.13
        },
        "complete": True,
        "complete-count": 1,
        "error-count": 0,
        "failure-count": 0,
        "first-timestamp": autograder.testing.asserts.TEST_TIMESTAMP,
        "last-timestamp": autograder.testing.asserts.TEST_TIMESTAMP,
        "pending-count": 0
    },
    "work-errors": {}
}
