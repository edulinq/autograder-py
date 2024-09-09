import autograder.api.common
import autograder.api.config

API_ENDPOINT = 'courses/admin/update'
API_PARAMS = [
    autograder.api.config.PARAM_COURSE_ID,
    autograder.api.config.PARAM_USER_EMAIL,
    autograder.api.config.PARAM_USER_PASS,

    autograder.api.config.PARAM_COURSE_SOURCE,
    autograder.api.config.APIParam('clear',
            'Clear the course database before updating.',
            required = False,
            parser_options = {'action': 'store_true', 'default': False})
]

DESCRIPTION = 'Update a course from its source.'

def send(arguments, **kwargs):
    return autograder.api.common.handle_api_request(arguments, API_PARAMS, API_ENDPOINT, **kwargs)

def _get_parser():
    parser = autograder.api.config.get_argument_parser(
        description = DESCRIPTION,
        params = API_PARAMS)

    return parser
