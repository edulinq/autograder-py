import os
import sys
import typing
import unittest

import autograder.api.config
import autograder.api.courses.assignments.submissions.submit
import autograder.testing.server

THIS_DIR: str = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
ROOT_DIR: str = os.path.join(THIS_DIR, '..', '..', '..', '..', '..')
SUBMODULE_DIR: str = os.path.join(ROOT_DIR, 'testdata', 'autograder-testdata', 'autograder-server')
COURSE_DIR: str = os.path.join(SUBMODULE_DIR, 'testdata', 'course-languages')
TEST_SOLUTION_PATH: str = os.path.join(COURSE_DIR, 'bash', 'test-submissions', 'solution', 'assignment.sh')
TEST_BAD_PATH: str = os.path.join(COURSE_DIR, 'bash', 'test-submissions', 'solution', 'test-submission.json')

class TestCourseAssignmentsSubmit(autograder.testing.server.ServerTest):
    """ Test submitting and assignment. """

    @unittest.skipIf(sys.platform.startswith("win"), "Windows file hashes create different HTTP exchange queries")
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
                    autograder.api.config.PARAM_ALLOW_LATE.config_key: False,
                },
                {
                    'post_paths': [
                        TEST_SOLUTION_PATH,
                    ]
                },
                {
                    'rejected': False,
                    'message': '',
                    'grading-success': True,
                    'result': 10,
                },
                None,
            ),

            # Message
            (
                {
                    autograder.api.config.PARAM_USER_EMAIL.config_key: 'server-admin@test.edulinq.org',
                    autograder.api.config.PARAM_USER_PASS.config_key: 'server-admin',
                    autograder.api.config.PARAM_COURSE.config_key: 'course-languages',
                    autograder.api.config.PARAM_ASSIGNMENT.config_key: 'bash',
                    autograder.api.config.PARAM_ALLOW_LATE.config_key: False,
                    autograder.api.config.PARAM_SUBMISSION_MESSAGE.config_key: 'Test Message.',
                },
                {
                    'post_paths': [
                        TEST_SOLUTION_PATH,
                    ]
                },
                {
                    'rejected': False,
                    'message': '',
                    'grading-success': True,
                    'result': 10,
                },
                None,
            ),

            # Missing Files
            (
                {
                    autograder.api.config.PARAM_USER_EMAIL.config_key: 'server-admin@test.edulinq.org',
                    autograder.api.config.PARAM_USER_PASS.config_key: 'server-admin',
                    autograder.api.config.PARAM_COURSE.config_key: 'course-languages',
                    autograder.api.config.PARAM_ASSIGNMENT.config_key: 'bash',
                    autograder.api.config.PARAM_ALLOW_LATE.config_key: False,
                },
                {},
                None,
                'No files provided for submission',
            ),

            # Bad Paths
            (
                {
                    autograder.api.config.PARAM_USER_EMAIL.config_key: 'server-admin@test.edulinq.org',
                    autograder.api.config.PARAM_USER_PASS.config_key: 'server-admin',
                    autograder.api.config.PARAM_COURSE.config_key: 'course-languages',
                    autograder.api.config.PARAM_ASSIGNMENT.config_key: 'bash',
                    autograder.api.config.PARAM_ALLOW_LATE.config_key: False,
                },
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
                {
                    autograder.api.config.PARAM_USER_EMAIL.config_key: 'server-admin@test.edulinq.org',
                    autograder.api.config.PARAM_USER_PASS.config_key: 'server-admin',
                    autograder.api.config.PARAM_COURSE.config_key: 'course-languages',
                    autograder.api.config.PARAM_ASSIGNMENT.config_key: 'bash',
                    autograder.api.config.PARAM_ALLOW_LATE.config_key: False,
                },
                {
                    'post_paths': [
                        TEST_BAD_PATH,
                    ]
                },
                {
                    'rejected': False,
                    'message': '',
                    'grading-success': False,
                    'result': None,
                },
                None,
            ),
        ]

        self.base_api_test(autograder.api.courses.assignments.submissions.submit.send, test_cases, actual_clean_func = _clean_response)

def _clean_response(actual: typing.Tuple[typing.Dict[str, typing.Any], typing.Union[autograder.assignment.GradedAssignment, None]]) -> typing.Any:
    """ Clean the submit response to parse out just the data we care about. """

    (response, assignment) = actual

    data = {
        'rejected': response['rejected'],
        'message': response['message'],
        'grading-success': response['grading-success'],
        'result': None,
    }

    if (assignment is not None):
        data['result'] = assignment.get_score()[0]

    return data
