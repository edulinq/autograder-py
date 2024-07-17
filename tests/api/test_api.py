import glob
import json
import importlib
import os
import unittest
import sys

import tests.api.server

THIS_DIR = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
DATA_DIR = os.path.join(THIS_DIR, "data")

SERVER_URL = "http://127.0.0.1:%s" % (tests.api.server.PORT)
FORMAT_STR = "\n--- Expected ---\n%s\n--- Actual ---\n%s\n---\n"
PYTHON_ERROR_PREFIX = "Failed to complete operation: "

REWRITE_TOKEN_ID = '<TOKEN_ID>'
REWRITE_TOKEN_CLEARTEXT = '<TOKEN_CLEARTEXT>'

BASE_ARGUMENTS = {
    'user': 'admin@test.com',
    'pass': 'admin',
    'course': 'COURSE101',
    'assignment': 'hw0',

    'server': SERVER_URL,
}

@unittest.skipUnless(sys.platform.startswith('linux'), 'linux only (multiprocessing)')
class APITest(unittest.TestCase):
    """
    Test API calls by mocking a server.

    Note that the same test output is used by the server to respond to a request
    and the test to verify the output (making the equality assertion seem redundant).
    However, the autograder server will verify that the output is correct in it's own test suite.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._server_process = None

    def setUp(self):
        self._server_process, self._next_response_queue = tests.api.server.start()

    def tearDown(self):
        tests.api.server.stop(self._server_process)
        self._server_process = None

    def assertDictEqual(self, a, b):
        a_json = json.dumps(a, indent = 4)
        b_json = json.dumps(b, indent = 4)

        super().assertDictEqual(a, b, FORMAT_STR % (a_json, b_json))

def _discover_api_tests():
    for path in sorted(glob.glob(os.path.join(DATA_DIR, "**", "test_*.json"), recursive = True)):
        try:
            _add_api_test(path)
        except Exception as ex:
            raise ValueError("Failed to parse test case '%s'." % (path)) from ex

def _add_api_test(path):
    test_name = os.path.splitext(os.path.basename(path))[0]
    setattr(APITest, test_name, _get_api_test_method(path))

def get_api_test_info(path):
    with open(path, 'r') as file:
        data = json.load(file)

    import_module_name = data.get('module', None)
    if (import_module_name is None):
        parts = data['endpoint'].split('/')
        prefix = parts[0]
        suffix = ''.join(parts[1:])

        import_module_name = '.'.join(['autograder', 'api', prefix, suffix])

    arguments = BASE_ARGUMENTS.copy()
    for key, value in data.get('arguments', {}).items():
        arguments[key] = value

    output = data['output']
    is_error = output.get('error', False)

    output_modifier = clean_output_noop
    if ('output-modifier' in data):
        modifier_name = data['output-modifier']

        if (modifier_name not in globals()):
            raise ValueError("Could not find API output modifier function: '%s'." % (modifier_name))

        output_modifier = globals()[modifier_name]

    return import_module_name, arguments, data['output'], is_error, output_modifier

def _get_api_test_method(path):
    import_module_name, arguments, expected, is_error, output_modifier = get_api_test_info(path)

    def __method(self):
        api_module = importlib.import_module(import_module_name)

        self._next_response_queue.put(expected)
        try:
            actual = api_module.send(arguments)
        except Exception as ex:
            if (not is_error):
                raise ex

            message = _unpack_expected_error_message(expected)
            assert (message == str(ex))
            return

        if (is_error):
            message = _unpack_expected_error_message(expected)
            raise ValueError("No error was raised when one was expected ('%s')." % (str(message)))

        actual = output_modifier(actual)

        self.assertDictEqual(actual, expected)

    return __method

def _unpack_expected_error_message(output):
    message = output.get('message', "")
    message = PYTHON_ERROR_PREFIX + message
    return message

def clean_output_noop(output):
    return output

def clean_token(output):
    output['token-id'] = REWRITE_TOKEN_ID
    output['token-cleartext'] = REWRITE_TOKEN_CLEARTEXT

    return output

def clean_output_logs(output):
    record_set_values = {
        'unix-time': 0,
    }

    attribute_set_values = {
        'path': '/some/path/course.json'
    }

    if (output.get('results') is None):
        return output

    for record in output['results']:
        for (key, value) in record_set_values.items():
            record[key] = value

        if ('attributes' not in record):
            continue

        for (key, value) in attribute_set_values.items():
            record['attributes'][key] = value

    return output

_discover_api_tests()
