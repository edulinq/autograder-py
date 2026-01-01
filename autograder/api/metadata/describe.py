"""
Describe all endpoints on the server.
"""

import typing

import autograder.api.common
import autograder.api.config

API_ENDPOINT: str = 'metadata/describe'
API_PARAMS: typing.List[autograder.api.config.APIParam] = [
    autograder.api.config.PARAM_SERVER,
    autograder.api.config.PARAM_FORCE_COMPUTE,
]

def send(config: typing.Dict[str, typing.Any], **kwargs: typing.Any) -> typing.Dict[str, typing.Any]:
    """ Send a request to the autograder. """

    return autograder.api.common.make_api_request(API_ENDPOINT, config, API_PARAMS, **kwargs)
