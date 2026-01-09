"""
Get the result of a pairwise analysis for the specified submissions.
"""

import typing

import autograder.api.common
import autograder.api.config

API_ENDPOINT: str = 'courses/assignments/submissions/analysis/pairwise'
API_WRITE: bool = True
API_PARAMS: typing.List[autograder.api.config.APIParam] = [
    autograder.api.config.PARAM_SERVER,
    autograder.api.config.PARAM_USER_EMAIL,
    autograder.api.config.PARAM_USER_PASS,

    autograder.api.config.PARAM_SUBMISSION_SPECS,

    autograder.api.config.PARAM_DRY_RUN,
    autograder.api.config.PARAM_OVERWRITE_RECORDS,
    autograder.api.config.PARAM_WAIT_FOR_COMPLETION,
]

def send(config: typing.Dict[str, typing.Any], **kwargs: typing.Any) -> typing.Dict[str, typing.Any]:
    """ Send a request to the autograder. """

    return autograder.api.common.make_api_request(API_ENDPOINT, config, API_PARAMS, write = API_WRITE, **kwargs)
