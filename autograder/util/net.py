"""
Utilities for network and HTTP.
"""

import typing

import edq.util.json
import requests

CLEAN_REMOVE_HEADERS: typing.List[str] = [
    'access-control-allow-origin',
    'transfer-encoding',
]
""" Headers to remove from API responses. """

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

    # Convert body back to a string.
    body = edq.util.json.dumps(data)

    return body
