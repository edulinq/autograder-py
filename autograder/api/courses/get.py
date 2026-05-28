"""
Get a course on a server.
"""

import typing

import autograder.api.common
import autograder.api.config
import autograder.model.course

API_ENDPOINT: str = 'courses/get'
API_WRITE: bool = False
API_PARAMS: typing.List[autograder.api.config.APIParam] = [
    autograder.api.config.PARAM_SERVER,
    autograder.api.config.PARAM_COURSE,
    autograder.api.config.PARAM_USER_EMAIL,
    autograder.api.config.PARAM_USER_PASS,
]

def send(config: typing.Dict[str, typing.Any], **kwargs: typing.Any) -> typing.Union[autograder.model.course.Course, None]:
    """ Send a request to the autograder. """

    response = autograder.api.common.make_api_request(API_ENDPOINT, config, API_PARAMS, write = API_WRITE, **kwargs)

    if (not response.get('found', False)):
        return None

    return autograder.model.course.Course.from_api(response['course'])
