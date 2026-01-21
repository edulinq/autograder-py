"""
Query log entries from the autograder server.
"""

import typing

import autograder.api.common
import autograder.api.config
import autograder.error

API_ENDPOINT: str = 'logs/query'
API_WRITE: bool = False
API_PARAMS: typing.List[autograder.api.config.APIParam] = [
    autograder.api.config.PARAM_SERVER,
    autograder.api.config.PARAM_USER_EMAIL,
    autograder.api.config.PARAM_USER_PASS,

    autograder.api.config.PARAM_QUERY_LOG_LEVEL,
    autograder.api.config.PARAM_QUERY_AFTER,
    autograder.api.config.PARAM_QUERY_PAST,

    autograder.api.config.PARAM_QUERY_TARGET_COURSE,
    autograder.api.config.PARAM_QUERY_TARGET_ASSIGNMENT,
    autograder.api.config.PARAM_QUERY_TARGET_EMAIL,
]

def send(config: typing.Dict[str, typing.Any], **kwargs: typing.Any) -> typing.Dict[str, typing.Any]:
    """ Send a request to the autograder. """

    return autograder.api.common.make_api_request(API_ENDPOINT, config, API_PARAMS, write = API_WRITE, **kwargs)
