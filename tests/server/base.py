import os
import re

import autograder.error
import tests.server.server
import tests.base

SERVER_URL_FORMAT = "http://127.0.0.1:%s"
FORMAT_STR = "\n--- Expected ---\n%s\n--- Actual ---\n%s\n---\n"

DATA_DIR_ID = tests.server.server.DATA_DIR_ID

class ServerBaseTest(tests.base.BaseTest):
    """
    A base tests that need to call the mock server.
    """

    _server_process = None
    _port = None

    _base_arguments = tests.server.server.INITIAL_BASE_ARGUMENTS.copy()

    @classmethod
    def setUpClass(cls):
        cls._server_process, cls._port = tests.server.server.start()
        cls._base_arguments['server'] = SERVER_URL_FORMAT % cls._port

        # Do not actually exit on errors, raise instead.
        autograder.error._exit_on_error_for_testing = False

    @classmethod
    def tearDownClass(cls):
        tests.server.server.stop(cls._server_process)
        cls._server_process = None

        # Reset.
        autograder.error._exit_on_error_for_testing = True

    def get_base_arguments(self):
        return ServerBaseTest._base_arguments.copy()

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
