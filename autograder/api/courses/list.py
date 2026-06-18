"""
List the courses on a server.
"""

import typing

import autograder.api.common
import autograder.api.config
import autograder.model.config
import autograder.model.course

API_ENDPOINT: str = 'courses/list'
API_WRITE: bool = False
API_PARAMS: typing.List[autograder.api.config.APIParam] = [
    autograder.api.config.PARAM_SERVER,
    autograder.api.config.PARAM_USER_EMAIL,
    autograder.api.config.PARAM_USER_PASS,
]

def send(config: autograder.model.config.Config, **kwargs: typing.Any) -> typing.List[autograder.model.course.Course]:
    """ Send a request to the autograder. """

    response = autograder.api.common.make_api_request(API_ENDPOINT, config, API_PARAMS, write = API_WRITE, **kwargs)

    courses = []
    for raw_course in response['courses']:
        courses.append(autograder.model.course.Course.from_api(raw_course))

    return sorted(courses)
