"""
Get the most recent scores for this assignment.
"""

import typing

import lms.model.scores

import autograder.api.common
import autograder.api.config
import autograder.model.assignment

API_ENDPOINT: str = 'courses/assignments/submissions/fetch/course/scores'
API_WRITE: bool = False
API_PARAMS: typing.List[autograder.api.config.APIParam] = [
    autograder.api.config.PARAM_SERVER,
    autograder.api.config.PARAM_USER_EMAIL,
    autograder.api.config.PARAM_USER_PASS,

    autograder.api.config.PARAM_COURSE,
    autograder.api.config.PARAM_ASSIGNMENT,

    autograder.api.config.PARAM_COURSE_USER_REFERENCES,
]

def send(config: typing.Dict[str, typing.Any], **kwargs: typing.Any) -> typing.List[lms.model.scores.AssignmentScore]:
    """ Send a request to the autograder. """

    response = autograder.api.common.make_api_request(API_ENDPOINT, config, API_PARAMS, write = API_WRITE, **kwargs)

    assignment_id = config.get(autograder.api.config.PARAM_ASSIGNMENT.config_key, None)

    scores = []
    for (user_email, raw_score) in response['submission-infos'].items():
        if (raw_score is None):
            scores.append(lms.model.scores.AssignmentScore(assignment = assignment_id, user = user_email))
        else:
            scores.append(autograder.model.assignment.make_assignment_score(raw_score))

    return sorted(scores)
