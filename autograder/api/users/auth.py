"""
Authenticate as a user.
"""

import typing

import lms.model.users

import autograder.api.common
import autograder.api.config
import autograder.api.model

API_ENDPOINT: str = 'users/auth'
API_WRITE: bool = False
API_PARAMS: typing.List[autograder.api.config.APIParam] = [
    autograder.api.config.PARAM_SERVER,
    autograder.api.config.PARAM_USER_EMAIL,
    autograder.api.config.PARAM_USER_PASS,
]

def send(config: typing.Dict[str, typing.Any], **kwargs: typing.Any) -> typing.Union[lms.model.users.ServerUser, None]:
    """ Send a request to the autograder. """

    results = autograder.api.common.make_api_request(API_ENDPOINT, config, API_PARAMS, write = API_WRITE, **kwargs)
    return results.get('success', False)
