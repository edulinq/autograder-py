"""
Enroll one or more users in a course.
"""

import typing

import autograder.api.common
import autograder.api.config
import autograder.model.config

API_ENDPOINT: str = 'courses/users/enroll'
API_WRITE: bool = True
API_PARAMS: typing.List[autograder.api.config.APIParam] = [
    autograder.api.config.PARAM_SERVER,
    autograder.api.config.PARAM_COURSE,
    autograder.api.config.PARAM_USER_EMAIL,
    autograder.api.config.PARAM_USER_PASS,

    autograder.api.config.PARAM_DRY_RUN,
    autograder.api.config.PARAM_SKIP_INSERTS,
    autograder.api.config.PARAM_SKIP_UPDATES,

    autograder.api.config.PARAM_SEND_EMAILS,

    autograder.api.config.PARAM_RAW_COURSE_USERS,

    autograder.api.config.PARAM_NEW_USER_EMAIL,
    autograder.api.config.PARAM_NEW_USER_NAME,
    autograder.api.config.PARAM_NEW_USER_COURSE_ROLE,
    autograder.api.config.PARAM_NEW_USER_LMS_ID,
]

def send(config: autograder.model.config.Config, **kwargs: typing.Any) -> typing.Dict[str, typing.Any]:
    """ Send a request to the autograder. """

    return autograder.api.common.make_api_request(API_ENDPOINT, config, API_PARAMS, write = API_WRITE, **kwargs)
