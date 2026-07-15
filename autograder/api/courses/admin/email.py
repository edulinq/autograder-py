"""
Send an email to course users.
"""

import typing

import autograder.api.common
import autograder.api.config
import autograder.model.config

API_ENDPOINT: str = 'courses/admin/email'
API_WRITE: bool = True
API_PARAMS: typing.List[autograder.api.config.APIParam] = [
    autograder.api.config.PARAM_SERVER,
    autograder.api.config.PARAM_USER_EMAIL,
    autograder.api.config.PARAM_USER_PASS,

    autograder.api.config.PARAM_COURSE,
    autograder.api.config.PARAM_DRY_RUN,

    autograder.api.config.PARAM_EMAIL_COURSE_TO,
    autograder.api.config.PARAM_EMAIL_COURSE_CC,
    autograder.api.config.PARAM_EMAIL_COURSE_BCC,
    autograder.api.config.PARAM_EMAIL_SUBJECT,
    autograder.api.config.PARAM_EMAIL_BODY,
    autograder.api.config.PARAM_EMAIL_HTML,
]

def send(config: autograder.model.config.Config, **kwargs: typing.Any) -> typing.Dict[str, typing.Any]:
    """ Send a request to the autograder. """

    return autograder.api.common.make_api_request(API_ENDPOINT, config, API_PARAMS, write = API_WRITE, **kwargs)
