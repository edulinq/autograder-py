"""
List the users in a course.
"""

import typing

import lms.model.users

import autograder.api.common
import autograder.api.config
import autograder.model.user
import autograder.model.config

API_ENDPOINT: str = 'courses/users/list'
API_WRITE: bool = False
API_PARAMS: typing.List[autograder.api.config.APIParam] = [
    autograder.api.config.PARAM_SERVER,
    autograder.api.config.PARAM_COURSE,
    autograder.api.config.PARAM_USER_EMAIL,
    autograder.api.config.PARAM_USER_PASS,

    autograder.api.config.PARAM_TARGET_USERS,
]

def send(config: autograder.model.config.Config, **kwargs: typing.Any) -> typing.List[lms.model.users.ServerUser]:
    """ Send a request to the autograder. """

    response = autograder.api.common.make_api_request(API_ENDPOINT, config, API_PARAMS, write = API_WRITE, **kwargs)

    users = []
    for raw_user in response['users']:
        users.append(autograder.model.user.make_course_user(raw_user))

    return sorted(users)
