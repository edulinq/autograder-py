import json
import os
import unittest
import re
import sys

import autograder.api.error
import tests.server.server

SERVER_URL_FORMAT = "http://127.0.0.1:%s"
FORMAT_STR = "\n--- Expected ---\n%s\n--- Actual ---\n%s\n---\n"

DATA_DIR_ID = tests.server.server.DATA_DIR_ID

@unittest.skipUnless(sys.platform.startswith('linux'), 'linux only (multiprocessing)')
class ServerBaseTest(unittest.TestCase):
    """
    A base tests that need to call the mock server.
    """

    maxDiff = None

    _server_process = None
    _port = None

    _base_arguments = tests.server.server.INITIAL_BASE_ARGUMENTS.copy()

    @classmethod
    def setUpClass(cls):
        cls._server_process, cls._port = tests.server.server.start()
        cls._base_arguments['server'] = SERVER_URL_FORMAT % cls._port

        # Do not actually exit on errors, raise instead.
        autograder.api.error._exit_on_error_for_testing = False

    @classmethod
    def tearDownClass(cls):
        tests.server.server.stop(cls._server_process)
        cls._server_process = None

        # Reset.
        autograder.api.error._exit_on_error_for_testing = True

    def get_base_arguments(self):
        return ServerBaseTest._base_arguments.copy()

    def assertDictEqual(self, a, b):
        a_json = json.dumps(a, indent = 4)
        b_json = json.dumps(b, indent = 4)

        super().assertDictEqual(a, b, FORMAT_STR % (a_json, b_json))

    def assertListEqual(self, a, b):
        a_json = json.dumps(a, indent = 4)
        b_json = json.dumps(b, indent = 4)

        super().assertListEqual(a, b, FORMAT_STR % (a_json, b_json))

def replace_path(text, key, base_dir):
    match = re.search(r'%s\(([^)]*)\)' % (key), text)
    if (match is not None):
        filename = match.group(1)

        # Normalize any path separators.
        filename = os.path.join(*filename.split('/'))

        if (filename == ''):
            path = base_dir
        else:
            path = os.path.join(base_dir, filename)

        text = text.replace(match.group(0), path)

    return text
