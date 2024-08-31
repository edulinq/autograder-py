import json
import unittest
import sys

import tests.server.server

SERVER_URL_FORMAT = "http://127.0.0.1:%s"
FORMAT_STR = "\n--- Expected ---\n%s\n--- Actual ---\n%s\n---\n"

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

    @classmethod
    def tearDownClass(cls):
        tests.server.server.stop(cls._server_process)
        cls._server_process = None

    def get_base_arguments(self):
        return ServerBaseTest._base_arguments.copy()

    def assertDictEqual(self, a, b):
        a_json = json.dumps(a, indent = 4)
        b_json = json.dumps(b, indent = 4)

        super().assertDictEqual(a, b, FORMAT_STR % (a_json, b_json))