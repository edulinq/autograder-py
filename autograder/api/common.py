import argparse
import json
import os

import requests

import autograder.util.hash

DEFAULT_CONFIG_PATH = 'config.json'
DEFAULT_AUTOGRADER_URL = 'http://lighthouse.soe.ucsc.edu'

API_REQUEST_JSON_KEY = 'content'

API_RESPONSE_KEY_SUCCESS = 'success'
API_RESPONSE_KEY_CONTENT = 'content'

def send_api_request(url, method = None, data = {}, files = [], clean = True):
    """
    Make an API request and respond with:
     - on success -- (the response body, None)
     - on failure -- (None, a failure message)
    """

    post_files = {}
    for path in files:
        filename = os.path.basename(path)
        if (filename in post_files):
            raise ValueError("Cannot submit duplicate filenames ('%s')." % (filename))

        post_files[filename] = open(path, 'rb')

    if (method is None):
        if ((len(files) > 0) or (len(data) > 0)):
            method = 'POST'
        else:
            method = 'GET'

    if (clean):
        # Don't send cleartext passwords.
        if ('pass' in data):
            data['pass'] = autograder.util.hash.sha256_hex(data['pass'])

    raw_response = requests.request(
        method = method,
        url = url,
        data = {API_REQUEST_JSON_KEY: json.dumps(data)},
        files = post_files)

    for file in post_files.values():
        file.close()

    if (raw_response.status_code == 401):
        return None, ("Request could not be authenticated."
            + " Ensure that your username, password, and course are properly set.")

    if (raw_response.status_code == 403):
        return None, "You do not have sufficient permissions for that operation."

    if (raw_response.status_code != 200):
        return None, "Recieved a failure status from the autograding server: %d." % (
            raw_response.status_code)

    try:
        response = raw_response.json()
    except Exception:
        return None, "Autograder response does not contain valid JSON. Response:\n---\n%s\n---" % (
            raw_response.text)

    if (not response.get(API_RESPONSE_KEY_SUCCESS, False)):
        message = response.get(API_RESPONSE_KEY_CONTENT, "Request to autograding server failed.")
        return None, message

    return response.get(API_RESPONSE_KEY_CONTENT, None), None

def parse_config(arguments):
    """
    Given the standard CLI options (from get_argument_parser()),
    parse out the full API configuration.
    """

    config = {
        'user': None,
        'pass': None,
        'course': None,
        'assignment': None,
    }

    if ((arguments.config_paths is not None) and (len(arguments.config_paths) > 0)):
        for path in arguments.config_paths:
            with open(path, 'r') as file:
                config.update(json.load(file))
    elif (os.path.isfile(DEFAULT_CONFIG_PATH)):
        with open(DEFAULT_CONFIG_PATH, 'r') as file:
            config.update(json.load(file))

    for (key, value) in vars(arguments).items():
        if (key == 'config_paths'):
            continue

        if ((value is None) or (value == '')):
            continue

        config[key] = value

    return config

def get_argument_parser(
        description = 'Send an API request to the autograder.'):
    """
    Create an argparse parser that has all the standard options for API requests.
    """

    parser = argparse.ArgumentParser(description = description)

    parser.add_argument('--config', dest = 'config_paths',
        action = 'append', type = str,
        help = 'A JSON config file with your submission/authentication details.'
            + " Can be specified multiple times with later values overriding earlier ones."
            + " If not specified, '%s' will be checked." % (DEFAULT_CONFIG_PATH)
            + ' These options can be set directly using other CLI arguments.')

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

    parser.add_argument('--server', dest = 'server',
        action = 'store', type = str, default = DEFAULT_AUTOGRADER_URL,
        help = 'The URL of the server to submit to (default: %(default)s).')

    return parser
