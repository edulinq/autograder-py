"""
Get the most recent scores for this user and assignment.
"""

import typing

import lms.model.scores

import autograder.api.common
import autograder.api.config
import autograder.model.assignment

API_ENDPOINT: str = 'courses/assignments/submissions/fetch/user/history'
API_WRITE: bool = False
API_PARAMS: typing.List[autograder.api.config.APIParam] = [
    autograder.api.config.PARAM_SERVER,
    autograder.api.config.PARAM_USER_EMAIL,
    autograder.api.config.PARAM_USER_PASS,

    autograder.api.config.PARAM_COURSE,
    autograder.api.config.PARAM_ASSIGNMENT,

    autograder.api.config.PARAM_TARGET_EMAIL_OR_SELF,
]

def send(config: typing.Dict[str, typing.Any], **kwargs: typing.Any) -> typing.Tuple[bool, typing.List[lms.model.scores.AssignmentScore]]:
    """ Send a request to the autograder. """

    response = autograder.api.common.make_api_request(API_ENDPOINT, config, API_PARAMS, write = API_WRITE, **kwargs)

    if (not response['found-user']):
        return False, []

    scores = []
    for raw_score in response['history']:
        scores.append(autograder.model.assignment.make_assignment_score(raw_score))

    return True, sorted(scores)
