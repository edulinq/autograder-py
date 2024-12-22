import autograder.api.common
import autograder.api.config

API_ENDPOINT = 'courses/assignments/submissions/submit'
API_PARAMS = [
    autograder.api.config.PARAM_COURSE_ID,
    autograder.api.config.PARAM_USER_EMAIL,
    autograder.api.config.PARAM_USER_PASS,
    autograder.api.config.PARAM_ASSIGNMENT_ID,

    autograder.api.config.APIParam('message',
        'An optional message to attatch to the submission.',
        required = False),

    autograder.api.config.APIParam('allow-late',
        'Allow this submission to be graded, even if it is late (default: %(default)s).',
        required = False,
        parser_options = {'action': 'store_true', 'default': False})
]

DESCRIPTION = 'Submit an assignment submission to the autograder.'

def send(arguments, **kwargs):
    return autograder.api.common.handle_api_request(arguments, API_PARAMS, API_ENDPOINT, **kwargs)

def _get_parser():
    parser = autograder.api.config.get_argument_parser(
        description = DESCRIPTION,
        params = API_PARAMS)

    return parser
