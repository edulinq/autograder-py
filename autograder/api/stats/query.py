"""
Query stats for the server.
"""

import typing

import autograder.api.common
import autograder.api.config
import autograder.error

API_ENDPOINT: str = 'stats/query'
API_WRITE: bool = False
API_PARAMS: typing.List[autograder.api.config.APIParam] = [
    autograder.api.config.PARAM_SERVER,
    autograder.api.config.PARAM_USER_EMAIL,
    autograder.api.config.PARAM_USER_PASS,

    autograder.api.config.PARAM_QUERY_METRIC_TYPE,
    autograder.api.config.PARAM_QUERY_LIMIT,
    autograder.api.config.PARAM_QUERY_AFTER,
    autograder.api.config.PARAM_QUERY_BEFORE,
    autograder.api.config.PARAM_QUERY_SORT,
    autograder.api.config.PARAM_QUERY_WHERE,
]

def send(config: typing.Dict[str, typing.Any], **kwargs: typing.Any) -> typing.Dict[str, typing.Any]:
    """ Send a request to the autograder. """

    return autograder.api.common.make_api_request(API_ENDPOINT, config, API_PARAMS, write = API_WRITE, **kwargs)
