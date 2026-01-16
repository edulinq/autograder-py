"""
Proxy regrade an assignment for all target users using their most recent submission.
"""

import typing

import autograder.api.common
import autograder.api.config

API_ENDPOINT: str = 'courses/assignments/submissions/proxy/regrade'
API_WRITE: bool = True
API_PARAMS: typing.List[autograder.api.config.APIParam] = [
    autograder.api.config.PARAM_SERVER,
    autograder.api.config.PARAM_USER_EMAIL,
    autograder.api.config.PARAM_USER_PASS,

    autograder.api.config.PARAM_COURSE,
    autograder.api.config.PARAM_ASSIGNMENT,

    autograder.api.config.PARAM_COURSE_USER_REFERENCES,
    autograder.api.config.PARAM_REGRADE_CUTOFF,

    autograder.api.config.PARAM_DRY_RUN,
    autograder.api.config.PARAM_OVERWRITE_RECORDS,
    autograder.api.config.PARAM_WAIT_FOR_COMPLETION,
]

def send(config: typing.Dict[str, typing.Any], **kwargs: typing.Any) -> typing.Dict[str, typing.Any]:
    """ Send a request to the autograder. """

    return autograder.api.common.make_api_request(API_ENDPOINT, config, API_PARAMS, write = API_WRITE, **kwargs)
