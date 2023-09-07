import argparse
import json
import os
import sys

import requests

import autograder.assignment

DEFAULT_CONFIG_PATH = 'config.json'
DEFAULT_AUTOGRADER_URL = 'http://sozopol.soe.ucsc.edu:12345'

API_ENDPOINT_SUBMIT = '/api/v01/submit'

API_REQUEST_JSON_KEY = 'content'

API_RESPONSE_KEY_SUCCESS = 'success'
API_RESPONSE_KEY_CONTENT = 'content'

API_SUBMIT_KEYS = ['user', 'pass', 'course', 'assignment', 'message']

def send_api_request(url, method = None, data = {}, files = []):
    post_files = {}
    for path in files:
        filename = os.path.basename(path)
        if (filename in post_files):
            raise ValueError("Cannot submit duplicate filenames ('%s')." % (filename))

        post_files[filename] = open(path, 'rb')

    if (method is None):
        if (len(files) > 0):
            method = 'POST'
        else:
            method = 'GET'

    raw_response = requests.request(
        method = method,
        url = url,
        data = {API_REQUEST_JSON_KEY: json.dumps(data)},
        files = post_files)

    for file in post_files.values():
        file.close()

    if (raw_response.status_code == 401):
        return None, "Request could not be authenticated. Ensure that your username, password, and course are properly set."

    if (raw_response.status_code != 200):
        return None, "Recieved a failure status from the autograding server: %d." % (raw_response.status_code)

    try:
        response = raw_response.json()
    except:
        return None, "Autograder response body does not contain valid JSON. Response:\n---\n%s\n---" % (raw_response.text)

    if (not response.get(API_RESPONSE_KEY_SUCCESS, False)):
        message = response.get(API_RESPONSE_KEY_CONTENT, "Request to autograding server failed.")
        return None, message

    return response.get(API_RESPONSE_KEY_CONTENT, None), None

def parse_config(arguments):
    """
    Given the standard CLI options, parse out the full submission configuration.
    """

    config = {
        'user': None,
        'pass': None,
        'course': None,
        'assignment': None,
        'message': '',
    }

    if (arguments.config_path is not None):
        with open(arguments.config_path, 'r') as file:
            config.update(json.load(file))
    elif (os.path.isfile(DEFAULT_CONFIG_PATH)):
        with open(arguments.config_path, 'r') as file:
            config.update(json.load(file))

    config.update(vars(arguments))

    return config

def run(arguments):
    url = "%s%s" % (arguments.server, API_ENDPOINT_SUBMIT)

    config_data = parse_config(arguments)

    data = {}
    for key in API_SUBMIT_KEYS:
        if (config_data.get(key) is None):
            print("Missing required config '%s'." % (key))
            return 1

        data[key] = config_data[key]

    body, message = send_api_request(url, data = data, files = arguments.files)

    if (body is None):
        print('The autograder failed to grade your assignment.')
        print('Message from the autograder: ' + message)
        return 10

    result = autograder.assignment.GradedAssignment.from_dict(body['result'])

    print('The autograder successfully graded your assignment.')
    print(result.report())

    return 0

def _load_args():
    parser = argparse.ArgumentParser(description =
        'Send a submission (a collection of files) to an autograding server.')

    parser.add_argument('--config', dest = 'config_path',
        action = 'store', type = str, default = None,
        help = 'A JSON config file with your submission/authentication details.' +
               " If not specified, '%s' will be checked." % (DEFAULT_CONFIG_PATH) +
               ' These options can be set directly using other CLI arguments.')

    parser.add_argument('--user', dest = 'user',
        action = 'store', type = str, default = None,
        help = 'username')

    parser.add_argument('--pass', dest = 'pass',
        action = 'store', type = str, default = None,
        help = 'password')

    parser.add_argument('--course', dest = 'course',
        action = 'store', type = str, default = None,
        help = 'course')

    parser.add_argument('--assignment', dest = 'assignment',
        action = 'store', type = str, default = None,
        help = 'assignment')

    parser.add_argument('--message', dest = 'message',
        action = 'store', type = str, default = '',
        help = 'message')

    parser.add_argument('--server', dest = 'server',
        action = 'store', type = str, default = DEFAULT_AUTOGRADER_URL,
        help = 'The URL of the server to submit to (default: %(default)s).')

    parser.add_argument('files', metavar = 'FILE',
        action = 'store', type = str, nargs = '+',
        help = 'The path to your submission file.')

    return parser.parse_args()

def main():
    return run(_load_args())

if (__name__ == '__main__'):
    sys.exit(main())
