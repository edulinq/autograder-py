import sys
import typing
import unittest

import edq.util.crypto
import edq.util.time

import autograder.api.config
import autograder.api.courses.assignments.submissions.proxy.submit
import autograder.model.config
import autograder.testing.constants
import autograder.testing.server

class TestCourseAssignmentsProxySubmit(autograder.testing.server.ServerTest):
    """ Test proxy submitting and assignment. """

    @unittest.skipIf(sys.platform.startswith("win"), "Windows file hashes create different HTTP exchange queries")
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
                    proxy_email = 'course-student@test.edulinq.org',
                ),
                {
                    'post_paths': [
                        autograder.testing.constants.TEST_SUBMISSIONS_BASH_SOLUTION_PATH,
                    ]
                },
                {
                    'found-user': True,
                    'rejected': False,
                    'message': '',
                    'grading-success': True,
                    'result': 10,
                },
                None,
            ),
            (
                autograder.model.config.Config(
                    auth_user = 'course-admin@test.edulinq.org',
                    auth_pass = edq.util.crypto.Secret('course-admin'),
                    course = 'course-languages',
                    assignment = 'bash',
                    proxy_email = 'course-student@test.edulinq.org',
                ),
                {
                    'post_paths': [
                        autograder.testing.constants.TEST_SUBMISSIONS_BASH_SOLUTION_PATH,
                    ]
                },
                {
                    'found-user': True,
                    'rejected': False,
                    'message': '',
                    'grading-success': True,
                    'result': 10,
                },
                None,
            ),

            # Proxy Time
            (
                autograder.model.config.Config(
                    auth_user = 'server-admin@test.edulinq.org',
                    auth_pass = edq.util.crypto.Secret('server-admin'),
                    course = 'course-languages',
                    assignment = 'bash',
                    proxy_email = 'course-student@test.edulinq.org',
                    proxy_time = edq.util.time.Timestamp.guess(12345),
                ),
                {
                    'post_paths': [
                        autograder.testing.constants.TEST_SUBMISSIONS_BASH_SOLUTION_PATH,
                    ]
                },
                {
                    'found-user': True,
                    'rejected': False,
                    'message': '',
                    'grading-success': True,
                    'result': 10,
                },
                None,
            ),

            # Missing User
            (
                autograder.model.config.Config(
                    auth_user = 'server-admin@test.edulinq.org',
                    auth_pass = edq.util.crypto.Secret('server-admin'),
                    course = 'course-languages',
                    assignment = 'bash',
                    proxy_email = 'ZZZ@test.edulinq.org',
                ),
                {
                    'post_paths': [
                        autograder.testing.constants.TEST_SUBMISSIONS_BASH_SOLUTION_PATH,
                    ]
                },
                {
                    'found-user': False,
                    'rejected': False,
                    'message': '',
                    'grading-success': False,
                    'result': None,
                },
                None,
            ),
            (
                autograder.model.config.Config(
                    auth_user = 'course-admin@test.edulinq.org',
                    auth_pass = edq.util.crypto.Secret('course-admin'),
                    course = 'course-languages',
                    assignment = 'bash',
                    proxy_email = 'ZZZ@test.edulinq.org',
                ),
                {
                    'post_paths': [
                        autograder.testing.constants.TEST_SUBMISSIONS_BASH_SOLUTION_PATH,
                    ]
                },
                {
                    'found-user': False,
                    'rejected': False,
                    'message': '',
                    'grading-success': False,
                    'result': None,
                },
                None,
            ),

            # Missing Files
            (
                autograder.model.config.Config(
                    auth_user = 'server-admin@test.edulinq.org',
                    auth_pass = edq.util.crypto.Secret('server-admin'),
                    course = 'course-languages',
                    assignment = 'bash',
                    proxy_email = 'course-student@test.edulinq.org',
                ),
                {},
                None,
                'No files provided for submission',
            ),

            # Bad Paths
            (
                autograder.model.config.Config(
                    auth_user = 'server-admin@test.edulinq.org',
                    auth_pass = edq.util.crypto.Secret('server-admin'),
                    course = 'course-languages',
                    assignment = 'bash',
                    proxy_email = 'course-student@test.edulinq.org',
                ),
                {
                    'post_paths': [
                        'ZZZ',
                    ]
                },
                None,
                'does not exist, or is not a file',
            ),

            # Grading Fail
            (
                autograder.model.config.Config(
                    auth_user = 'server-admin@test.edulinq.org',
                    auth_pass = edq.util.crypto.Secret('server-admin'),
                    course = 'course-languages',
                    assignment = 'bash',
                    proxy_email = 'course-student@test.edulinq.org',
                ),
                {
                    'post_paths': [
                        autograder.testing.constants.TEST_SUBMISSIONS_BASH_BAD_PATH,
                    ]
                },
                {
                    'found-user': True,
                    'rejected': False,
                    'message': '',
                    'grading-success': False,
                    'result': None,
                },
                None,
            ),
        ]

        self.base_api_test(autograder.api.courses.assignments.submissions.proxy.submit.send, test_cases, actual_clean_func = _clean_response)

def _clean_response(actual: typing.Tuple[typing.Dict[str, typing.Any], typing.Union[autograder.assignment.GradedAssignment, None]]) -> typing.Any:
    """ Clean the submit response to parse out just the data we care about. """

    (response, assignment) = actual

    data = {
        'found-user': response['found-user'],
        'rejected': response['rejected'],
        'message': response['message'],
        'grading-success': response['grading-success'],
        'result': None,
    }

    if (assignment is not None):
        data['result'] = assignment.get_score()[0]

    return data
