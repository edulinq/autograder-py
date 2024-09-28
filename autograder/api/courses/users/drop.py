import autograder.api.common
import autograder.api.config

API_ENDPOINT = 'courses/users/drop'

API_PARAMS = [
    autograder.api.config.PARAM_USER_EMAIL,
    autograder.api.config.PARAM_USER_PASS,

    autograder.api.config.PARAM_COURSE_ID,

    autograder.api.config.PARAM_TARGET_EMAIL,
]

DESCRIPTION = 'Drop a user from the course.'

def send(arguments, **kwargs):
    return autograder.api.common.handle_api_request(arguments, API_PARAMS, API_ENDPOINT, **kwargs)

def _get_parser():
    parser = autograder.api.config.get_argument_parser(
        description = DESCRIPTION,
        params = API_PARAMS)

    return parser
