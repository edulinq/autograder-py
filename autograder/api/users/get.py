"""
Get information about a server user.
"""

import typing

import lms.model.users

import autograder.api.common
import autograder.api.config
import autograder.model.user

API_ENDPOINT: str = 'users/get'
API_WRITE: bool = False
API_PARAMS: typing.List[autograder.api.config.APIParam] = [
    autograder.api.config.PARAM_SERVER,
    autograder.api.config.PARAM_USER_EMAIL,
    autograder.api.config.PARAM_USER_PASS,

    autograder.api.config.PARAM_TARGET_EMAIL_OR_SELF,
]

def send(config: typing.Dict[str, typing.Any], **kwargs: typing.Any) -> typing.Union[lms.model.users.ServerUser, None]:
    """ Send a request to the autograder. """

    response = autograder.api.common.make_api_request(API_ENDPOINT, config, API_PARAMS, write = API_WRITE, **kwargs)

    if (not response.get('found', False)):
        return None

    return autograder.model.user.make_server_user(response['user'])
