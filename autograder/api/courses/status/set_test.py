import typing

import edq.util.crypto

import autograder.api.courses.status.set
import autograder.model.config
import autograder.testing.asserts
import autograder.testing.constants
import autograder.testing.server

class TestCoursesStatusSet(autograder.testing.server.ServerTest):
    """ Test setting a course status. """

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
                    auth_user = 'course-owner@test.edulinq.org',
                    auth_pass = edq.util.crypto.Secret('course-owner'),
                    course = 'course101',
                    active = True,
                ),
                {},
                {
                    "status": {
                        "active": True,
                        "owner": "course-owner@test.edulinq.org",
                        "set-time": autograder.testing.constants.TEST_TIMESTAMP,
                        "source": "course",
                    },
                },
                None,
            ),

            # Valid Overwrite
            (
                autograder.model.config.Config(
                    auth_user = 'course-admin@test.edulinq.org',
                    auth_pass = edq.util.crypto.Secret('course-admin'),
                    course = 'course101',
                    active = False,
                    force = True,
                ),
                {},
                {
                    "status": {
                        "active": False,
                        "owner": "course-admin@test.edulinq.org",
                        "set-time": autograder.testing.constants.TEST_TIMESTAMP,
                        "source": "course",
                    }
                },
                None,
            ),

            # Invalid Overwrite
            (
                autograder.model.config.Config(
                    auth_user = 'course-admin@test.edulinq.org',
                    auth_pass = edq.util.crypto.Secret('course-admin'),
                    course = 'course101',
                    active = True,
                ),
                {
                    'exit_on_error': False,
                },
                None,
                'Course active/inactive status already exists for this user',
            ),

            # Bad Permissions
            (
                autograder.model.config.Config(
                    auth_user = 'course-grader@test.edulinq.org',
                    auth_pass = edq.util.crypto.Secret('course-grader'),
                    course = 'course101',
                    active = True,
                ),
                {
                    'exit_on_error': False,
                },
                None,
                'You have insufficient permissions',
            ),
        ]

        self.base_api_test(autograder.api.courses.status.set.send, test_cases, actual_clean_func = autograder.testing.asserts.normalize_dict)
