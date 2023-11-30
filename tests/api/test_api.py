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
    for path in glob.glob(os.path.join(DATA_DIR, "**", "test_*.json"), recursive = True):
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

    parts = data['endpoint'].split('/')
    prefix = parts[0]
    suffix = ''.join(parts[1:])

    import_module_name = '.'.join(['autograder', 'api', prefix, suffix])
    expected = data['output']

    arguments = BASE_ARGUMENTS.copy()
    for key, value in data.get('arguments', {}).items():
        arguments[key] = value

    return import_module_name, arguments, expected

def _get_api_test_method(path):
    import_module_name, arguments, expected = get_api_test_info(path)

    def __method(self):
        api_module = importlib.import_module(import_module_name)

        self._next_response_queue.put(expected)
        actual = api_module.send(arguments)

        self.assertDictEqual(actual, expected)

    return __method

_discover_api_tests()
