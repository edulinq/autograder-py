import typing

import edq.util.crypto

import autograder.api.config
import autograder.api.courses.gradebook.fetch
import autograder.model.config
import autograder.testing.server

class TestCoursesGradebookFetch(autograder.testing.server.ServerTest):
    """ Test fetching a course gradebook. """

    def test_base(self) -> None:
        """ Test base functionality. """

        # [(config (and overrides), kwargs, expected, error substring), ...]
        test_cases: typing.List[typing.Tuple[
            autograder.model.config.Config,
            typing.Dict[str, typing.Any],
            typing.Any,
            typing.Union[str, None],
        ]] = [
            # Full Gradebook
            (
                autograder.model.config.Config(
                    auth_user = 'course-grader@test.edulinq.org',
                    auth_pass = edq.util.crypto.Secret('course-grader'),
                    course = 'course-languages',
                ),
                {},
                {
                    "gradebook": {
                        "bash": {
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
                        "cpp": {
                            "course-admin@test.edulinq.org": None,
                            "course-grader@test.edulinq.org": None,
                            "course-other@test.edulinq.org": None,
                            "course-owner@test.edulinq.org": None,
                            "course-student@test.edulinq.org": None
                        },
                        "java": {
                            "course-admin@test.edulinq.org": None,
                            "course-grader@test.edulinq.org": None,
                            "course-other@test.edulinq.org": None,
                            "course-owner@test.edulinq.org": None,
                            "course-student@test.edulinq.org": None
                        }
                    }
                },
                None,
            ),

            # Filtered Gradebook
            (
                autograder.model.config.Config(
                    auth_user = 'course-grader@test.edulinq.org',
                    auth_pass = edq.util.crypto.Secret('course-grader'),
                    course = 'course-languages',
                    target_users = ['student'],
                    target_assignments = ['bash', 'cpp'],
                ),
                {},
                {
                    "gradebook": {
                        "bash": {
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
                        "cpp": {
                            "course-student@test.edulinq.org": None
                        }
                    }
                },
                None,
            ),
        ]

        self.base_api_test(autograder.api.courses.gradebook.fetch.send, test_cases)
