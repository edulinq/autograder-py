#!/usr/bin/env python3

"""
Verify that the API test data (responses) are correct by sending them to an online
autograding server and verifying the responses.
This script should also be run in the autograding server's CI.
"""

import glob
import importlib
import json
import os
import sys
import traceback

THIS_DIR = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
ROOT_DIR = os.path.join(THIS_DIR, '..')
TEST_DATA_DIR = os.path.join(ROOT_DIR, 'tests', 'api', 'data')

# Add in the tests path.
sys.path.append(ROOT_DIR)

import autograder.api.config
import autograder.api.admin.updatecourse
import tests.api.test_api

def verify_test_case(cli_arguments, path):
    print("Verifying test case: '%s'." % (path))

    import_module_name, arguments, expected, is_error, output_modifier = tests.api.test_api.get_api_test_info(path)

    for key, value in vars(cli_arguments).items():
        if ((value is not None) or (value)):
            arguments[key] = value

    api_module = importlib.import_module(import_module_name)

    try:
        actual = api_module.send(arguments)

        if (is_error):
            _format_error(expected, actual, path, "Test case does not raise an error when one was expected")

            return 1
    except Exception as ex:
        if (not is_error):
            raise ex

        expected = expected.get('message', '')
        expected = tests.api.test_api.PYTHON_ERROR_PREFIX + expected
        if (expected != str(ex)):
            _format_error(expected, str(ex), path, "Test case does not raise the expected error")

            return 1

        return 0

    actual = output_modifier(actual)

    if (actual != expected):
        _format_error(expected, actual, path, "Test case does not have expected content")

        return 1

    return 0

def _format_error(expected, actual, path, message):
    expected_json = json.dumps(expected, indent = 4)
    actual_json = json.dumps(actual, indent = 4)

    print("ERROR: %s: '%s'." % (message, path))
    print(tests.api.test_api.FORMAT_STR % (expected_json, actual_json))

def reset_course(cli_arguments):
    arguments = tests.api.test_api.BASE_ARGUMENTS.copy()
    for key, value in vars(cli_arguments).items():
        if ((value is not None) or (value)):
            arguments[key] = value

    arguments['clear'] = True

    autograder.api.admin.updatecourse.send(arguments)

def run(arguments):
    error_count = 0

    # Do an initial reset of the DB.
    reset_course(arguments)

    for path in sorted(glob.glob(os.path.join(TEST_DATA_DIR, '**', 'test_*.json'), recursive = True)):
        try:
            error_count += verify_test_case(arguments, path)
        except Exception as ex:
            error_count += 1
            print("Error verifying test '%s'." % (path))
            traceback.print_exception(ex)

        # Reset the DB after every test.
        reset_course(arguments)

    if (error_count > 0):
        print("Found %d API test case issues." % (error_count))
    else:
        print("Found no API test case issues.")

    return error_count

def main():
    parser = autograder.api.config.get_argument_parser(
        description = 'Verify test API data against an autograder server.')

    return run(parser.parse_args())

if __name__ == '__main__':
    sys.exit(main())
