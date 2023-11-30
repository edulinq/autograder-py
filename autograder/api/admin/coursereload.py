import autograder.api.common
import autograder.api.config

API_ENDPOINT = 'admin/course/reload'
API_PARAMS = [
    autograder.api.config.PARAM_COURSE_ID,
    autograder.api.config.PARAM_USER_EMAIL,
    autograder.api.config.PARAM_USER_PASS,

    autograder.api.config.APIParam('clear',
            'Clear the course database before reloading.',
            required = False,
            parser_options = {'action': 'store_true', 'default': False})
]

DESCRIPTION = 'Reload a course from its config.'

def send(arguments, **kwargs):
    return autograder.api.common.handle_api_request(arguments, API_PARAMS, API_ENDPOINT, **kwargs)

def _get_parser():
    parser = autograder.api.config.get_argument_parser(
        description = DESCRIPTION,
        params = API_PARAMS)

    return parser
