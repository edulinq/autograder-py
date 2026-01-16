"""
Utilities for network and HTTP.
"""

import typing

import edq.util.json
import requests

import autograder.api.constants
import autograder.testing.asserts

CLEAN_REMOVE_HEADERS: typing.Set[str] = {
    'access-control-allow-origin',
    'transfer-encoding',
}
""" Headers to remove from API responses. """

GRADING_ENDPOINTS: typing.Set[str] = {
    'courses/assignments/submissions/submit',
}
"""
These endpoints need to have additional timestamps normalized.
Note that the endpoint constants are copied to avoid cyclic dependencies.
"""

FULL_NORMALIZE_TIMESTAMP_KEYS: typing.Set[str] = autograder.testing.asserts.NORMALIZE_TIMESTAMP_KEYS | {
    'grading_end_time',
    'grading_start_time',
}
""" Keys for timestamp values to normalize. """

def clean_api_response(response: requests.Response, body: str) -> str:
    """
    Clean autograder API responses (so they can be stored consistently).
    """

    # Clean response headers.
    for header in CLEAN_REMOVE_HEADERS:
        response.headers.pop(header, None)

    # Most responses are JSON.
    try:
        data = edq.util.json.loads(body, strict = True)
    except Exception:
        # Response is not JSON.
        return body

    # Standardize top-level (metadata) keys.
    data['start-timestamp'] = 0
    data['end-timestamp'] = 0
    data['id'] = '00000000-0000-0000-0000-000000000000'

    # Standardize content keys.

    content = data.get('content', None)
    if (content is not None):
        if ('token-id' in content):
            content['token-id'] = autograder.testing.asserts.TEST_TOKEN_ID

        if ('token-cleartext' in content):
            content['token-cleartext'] = autograder.testing.asserts.TEST_TOKEN_CLEARTEXT

    # Clean specific timestamps.

    endpoint = response.url.strip().split(f"api/{autograder.api.constants.API_VERSION}/")[-1]

    timestamp_keys = autograder.testing.asserts.NORMALIZE_TIMESTAMP_KEYS
    if (endpoint in GRADING_ENDPOINTS):
        timestamp_keys = FULL_NORMALIZE_TIMESTAMP_KEYS

    data = autograder.testing.asserts._normalize_timestamps(data, keys = timestamp_keys)

    # Endpoint-Specific Tasks

    if (endpoint in GRADING_ENDPOINTS):
        # Normalize submission IDs.
        if (content is not None):
            result = content.get('result', None)
            if (result is not None):
                parts = result['id'].split('::')
                parts[3] = str(autograder.testing.asserts.TEST_TIMESTAMP)
                result['id'] = '::'.join(parts)

    # Convert body back to a string.
    body = edq.util.json.dumps(data)

    return body
