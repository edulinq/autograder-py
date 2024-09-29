import autograder.api.common
import autograder.api.config

API_ENDPOINT = 'courses/users/enroll'
API_PARAMS = [
    autograder.api.config.PARAM_USER_EMAIL,
    autograder.api.config.PARAM_USER_PASS,
    autograder.api.config.PARAM_COURSE_ID,

    autograder.api.config.PARAM_DRY_RUN,
    autograder.api.config.PARAM_SKIP_INSERTS,
    autograder.api.config.PARAM_SKIP_UPDATES,

    autograder.api.config.PARAM_SEND_EMAILS,

    autograder.api.config.APIParam('raw-course-users',
        'A list of users to enroll.',
        required = True, cli_param = False),
]

DESCRIPTION = 'Enroll one or more users to the course.'

def send(arguments, **kwargs):
    return autograder.api.common.handle_api_request(arguments, API_PARAMS, API_ENDPOINT, **kwargs)

def _get_parser():
    parser = autograder.api.config.get_argument_parser(
        description = DESCRIPTION,
        params = API_PARAMS)

    return parser
