import typing

import autograder.api.config
import autograder.api.courses.assignments.report
import autograder.model.config
import autograder.testing.model
import autograder.testing.server

class TestCoursesAssignmentsReport(autograder.testing.server.ServerTest):
    """ Test getting assignment reports. """

    def test_base(self) -> None:
        """ Test base functionality. """

        # [(config (and overrides), kwargs, expected, error substring), ...]
        test_cases: typing.List[typing.Tuple[
            autograder.model.config.Config,
            typing.Dict[str, typing.Any],
            typing.Any,
            typing.Union[str, None],
        ]] = [
            (
                autograder.model.config.Config(
                    course = 'course101',
                    auth_user = 'server-admin@test.edulinq.org',
                    auth_pass = 'server-admin',
                ),
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
