"""
Proxy resubmit an assignment submission to the autograder.
"""

import typing

import autograder.api.common
import autograder.api.config
import autograder.assignment
import autograder.error

API_ENDPOINT: str = 'courses/assignments/submissions/proxy/resubmit'
API_WRITE: bool = True
API_PARAMS: typing.List[autograder.api.config.APIParam] = [
    autograder.api.config.PARAM_SERVER,
    autograder.api.config.PARAM_USER_EMAIL,
    autograder.api.config.PARAM_USER_PASS,

    autograder.api.config.PARAM_COURSE,
    autograder.api.config.PARAM_ASSIGNMENT,
    autograder.api.config.PARAM_TARGET_SUBMISSION_OR_RECENT,

    autograder.api.config.PARAM_PROXY_EMAIL,
    autograder.api.config.PARAM_PROXY_TIME,
]

def send(config: typing.Dict[str, typing.Any], **kwargs: typing.Any) -> typing.Tuple[
        typing.Dict[str, typing.Any], typing.Union[autograder.assignment.GradedAssignment, None]]:
    """
    Send a request to the autograder.
    Return the raw response and graded assignment (if grading was successful).
    """

    response = autograder.api.common.make_api_request(API_ENDPOINT, config, API_PARAMS, write = API_WRITE, **kwargs)

    assignment = None
    result = response.get('result', None)
    if (result is not None):
        assignment = autograder.assignment.GradedAssignment.from_dict(result)

    return response, assignment
