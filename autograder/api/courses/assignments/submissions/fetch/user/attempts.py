"""
Get all submission attempts made by a user along with all grading information.
"""

import typing

import autograder.api.common
import autograder.api.config
import autograder.assignment

API_ENDPOINT: str = 'courses/assignments/submissions/fetch/user/attempts'
API_WRITE: bool = False
API_PARAMS: typing.List[autograder.api.config.APIParam] = [
    autograder.api.config.PARAM_SERVER,
    autograder.api.config.PARAM_USER_EMAIL,
    autograder.api.config.PARAM_USER_PASS,

    autograder.api.config.PARAM_COURSE,
    autograder.api.config.PARAM_ASSIGNMENT,

    autograder.api.config.PARAM_TARGET_EMAIL_OR_SELF,

    autograder.api.config.PARAM_OUT_DIR,
]

def send(config: typing.Dict[str, typing.Any], **kwargs: typing.Any) -> typing.Tuple[bool, typing.List[typing.Dict[str, typing.Any]]]:
    """
    Send a request to the autograder.
    Returns: (found user, attempts).
    """

    response = autograder.api.common.make_api_request(API_ENDPOINT, config, API_PARAMS, write = API_WRITE, **kwargs)

    if (not response['found-user']):
        return False, []

    return True, response['grading-results']
