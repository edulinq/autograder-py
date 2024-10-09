import autograder.api.common
import autograder.api.config

API_ENDPOINT = 'courses/upsert/filespec'
API_PARAMS = [
    autograder.api.config.PARAM_COURSE_ID,
    autograder.api.config.PARAM_USER_EMAIL,
    autograder.api.config.PARAM_USER_PASS,

    autograder.api.config.PARAM_SKIP_SOURCE_SYNC,
    autograder.api.config.PARAM_SKIP_LMS_SYNC,
    autograder.api.config.PARAM_SKIP_BUILD_IMAGES,
    autograder.api.config.PARAM_SKIP_TASKS,

    autograder.api.config.PARAM_DRY_RUN,
    autograder.api.config.PARAM_SKIP_EMAILS,

    autograder.api.config.APIParam('filespec',
        'The specification of the file to upload.',
        required = True, cli_param = False),
]

DESCRIPTION = 'Upsert a course using a filespec.'

def send(arguments, **kwargs):
    return autograder.api.common.handle_api_request(arguments, API_PARAMS, API_ENDPOINT, **kwargs)

def _get_parser():
    parser = autograder.api.config.get_argument_parser(
        description = DESCRIPTION,
        params = API_PARAMS)

    return parser
