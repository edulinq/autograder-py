import autograder.api.config
import autograder.api.courses.assignments.report
import autograder.testing.model
import autograder.testing.server

class TestUsersList(autograder.testing.server.ServerTest):
    """ Test getting assignment reports. """

    def test_base(self):
        """ Test base functionality. """

        # [(config (and overrides), kwargs, expected, error substring), ...]
        test_cases = [
            (
                {
                    autograder.api.config.PARAM_COURSE.config_key: 'course101',
                    autograder.api.config.PARAM_USER_EMAIL.config_key: 'server-admin@test.edulinq.org',
                    autograder.api.config.PARAM_USER_PASS.config_key: 'server-admin',
                },
                {},
                {
                    "course-report": {
                        "assignments": [
                            {
                                "assignment-name": "Homework 0",
                                "latest-submission": 1697406273000,
                                "number-of-submissions": 1,
                                "questions": [
                                    {
                                        "max": 1,
                                        "mean": 1,
                                        "median": 1,
                                        "min": 1,
                                        "question-name": "Q1",
                                        "standard-deviation": -1
                                    },
                                    {
                                        "max": 1,
                                        "mean": 1,
                                        "median": 1,
                                        "min": 1,
                                        "question-name": "Q2",
                                        "standard-deviation": -1
                                    },
                                    {
                                        "max": 0,
                                        "mean": 0,
                                        "median": 0,
                                        "min": 0,
                                        "question-name": "Style",
                                        "standard-deviation": -1
                                    },
                                    {
                                        "max": 1,
                                        "mean": 1,
                                        "median": 1,
                                        "min": 1,
                                        "question-name": "<Overall>",
                                        "standard-deviation": -1
                                    }
                                ]
                            }
                        ],
                        "course-name": "Course 101"
                    }
                },
                None,
            ),
        ]

        self.base_api_test(autograder.api.courses.assignments.report.send, test_cases)
