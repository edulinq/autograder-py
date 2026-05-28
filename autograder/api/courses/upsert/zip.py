"""
Upsert a course using a zip file.
"""

import typing

import autograder.api.common
import autograder.api.config
import autograder.error

API_ENDPOINT: str = 'courses/upsert/zip'
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

    autograder.api.config.PARAM_UPSERT_ZIP,
]

def send(
        config: typing.Dict[str, typing.Any],
        post_paths: typing.Union[typing.List[str], None] = None,
        **kwargs: typing.Any,
        ) -> typing.Dict[str, typing.Any]:
    """ Send a request to the autograder. """

    if ((post_paths is None) or len(post_paths) == 0):
        raise autograder.error.AutograderError("No files provided for upsert.")

    if (len(post_paths) > 1):
        raise autograder.error.AutograderError(f"Too many files ({len(post_paths)}) provided for upsert, expecting exactly one.")

    return autograder.api.common.make_api_request(API_ENDPOINT, config, API_PARAMS, write = API_WRITE, post_paths = post_paths, **kwargs)
