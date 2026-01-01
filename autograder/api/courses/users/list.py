"""
List the users in a course.
"""

import typing

import lms.model.users

import autograder.api.common
import autograder.api.config
import autograder.api.model

API_ENDPOINT: str = 'courses/users/list'
API_PARAMS: typing.List[autograder.api.config.APIParam] = [
    autograder.api.config.PARAM_SERVER,
    autograder.api.config.PARAM_COURSE,
    autograder.api.config.PARAM_USER_EMAIL,
    autograder.api.config.PARAM_USER_PASS,

    autograder.api.config.PARAM_TARGET_USERS,
]

def send(config: typing.Dict[str, typing.Any], **kwargs: typing.Any) -> typing.List[lms.model.users.ServerUser]:
    """ Send a request to the autograder. """

    response = autograder.api.common.make_api_request(API_ENDPOINT, config, API_PARAMS, **kwargs)

    users = []
    for raw_user in response['users']:
        users.append(autograder.api.model.make_course_user(raw_user))

    return sorted(users)
