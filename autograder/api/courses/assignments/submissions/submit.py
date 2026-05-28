"""
Submit an assignment submission to the autograder.
"""

import typing

import autograder.api.common
import autograder.api.config
import autograder.assignment
import autograder.error

# Params have been split up so others can use these base params.
BASE_API_PARAMS: typing.List[autograder.api.config.APIParam] = [
    autograder.api.config.PARAM_SERVER,
    autograder.api.config.PARAM_USER_EMAIL,
    autograder.api.config.PARAM_USER_PASS,

    autograder.api.config.PARAM_COURSE,
    autograder.api.config.PARAM_ASSIGNMENT,

    autograder.api.config.PARAM_SUBMISSION_MESSAGE,
    autograder.api.config.PARAM_ALLOW_LATE,
]

API_ENDPOINT: str = 'courses/assignments/submissions/submit'
API_WRITE: bool = True
API_PARAMS: typing.List[autograder.api.config.APIParam] = BASE_API_PARAMS + [
    autograder.api.config.PARAM_SUBMISSION_FILES,
]

def send(config: typing.Dict[str, typing.Any], post_paths: typing.Union[typing.List[str], None] = None, **kwargs: typing.Any) -> typing.Tuple[
        typing.Dict[str, typing.Any], typing.Union[autograder.assignment.GradedAssignment, None]]:
    """
    Send a request to the autograder.
    Return the raw response and graded assignment (if grading was successful).
    """

    if ((post_paths is None) or len(post_paths) == 0):
        raise autograder.error.AutograderError("No files provided for submission.")

    response = autograder.api.common.make_api_request(API_ENDPOINT, config, API_PARAMS, write = API_WRITE, post_paths = post_paths, **kwargs)

    assignment = None
    result = response.get('result', None)
    if (result is not None):
        assignment = autograder.assignment.GradedAssignment.from_dict(result)

    return response, assignment
