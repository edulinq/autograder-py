import os
import sys
import typing

import edq.util.json
import edq.util.net
import requests

import autograder
import autograder.api.config
import autograder.api.constants
import autograder.error
import autograder.util.timestamp

DEFAULT_SOURCE_NAME: str = 'edq-autograder-py'
DEFAULT_SOURCE_VERSION: str = autograder.__version__

TESTING_SOURCE_NAME: str = 'testing'
TESTING_SOURCE_VERSION: str = '0.0.0'

_source_name: str = DEFAULT_SOURCE_NAME
_source_version: str = DEFAULT_SOURCE_VERSION

def set_testing_source_info() -> None:
    """ Set source info for API requests to consistent values for testing. """

    global _source_name
    global _source_version

    _source_name = TESTING_SOURCE_NAME
    _source_version = TESTING_SOURCE_VERSION

def make_api_request(
        endpoint: str,
        config: typing.Dict[str, typing.Any],
        api_params: typing.List[autograder.api.config.APIParam],
        exit_on_error: bool = True,
        post_paths: typing.Union[typing.List[str], None] = None,
        ) -> typing.Dict[str, typing.Any]:
    """
    Given arguments (usually from argparse), API params, and an endpoint,
    make an API request.
    Will raise an error on any error or error response.
    """

    try:
        return _make_api_request(endpoint, config, api_params, post_paths = post_paths)
    except autograder.error.AutograderError as ex:
        if (exit_on_error):
            print("ERROR: " + ex.args[0], file = sys.stderr)
            autograder.error.exit_from_error(1)

        raise ex

def _make_api_request(
        endpoint: str,
        config: typing.Dict[str, typing.Any],
        api_params: typing.List[autograder.api.config.APIParam],
        post_paths: typing.Union[typing.List[str], None] = None,
        ) -> typing.Dict[str, typing.Any]:
    """ Wrapped function for make_api_request(). """

    payload = _verify_payload(config, api_params)

    return send_api_request(endpoint, payload, config, post_paths = post_paths)

def _verify_payload(
        raw_payload: typing.Dict[str, typing.Any],
        api_params: typing.List[autograder.api.config.APIParam],
        ) -> typing.Dict[str, typing.Any]:
    """
    Verify that the given payload matches the listed API parameters,
    and return a new copy of the payload with only the specified keys.
    """

    payload = {}

    for api_param in api_params:
        value = api_param.clean_value(raw_payload.get(api_param.config_key, None))

        if (value is None):
            if (api_param.required):
                raise autograder.error.APIError(None,
                    f"Required parameter '{param.config_key}' not found.")

            if (api_param.omit_empty):
                continue

        payload[api_param.payload_key] = value

    return payload

def send_api_request(
        endpoint: str,
        payload: typing.Dict[str, typing.Any],
        config: typing.Dict[str, typing.Any],
        post_paths: typing.Union[typing.List[str], None] = None,
        ) -> typing.Dict[str, typing.Any]:
    """
    Make an autograder API request.
    On a failure (including non 200), an error will be raised with error information.
    Otherwise (including a successful response with a failed operation (soft error)),
    the content of the response will be returned (converted from JSON to a dict).
    """

    if (post_paths is None):
        post_paths = []

    server = payload.pop('server', None)
    if (server is None):
        raise autograder.error.APIError(None, "No server provided.")

    server = server.rstrip('/')
    endpoint = endpoint.lstrip('/')

    url = "%s/api/%s/%s" % (server, autograder.api.constants.API_VERSION, endpoint)

    # Add source information.
    payload['source'] = _source_name
    payload['source-version'] = _source_version

    post_files = {}
    for path in post_paths:
        filename = os.path.basename(path)
        if (filename in post_files):
            raise autograder.error.APIError(None, "Cannot submit duplicate filenames ('%s')." % (filename))

        post_files[filename] = open(path, 'rb')

    try:
        raw_response, raw_body = edq.util.net.make_post(
            url,
            data = {autograder.api.constants.API_REQUEST_JSON_KEY: edq.util.json.dumps(payload)},
            files = post_files)
    except requests.exceptions.ConnectionError:
        raise autograder.error.ConnectionError((f"Could not connect to autograder server '{server}'."
            + " This is a networking issue (e.g., network down, server down, wrong server address), not an authentication issue."))

    for file in post_files.values():
        file.close()

    try:
        response_body = edq.util.json.loads(raw_body)
    except Exception as ex:
        raise autograder.error.APIError(None, "Autograder response does not contain valid JSON."
            + " Contact a server admin with the following. Response:\n---\n%s\n---" % (
                raw_response.text)) from ex

    if (not response_body.get(autograder.api.constants.API_RESPONSE_KEY_SUCCESS, False)):
        message = 'Request to the autograder failed.'
        if (autograder.api.constants.API_RESPONSE_KEY_MESSAGE in response_body):
            message = f"Failed to complete operation: {response_body[autograder.api.constants.API_RESPONSE_KEY_MESSAGE]}"

            # Replace any timestamps in the message.
            message = autograder.util.timestamp.convert_message(message, pretty = True)

        code = response_body.get(API_RESPONSE_KEY_STATUS, None)
        raise autograder.error.APIError(code, message)

    return response_body[autograder.api.constants.API_RESPONSE_KEY_CONTENT]
