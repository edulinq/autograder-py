"""
Get all recent submissions and grading information for this assignment.
"""

import typing

import autograder.api.common
import autograder.api.config
import autograder.assignment
import autograder.model.config

API_ENDPOINT: str = 'courses/assignments/submissions/fetch/course/attempts'
API_WRITE: bool = False
API_PARAMS: typing.List[autograder.api.config.APIParam] = [
    autograder.api.config.PARAM_SERVER,
    autograder.api.config.PARAM_USER_EMAIL,
    autograder.api.config.PARAM_USER_PASS,

    autograder.api.config.PARAM_COURSE,
    autograder.api.config.PARAM_ASSIGNMENT,

    autograder.api.config.PARAM_COURSE_USER_REFERENCES,

    autograder.api.config.PARAM_OUT_DIR,
]

def send(config: autograder.model.config.Config, **kwargs: typing.Any) -> typing.Dict[str, typing.Dict[str, typing.Any]]:
    """
    Send a request to the autograder.
    Return a map of grading results keyed by user email.
    """

    response = autograder.api.common.make_api_request(API_ENDPOINT, config, API_PARAMS, write = API_WRITE, **kwargs)
    return typing.cast(typing.Dict[str, typing.Dict[str, typing.Any]], response['grading-results'])
