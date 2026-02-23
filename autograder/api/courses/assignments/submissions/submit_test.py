import re
import sys
import typing
import unittest

import edq.testing.asserts

import autograder.api.config
import autograder.api.courses.assignments.submissions.submit
import autograder.testing.constants
import autograder.testing.server

class TestCourseAssignmentsSubmit(autograder.testing.server.ServerTest):
    """ Test submitting and assignment. """

    @unittest.skipIf(sys.platform.startswith("win"), "Windows file hashes create different HTTP exchange queries")
    def test_base(self):
        """ Test base functionality. """

        # pylint: disable=line-too-long
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
                        autograder.testing.constants.TEST_SUBMISSIONS_BASH_SOLUTION_PATH,
                    ]
                },
                {
                    'rejected': False,
                    'message': '',
                    'grading-success': True,
                    'result': 10,
                    'epilogue': None,
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
                        autograder.testing.constants.TEST_SUBMISSIONS_BASH_SOLUTION_PATH,
                    ]
                },
                {
                    'rejected': False,
                    'message': '',
                    'grading-success': True,
                    'result': 10,
                    'epilogue': None,
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
                        autograder.testing.constants.TEST_SUBMISSIONS_BASH_BAD_PATH,
                    ]
                },
                {
                    'rejected': False,
                    'message': '',
                    'grading-success': False,
                    'result': None,
                    'epilogue': None,
                },
                None,
            ),

            # Crash - Bash
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
                        autograder.testing.constants.TEST_SUBMISSIONS_BASH_CRASH_PATH,
                    ]
                },
                {
                    'rejected': False,
                    'message': "Cannot find output/result of grading. It is likely that the grader crashed.\n--- stdout ---\nCRASH\n\n--------------\n\n--- stderr ---\n\n--------------\n",
                    'grading-success': False,
                    'result': None,
                    'epilogue': None,
                },
                None,
            ),

            # Crash - Python
            (
                {
                    autograder.api.config.PARAM_USER_EMAIL.config_key: 'server-admin@test.edulinq.org',
                    autograder.api.config.PARAM_USER_PASS.config_key: 'server-admin',
                    autograder.api.config.PARAM_COURSE.config_key: 'course101',
                    autograder.api.config.PARAM_ASSIGNMENT.config_key: 'hw0',
                    autograder.api.config.PARAM_ALLOW_LATE.config_key: False,
                },
                {
                    'post_paths': [
                        autograder.testing.constants.NOCOMPILE_PYTHON_PATH,
                    ]
                },
                {
                    'rejected': False,
                    'message': "",
                    'grading-success': True,
                    'result': 0,
                    'epilogue': autograder.testing.constants.TEST_CRASH_EPILOGUE,
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
        'epilogue': None,
    }

    if (assignment is not None):
        data['result'] = assignment.get_score()[0]

        if (assignment.epilogue is not None):
            epilogue = assignment.epilogue
            for (regex, replacement) in edq.testing.asserts.TEXT_NORMALIZATIONS:
                epilogue = re.sub(regex, replacement, epilogue, flags = re.MULTILINE)

            if ("ModuleNotFoundError: No module named 'ZZZ'" in epilogue):
                epilogue = autograder.testing.constants.TEST_CRASH_EPILOGUE

            data['epilogue'] = epilogue

    return data
