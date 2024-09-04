import autograder.api.common
import autograder.api.config

API_ENDPOINT = 'users/password/reset'
API_PARAMS = [
    autograder.api.config.PARAM_USER_EMAIL,
]

DESCRIPTION = 'Reset to a random password that will be emailed to you.'

def send(arguments, **kwargs):
    return autograder.api.common.handle_api_request(arguments, API_PARAMS, API_ENDPOINT, **kwargs)

def _get_parser():
    parser = autograder.api.config.get_argument_parser(
        description = DESCRIPTION,
        params = API_PARAMS)

    return parser
