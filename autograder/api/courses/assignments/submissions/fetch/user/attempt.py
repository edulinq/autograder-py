"""
Get a submission along with all grading information.
"""

import typing

import autograder.api.common
import autograder.api.config
import autograder.assignment

API_ENDPOINT: str = 'courses/assignments/submissions/fetch/user/attempt'
API_WRITE: bool = False
API_PARAMS: typing.List[autograder.api.config.APIParam] = [
    autograder.api.config.PARAM_SERVER,
    autograder.api.config.PARAM_USER_EMAIL,
    autograder.api.config.PARAM_USER_PASS,

    autograder.api.config.PARAM_COURSE,
    autograder.api.config.PARAM_ASSIGNMENT,

    autograder.api.config.PARAM_TARGET_EMAIL_OR_SELF,
    autograder.api.config.PARAM_TARGET_SUBMISSION_OR_RECENT,

    autograder.api.config.PARAM_OUT_DIR,
]

def send(config: typing.Dict[str, typing.Any], **kwargs: typing.Any) -> typing.Tuple[
        bool, bool, typing.Union[typing.Dict[str, typing.Any], None]]:
    """
    Send a request to the autograder.
    Returns: (found user, found submission, attempt).
    """

    response = autograder.api.common.make_api_request(API_ENDPOINT, config, API_PARAMS, write = API_WRITE, **kwargs)

    if (not response['found-user']):
        return False, False, None

    if (not response['found-submission']):
        return True, False, None

    return True, True, response['grading-result']
