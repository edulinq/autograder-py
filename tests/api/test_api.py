import glob
import json
import importlib
import os
import re

import tests.server.base

THIS_DIR = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
TEST_CASES_DIR = os.path.join(THIS_DIR, "testdata")
DATA_DIR = os.path.join(THIS_DIR, '..', "data")

REWRITE_TOKEN_ID = '<TOKEN_ID>'
REWRITE_TOKEN_CLEARTEXT = '<TOKEN_CLEARTEXT>'

SUBMISSION_ID_PATTERN = r'\b\d{10}\b'
SUBMISSION_ID_REPLACEMENT = '1234567890'

TIMESTAMP_PATTERN = r'\b\d{13}\b'
TIMESTAMP_REPLACEMENT = '1234567890123'

TIME_DELTA_PATTERN = r'(\d+h)?(\d+m)?(\d+\.)?(\d+[mun]?s)'
TIME_DELTA_REPLACEMENT = '<time-delta:1234567890123>'

TIME_MESSAGE_PATTERN = r'<timestamp:(-?\d+|nil)>'
TIME_MESSAGE_REPLACEMENT = '<timestamp:1234567890123>'

class APITest(tests.server.base.ServerBaseTest):
    """
    Test API calls by mocking a server.

    Note that the same test output is used by the server to respond to a request
    and the test to verify the output (making the equality assertion seem redundant).
    However, the autograder server will verify that the output is correct in it's own test suite.
    """

    def _get_test_info(self, path):
        return _get_api_test_info(path, self.get_base_arguments())

def _get_api_test_info(path, arguments):
    with open(path, 'r') as file:
        data = json.load(file)

    import_module_name = data.get('module', None)
    if (import_module_name is None):
        raise ValueError("Could not find API test module.")

    for key, value in data.get('arguments', {}).items():
        arguments[key] = value

    files = data.get('files', [])
    for i in range(len(files)):
        path = files[i]
        files[i] = tests.server.base.replace_path(path, tests.server.base.DATA_DIR_ID, DATA_DIR)

    is_error = data.get('error', False)
    read_write = data.get('read-write', False)

    output = data['output']

    output_modifier = clean_output_noop
    if ('output-modifier' in data):
        modifier_name = data['output-modifier']

        if (modifier_name not in globals()):
            raise ValueError("Could not find API output modifier function: '%s'." % (
                modifier_name))

        output_modifier = globals()[modifier_name]

    return import_module_name, arguments, files, output, is_error, read_write, output_modifier

def _discover_api_tests():
    for path in sorted(glob.glob(os.path.join(TEST_CASES_DIR, "**", "*.json"), recursive = True)):
        try:
            _add_api_test(path)
        except Exception as ex:
            raise ValueError("Failed to parse test case '%s'." % (path)) from ex

def _add_api_test(path):
    test_name = os.path.splitext(os.path.basename(path))[0]
    setattr(APITest, 'test_api__' + test_name, _get_api_test_method(path))

def _get_api_test_method(path):
    def __method(self):
        parts = self._get_test_info(path)
        (module_name, arguments, files, expected, is_error, read_write, output_modifier) = parts

        api_module = importlib.import_module(module_name)

        try:
            actual = api_module.send(arguments, files = files)
        except Exception as ex:
            if (not is_error):
                raise ex

            python_message = expected.get('python-message', "")
            self.assertEqual(python_message, str(ex))

            code = expected.get('code', None)
            self.assertEqual(code, ex.code)

            return

        if (is_error):
            self.fail("Test case does not raise an error when one was expected: '%s'." % (path))
            return

        actual = output_modifier(actual)

        self.assertDictEqual(actual, expected)

    return __method

def clean_output_noop(output):
    return output

def clean_output_timestamps(output):
    # Convert the output to JSON so we can do a simple find/replace for all timestamps-like things.
    text_output = json.dumps(output)

    text_output = re.sub(TIMESTAMP_PATTERN, TIMESTAMP_REPLACEMENT, text_output)
    text_output = re.sub(TIME_DELTA_PATTERN, TIME_DELTA_REPLACEMENT, text_output)
    text_output = re.sub(TIME_MESSAGE_PATTERN, TIME_MESSAGE_REPLACEMENT, text_output)

    return json.loads(text_output)

def clean_output_timestamps_and_submission_ids(output):
    output = clean_output_timestamps(output)

    # Convert the output to JSON so we can do a simple find/replace for all timestamps-like things.
    text_output = json.dumps(output)

    text_output = re.sub(SUBMISSION_ID_PATTERN, SUBMISSION_ID_REPLACEMENT, text_output)

    return json.loads(text_output)

def clean_token(output):
    output['token-id'] = REWRITE_TOKEN_ID
    output['token-cleartext'] = REWRITE_TOKEN_CLEARTEXT

    return output

def clean_output_logs(output):
    record_set_values = {
        'timestamp': 0,
    }

    attribute_set_values = {
        'path': '/some/path/course.json',
        'unix_socket': '/tmp/autograder.sock',
        'port': 8080,
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

    # Sort the output for consistency.
    output['results'] = sorted(output['results'], key = lambda record: record['message'])

    return output

def fake_system_stats(output):
    """
    Because of the variable and fine-grained level of system stats,
    the entire output must be faked.
    """

    return {
        "results": [
            {
                "timestamp": 100,
                "cpu-percent": 1,
                "mem-percent": 1,
                "net-bytes-sent": 1,
                "net-bytes-received": 1,
            },
            {
                "timestamp": 200,
                "cpu-percent": 2,
                "mem-percent": 2,
                "net-bytes-sent": 2,
                "net-bytes-received": 2,
            },
            {
                "timestamp": 300,
                "cpu-percent": 3,
                "mem-percent": 3,
                "net-bytes-sent": 3,
                "net-bytes-received": 3,
            },
        ],
    }

def fake_course_stats(output):
    """
    Because of the variable and fine-grained level of course stats,
    the entire output must be faked.
    """

    return {
        "results": [
            {
                "timestamp": 100,
                "type": "grading-time",
                "course": "course101",
                "assignment": "hw0",
                "user": "server-admin@test.edulinq.org",
                "duration": 100
            },
            {
                "timestamp": 200,
                "type": "grading-time",
                "course": "course101",
                "assignment": "hw0",
                "user": "server-admin@test.edulinq.org",
                "duration": 200
            }
        ]
    }

_discover_api_tests()
