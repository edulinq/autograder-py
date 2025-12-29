"""
Describe all endpoints on the server.
"""

import typing

import autograder.api.common
import autograder.api.config

API_ENDPOINT: str = 'metadata/describe'
API_PARAMS: typing.List[autograder.api.config.APIParam] = [
    autograder.api.config.PARAM_SERVER,

    autograder.api.config.APIParam('force_compute',
        'Force the server to compute metadata descriptions, ignoring any existing cache.',
        api_required = False,
        value_type = bool,
        cli_show_default = False,
    ),
]

def send(config: typing.Dict[str, typing.Any], **kwargs: typing.Any) -> typing.Dict[str, typing.Any]:
    """ Send a request to the autograder. """

    return autograder.api.common.make_api_request(API_ENDPOINT, config, API_PARAMS, **kwargs)
