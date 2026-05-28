"""
Update an existing course using its own source.
"""

import typing

import autograder.api.common
import autograder.api.config

API_ENDPOINT: str = 'courses/admin/update'
API_WRITE: bool = True
API_PARAMS: typing.List[autograder.api.config.APIParam] = [
    autograder.api.config.PARAM_SERVER,
    autograder.api.config.PARAM_USER_EMAIL,
    autograder.api.config.PARAM_USER_PASS,

    autograder.api.config.PARAM_DRY_RUN,
    autograder.api.config.PARAM_SKIP_EMAILS,
    autograder.api.config.PARAM_SKIP_SOURCE_SYNC,
    autograder.api.config.PARAM_SKIP_LMS_SYNC,
    autograder.api.config.PARAM_SKIP_BUILD_IMAGES,
    autograder.api.config.PARAM_SKIP_TEMPLATE_FILES,

    autograder.api.config.PARAM_COURSE,
]

def send(config: typing.Dict[str, typing.Any], **kwargs: typing.Any) -> typing.Dict[str, typing.Any]:
    """ Send a request to the autograder. """

    return autograder.api.common.make_api_request(API_ENDPOINT, config, API_PARAMS, write = API_WRITE, **kwargs)
