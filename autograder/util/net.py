"""
Utilities for network and HTTP.
"""

import typing

import edq.util.json
import requests

CLEAN_REMOVE_CONTENT_KEYS: typing.List[str] = [
    'source',
    'source-version',
]
""" Keys to remove from API responses. """

def clean_api_response(response: requests.Response, body: str) -> str:
    """
    Clean autograder API responses (so they can be stored consistently).
    """

    # Most responses are JSON.
    try:
        data = edq.util.json.loads(body, strict = True)
    except Exception:
        # Response is not JSON.
        return body

    # Remove any content keys.
    _recursive_remove_keys(data, set(CLEAN_REMOVE_CONTENT_KEYS))

    # Convert body back to a string.
    body = edq.util.json.dumps(data)

    return body

def _recursive_remove_keys(data: typing.Any, remove_keys: typing.Set[str]) -> None:
    """
    Recursively descend through the given and remove any instance to the given key from any dictionaries.
    The data should only be simple types (POD, dicts, lists, tuples).
    """

    if (isinstance(data, (list, tuple))):
        for item in data:
            _recursive_remove_keys(item, remove_keys)
    elif (isinstance(data, dict)):
        for key in list(data.keys()):
            if (key in remove_keys):
                del data[key]
            else:
                _recursive_remove_keys(data[key], remove_keys)
