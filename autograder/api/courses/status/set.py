"""
Set a status for this course.
"""

import typing

import autograder.api.common
import autograder.api.config
import autograder.model.config

API_ENDPOINT: str = 'courses/status/set'
API_WRITE: bool = True
API_PARAMS: typing.List[autograder.api.config.APIParam] = [
    autograder.api.config.PARAM_SERVER,
    autograder.api.config.PARAM_USER_EMAIL,
    autograder.api.config.PARAM_USER_PASS,

    autograder.api.config.PARAM_COURSE,

    autograder.api.config.PARAM_STATUS_ACTIVE,
    autograder.api.config.PARAM_STATUS_MESSAGE,
    autograder.api.config.PARAM_STATUS_FORCE,
]

def send(config: autograder.model.config.Config, **kwargs: typing.Any) -> typing.Dict[str, typing.Any]:
    """ Send a request to the autograder. """

    return autograder.api.common.make_api_request(API_ENDPOINT, config, API_PARAMS, write = API_WRITE, **kwargs)
