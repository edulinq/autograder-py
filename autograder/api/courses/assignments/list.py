"""
List the assignments in a course.
"""

import typing

import lms.model.assignments

import autograder.api.common
import autograder.api.config
import autograder.model.assignment
import autograder.model.config

API_ENDPOINT: str = 'courses/assignments/list'
API_WRITE: bool = False
API_PARAMS: typing.List[autograder.api.config.APIParam] = [
    autograder.api.config.PARAM_SERVER,
    autograder.api.config.PARAM_COURSE,
    autograder.api.config.PARAM_USER_EMAIL,
    autograder.api.config.PARAM_USER_PASS,
]

def send(config: autograder.model.config.Config, **kwargs: typing.Any) -> typing.List[lms.model.assignments.Assignment]:
    """ Send a request to the autograder. """

    response = autograder.api.common.make_api_request(API_ENDPOINT, config, API_PARAMS, write = API_WRITE, **kwargs)

    assignments = []
    for raw_assignment in response['assignments']:
        assignments.append(autograder.model.assignment.make_assignment(raw_assignment))

    return sorted(assignments)