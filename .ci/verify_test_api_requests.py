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
import subprocess
import sys
import time
import traceback

THIS_DIR = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
ROOT_DIR = os.path.join(THIS_DIR, '..')
TEST_DATA_DIR = os.path.join(ROOT_DIR, 'tests', 'api', 'testdata')

# Add in the tests path.
sys.path.append(ROOT_DIR)

import autograder.api.config
import autograder.api.courses.admin.update
import tests.api.test_api
import tests.server.base
import tests.server.server

DEFAULT_PORT = 8080

DEFAULT_DOCKER_IMAGE = 'edulinq/autograder-server-prebuilt:latest'
DOCKER_CONTAINER_NAME = 'autograder-py-verify-test-data'
DOCKER_START_SLEEP_TIME_SECS = 0.25
DOCKER_KILL_SLEEP_TIME_SECS = 0.25

def verify_test_case(cli_arguments, path):
    print("Verifying test case: '%s'." % (path))

    arguments = tests.server.server.INITIAL_BASE_ARGUMENTS.copy()
    parts = tests.api.test_api._get_api_test_info(path, arguments)
    (import_module_name, arguments, expected, is_error, output_modifier) = parts

    for key, value in vars(cli_arguments).items():
        if ((value is not None) or (value)):
            arguments[key] = value

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

    actual = output_modifier(actual)

    if (actual != expected):
        expected_json = json.dumps(expected, indent = 4)
        actual_json = json.dumps(actual, indent = 4)

        print("ERROR: Test case does not have expected content: '%s'." % (path))
        print(tests.server.base.FORMAT_STR % (expected_json, actual_json))
        return 1

    return 0

def start_server(cli_arguments):
    if (cli_arguments.docker):
        _reset_server_docker(cli_arguments, True)
    else:
        _reset_server_api(cli_arguments)

def reset_server(cli_arguments):
    if (cli_arguments.docker):
        _reset_server_docker(cli_arguments, False)
    else:
        _reset_server_api(cli_arguments)

def stop_server(cli_arguments):
    if (not cli_arguments.docker):
        return

    _run_bin(['docker', 'kill', DOCKER_CONTAINER_NAME])
    time.sleep(DOCKER_KILL_SLEEP_TIME_SECS)

# Do a soft server reset using the API to update the course.
def _reset_server_api(cli_arguments):
    arguments = tests.server.server.INITIAL_BASE_ARGUMENTS.copy()
    for key, value in vars(cli_arguments).items():
        if ((value is not None) or (value)):
            arguments[key] = value

    arguments['clear'] = True

    autograder.api.courses.admin.update.send(arguments)

# Do a hard server reset by (re)starting the docker continer.
def _reset_server_docker(cli_arguments, initial):
    base_args = [
        'docker', 'run',
        '-d', '-it', '--rm',
        '--name', DOCKER_CONTAINER_NAME,
        '-v', '/var/run/docker.sock:/var/run/docker.sock',
        '-v', '/tmp/autograder-temp/:/tmp/autograder-temp',
        '-p', '%d:%d' % (cli_arguments.port, DEFAULT_PORT),
        cli_arguments.image,
    ]

    if (initial):
        # If this is the first run, then ensure all the images are built.
        # This will speed up later resets.
        args = base_args + ['build-images', '--unit-testing']

        # Don't detach this container, wait for it to finish.
        args.remove('-d')

        print("Building Assignment Images")
        _run_bin(args)
    else:
        # Kill the previous container.
        stop_server(cli_arguments)

    args = base_args + ['server', '--unit-testing']

    _run_bin(args)
    time.sleep(DOCKER_START_SLEEP_TIME_SECS)

def _run_bin(args, cwd = '.', raise_on_error = True, print_output = False):
    try:
        subprocess.run(args, cwd = cwd, check = raise_on_error, capture_output = (not print_output))
    except subprocess.CalledProcessError as ex:
        print("--- stdout ---")
        print(ex.stdout)
        print("--------------")
        print("--- stderr ---")
        print(ex.stderr)
        print("--------------")

        raise ex

def run(arguments):
    # Override the server with the local server.
    arguments.server = "http://127.0.0.1:%d" % (arguments.port)

    error_count = 0

    # Start the API server.
    start_server(arguments)

    for path in sorted(glob.glob(os.path.join(TEST_DATA_DIR, '**', '*.json'), recursive = True)):
        try:
            error_count += verify_test_case(arguments, path)
        except Exception as ex:
            error_count += 1
            print("Error verifying test '%s'." % (path))
            traceback.print_exception(ex)

        # Reset the server after every test.
        reset_server(arguments)

    # Stop the API server.
    stop_server(arguments)

    if (error_count > 0):
        print("Found %d API test case issues." % (error_count))
    else:
        print("Found no API test case issues.")

    return error_count

def main():
    parser = autograder.api.config.get_argument_parser(
        description = ('Verify test API data against an autograder server.'
            + ' We will always try to connect to a local server (127.0.0.1),'
            + ' but the target port can be chosen with --port'))

    parser.add_argument('--port', dest = 'port',
        action = 'store', type = int, default = DEFAULT_PORT,
        help = 'The default local port to connect to (default: %(default)s).')

    parser.add_argument('--docker', dest = 'docker',
        action = 'store_true', default = False,
        help = 'Use a docker container for the serevr (will be started and restarted) (default: %(default)s).')

    parser.add_argument('--image', dest = 'image',
        action = 'store', type = str, default = DEFAULT_DOCKER_IMAGE,
        help = 'The Docker image to use (when --docker is given) (default: %(default)s).')

    return run(parser.parse_args())

if __name__ == '__main__':
    sys.exit(main())
