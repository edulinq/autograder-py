"""
Upsert a course using a file specification (FileSpec).
"""

import typing

import autograder.api.common
import autograder.api.config
import autograder.error

API_ENDPOINT: str = 'courses/upsert/filespec'
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

    autograder.api.config.PARAM_UPSERT_FILESPEC,

    autograder.api.config.PARAM_FILESPEC_PART_TYPE,
    autograder.api.config.PARAM_FILESPEC_PART_PATH,
    autograder.api.config.PARAM_FILESPEC_PART_REFERENCE,
    autograder.api.config.PARAM_FILESPEC_PART_USERNAME,
    autograder.api.config.PARAM_FILESPEC_PART_TOKEN,
]

def send(config: typing.Dict[str, typing.Any], **kwargs: typing.Any) -> typing.Dict[str, typing.Any]:
    """ Send a request to the autograder. """

    return autograder.api.common.make_api_request(API_ENDPOINT, config, API_PARAMS, write = API_WRITE, **kwargs)
