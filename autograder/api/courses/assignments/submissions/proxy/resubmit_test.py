import sys
import typing
import unittest

import autograder.api.config
import autograder.api.courses.assignments.submissions.proxy.resubmit
import autograder.model.config
import autograder.testing.server

class TestCourseAssignmentsProxyResubmit(autograder.testing.server.ServerTest):
    """ Test proxy resubmitting and assignment. """

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
                    auth_pass = 'server-admin',
                    course = 'course-languages',
                    assignment = 'bash',
                    proxy_email = 'course-student@test.edulinq.org',
                ),
                {},
                {
                    'found-user': True,
                    'found-submission': True,
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
                    auth_pass = 'course-admin',
                    course = 'course-languages',
                    assignment = 'bash',
                    proxy_email = 'course-student@test.edulinq.org',
                ),
                {},
                {
                    'found-user': True,
                    'found-submission': True,
                    'rejected': False,
                    'message': '',
                    'grading-success': True,
                    'result': 10,
                },
                None,
            ),

            # Submission
            (
                autograder.model.config.Config(
                    auth_user = 'server-admin@test.edulinq.org',
                    auth_pass = 'server-admin',
                    course = 'course-languages',
                    assignment = 'bash',
                    proxy_email = 'course-student@test.edulinq.org',
                    target_submission = '1768603646',
                ),
                {},
                {
                    'found-user': True,
                    'found-submission': True,
                    'rejected': False,
                    'message': '',
                    'grading-success': True,
                    'result': 0,
                },
                None,
            ),

            # Proxy Time
            (
                autograder.model.config.Config(
                    auth_user = 'server-admin@test.edulinq.org',
                    auth_pass = 'server-admin',
                    course = 'course-languages',
                    assignment = 'bash',
                    proxy_email = 'course-student@test.edulinq.org',
                    proxy_time = 12345,
                ),
                {},
                {
                    'found-user': True,
                    'found-submission': True,
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
                    auth_pass = 'server-admin',
                    course = 'course-languages',
                    assignment = 'bash',
                    proxy_email = 'ZZZ@test.edulinq.org',
                ),
                {},
                {
                    'found-user': False,
                    'found-submission': False,
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
                    auth_pass = 'course-admin',
                    course = 'course-languages',
                    assignment = 'bash',
                    proxy_email = 'ZZZ@test.edulinq.org',
                ),
                {},
                {
                    'found-user': False,
                    'found-submission': False,
                    'rejected': False,
                    'message': '',
                    'grading-success': False,
                    'result': None,
                },
                None,
            ),

            # Missing Submission
            (
                autograder.model.config.Config(
                    auth_user = 'server-admin@test.edulinq.org',
                    auth_pass = 'server-admin',
                    course = 'course-languages',
                    assignment = 'bash',
                    proxy_email = 'course-student@test.edulinq.org',
                    target_submission = 'zzz',
                ),
                {},
                {
                    'found-user': True,
                    'found-submission': False,
                    'rejected': False,
                    'message': '',
                    'grading-success': False,
                    'result': None,
                },
                None,
            ),
        ]

        self.base_api_test(autograder.api.courses.assignments.submissions.proxy.resubmit.send, test_cases, actual_clean_func = _clean_response)

def _clean_response(actual: typing.Tuple[typing.Dict[str, typing.Any], typing.Union[autograder.assignment.GradedAssignment, None]]) -> typing.Any:
    """ Clean the response to parse out just the data we care about. """

    (response, assignment) = actual

    data = {
        'found-user': response['found-user'],
        'found-submission': response['found-submission'],
        'rejected': response['rejected'],
        'message': response['message'],
        'grading-success': response['grading-success'],
        'result': None,
    }

    if (assignment is not None):
        data['result'] = assignment.get_score()[0]

    return data
