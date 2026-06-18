"""
Remove a specified submission.
Defaults to the most recent submission.
"""

import typing

import autograder.api.common
import autograder.api.config
import autograder.assignment
import autograder.model.config

API_ENDPOINT: str = 'courses/assignments/submissions/remove'
API_WRITE: bool = True
API_PARAMS: typing.List[autograder.api.config.APIParam] = [
    autograder.api.config.PARAM_SERVER,
    autograder.api.config.PARAM_USER_EMAIL,
    autograder.api.config.PARAM_USER_PASS,

    autograder.api.config.PARAM_COURSE,
    autograder.api.config.PARAM_ASSIGNMENT,

    autograder.api.config.PARAM_TARGET_EMAIL_OR_SELF,
    autograder.api.config.PARAM_TARGET_SUBMISSION_OR_RECENT,
]

def send(config: autograder.model.config.Config, **kwargs: typing.Any) -> typing.Tuple[bool, bool]:
    """
    Send a request to the autograder.
    Returns: (found user, found submission)
    """

    response = autograder.api.common.make_api_request(API_ENDPOINT, config, API_PARAMS, write = API_WRITE, **kwargs)
    return response['found-user'], response['found-submission']
