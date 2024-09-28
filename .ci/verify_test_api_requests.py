#!/usr/bin/env python3

"""
Verify test API data against an autograder server.

To verify the test data, we will need to send requests to an autograder server.
There are three methods that can be used to specify a server.
 1) --web can be used to contact an already running server on localhost (127.0.0.1).
    This method is the fastest, but will result in tests failing
    since the database will not be reset between tests.
 2) --source-dir can be used to point to a directory containing the source code for the server.
    `go run cmd/server/main.go --unit-testing` will be run in that directory to start the server,
    and SIGINT will be sent to the server to stop it.
    This method will not produce false negative, but requires the ability to build from source.
 3) --docker can be used to run the sever via using a docker image.
    This is the slowest of the methods, but should also be the most portable.
"""

import argparse
import glob
import importlib
import json
import os
import sys
import traceback

THIS_DIR = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
ROOT_DIR = os.path.join(THIS_DIR, '..')
TEST_DATA_DIR = os.path.join(ROOT_DIR, 'tests', 'api', 'testdata')

# Add in the root path.
sys.path.append(ROOT_DIR)

import backend
import tests.api.test_api
import tests.server.base
import util

def verify_test_case(server, path):
    print("Verifying test case: '%s'." % (path))

    arguments = util.build_api_args(server)
    parts = tests.api.test_api._get_api_test_info(path, arguments)
    (import_module_name, arguments, expected, is_error, read_write, output_modifier) = parts

    api_module = importlib.import_module(import_module_name)

    try:
        actual = api_module.send(arguments)

        if (is_error):
            print("ERROR: Test case does not raise an error when one was expected: '%s'." % (path))
            return 1
    except Exception as ex:
        if (not is_error):
            raise ex

        python_message = expected.get("python-message", "")
        if (python_message != str(ex)):
            print("ERROR: Test case does not raise the expected error: '%s'." % (path))
            print(tests.server.base.FORMAT_STR % (python_message, str(ex)))
            return 1

        code = expected.get("code", None)
        if (code != ex.code):
            print("ERROR: Test case has an unexpected error code: '%s'." % (path))
            print(tests.server.base.FORMAT_STR % (code, ex.code))
            return 1

        return 0
    finally:
        # Ensure that tests that write data reset the server.
        if (read_write):
            server.reset()

    actual = output_modifier(actual)

    if (actual != expected):
        expected_json = json.dumps(expected, indent = 4)
        actual_json = json.dumps(actual, indent = 4)

        print("ERROR: Test case does not have expected content: '%s'." % (path))
        print(tests.server.base.FORMAT_STR % (expected_json, actual_json))
        return 1

    return 0

def run(arguments):
    server = backend.WebServer(port = arguments.port)
    if (arguments.docker):
        server = backend.DockerServer(port = arguments.port, image = arguments.image)
    elif (arguments.source_dir is not None):
        server = backend.SourceServer(port = arguments.port, source_dir = arguments.source_dir)

    error_count = 0

    # Start the API server.
    server.start()

    for path in sorted(glob.glob(os.path.join(TEST_DATA_DIR, '**', '*.json'), recursive = True)):
        try:
            error_count += verify_test_case(server, path)
        except Exception as ex:
            error_count += 1
            print("Error verifying test '%s'." % (path))
            traceback.print_exception(ex)

    # Stop the API server.
    server.stop()

    if (error_count > 0):
        print("Found %d API test case issues." % (error_count))
    else:
        print("Found no API test case issues.")

    return error_count

def main():
    parser = argparse.ArgumentParser(
            description = __doc__.strip(),
            formatter_class = argparse.RawTextHelpFormatter)

    # Only one server method can be chosen.
    group = parser.add_mutually_exclusive_group(required = True)

    group.add_argument('--web', dest = 'web',
        action = 'store_true', default = False,
        help = 'Use an already running server (default: %(default)s).')

    group.add_argument('--docker', dest = 'docker',
        action = 'store_true', default = False,
        help = 'Use a docker container for the server (will be started and restarted) (default: %(default)s).')

    group.add_argument('--source-dir', dest = 'source_dir',
        action = 'store', type = str, default = None,
        help = 'Use a server build from this source directory (default: %(default)s).')

    # Supporting options.

    parser.add_argument('--port', dest = 'port',
        action = 'store', type = int, default = backend.DEFAULT_PORT,
        help = 'The local port to connect to (default: %(default)s).')

    parser.add_argument('--image', dest = 'image',
        action = 'store', type = str, default = backend.DEFAULT_DOCKER_IMAGE,
        help = 'The Docker image to use (when --docker is given) (default: %(default)s).')

    return run(parser.parse_args())

if __name__ == '__main__':
    sys.exit(main())
