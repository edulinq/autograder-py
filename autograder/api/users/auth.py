"""
Authenticate as a user.
"""

import typing

import autograder.api.common
import autograder.api.config
import autograder.model.config
import autograder.model.user

API_ENDPOINT: str = 'users/auth'
API_WRITE: bool = False
API_PARAMS: typing.List[autograder.api.config.APIParam] = [
    autograder.api.config.PARAM_SERVER,
    autograder.api.config.PARAM_USER_EMAIL,
    autograder.api.config.PARAM_USER_PASS,
]

def send(config: autograder.model.config.Config, **kwargs: typing.Any) -> bool:
    """ Send a request to the autograder. """

    results = autograder.api.common.make_api_request(API_ENDPOINT, config, API_PARAMS, write = API_WRITE, **kwargs)
    return bool(results.get('success', False))
