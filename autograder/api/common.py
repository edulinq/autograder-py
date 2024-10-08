import json
import os
import sys

import requests

import autograder.api.config
import autograder.api.constants
import autograder.error
import autograder.util.timestamp

def handle_api_request(arguments, params, endpoint, exit_on_error = False, files = []):
    """
    Given arguments (usually from argparse), API params, and an endpoint,
    make an API request.
    Will raise an error on any error or error response.
    """

    try:
        return _handle_api_request(arguments, params, endpoint, exit_on_error, files)
    except autograder.error.AutograderError as ex:
        if (exit_on_error):
            print("ERROR: " + ex.args[0], file = sys.stderr)
            autograder.error.exit_from_error(1)

        raise ex

def _handle_api_request(arguments, params, endpoint, exit_on_error, files):
    config = autograder.api.config.get_tiered_config(arguments)
    data, extra = autograder.api.config.parse_api_config(config, params,
            exit_on_error = exit_on_error)

    return send_api_request(endpoint, data = data, files = files, **extra)

def send_api_request(endpoint, server = None, verbose = False, data = {}, files = [], **kwargs):
    """
    Make an autograder API request.
    On a failure statue, an error will be raised with error information.
    Otherwise (including a successful response with a failed operation (soft error)),
    the content of the response will be returned.
    """

    if ((server is None) or (server == '')):
        raise autograder.error.APIError(None, "No server provided.")

    server = server.rstrip('/')
    endpoint = endpoint.lstrip('/')

    url = "%s/api/%s/%s" % (server, autograder.api.constants.API_VERSION, endpoint)

    post_files = {}
    for path in files:
        filename = os.path.basename(path)
        if (filename in post_files):
            raise autograder.error.APIError(None, "Cannot submit duplicate filenames ('%s')."
                % (filename))

        post_files[filename] = open(path, 'rb')

    if (verbose):
        print("\nAutograder Request Data:\n---\n%s\n---\n" % (json.dumps(data, indent = 4)))

    try:
        raw_response = requests.request(
            method = 'POST',
            url = url,
            data = {autograder.api.constants.API_REQUEST_JSON_KEY: json.dumps(data)},
            files = post_files)
    except requests.exceptions.ConnectionError:
        raise autograder.error.ConnectionError(("Could not connect to autograder server"
            + " '%s'." % (server)
            + " This is a networking issue"
            + " (e.g., network down, server down, wrong server address),"
            + " not an authentication issue."))

    for file in post_files.values():
        file.close()

    try:
        response = raw_response.json()
    except Exception as ex:
        raise autograder.error.APIError(None, "Autograder response does not contain valid JSON."
            + " Contact a server admin with the following. Response:\n---\n%s\n---" % (
                raw_response.text)) from ex

    if (verbose):
        print("\nAutograder Response:\n---\n%s\n---\n" % (json.dumps(response, indent = 4)))

    if (not response.get(autograder.api.constants.API_RESPONSE_KEY_SUCCESS, False)):
        message = 'Request to the autograder failed.'
        if (autograder.api.constants.API_RESPONSE_KEY_MESSAGE in response):
            message = ("Failed to complete operation: %s" %
                response[autograder.api.constants.API_RESPONSE_KEY_MESSAGE])

            # Replace any timestamps in the message.
            message = autograder.util.timestamp.convert_message(message, pretty = True)

        code = response.get("status", None)
        raise autograder.error.APIError(code, message)

    return response[autograder.api.constants.API_RESPONSE_KEY_CONTENT]
