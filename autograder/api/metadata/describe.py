import autograder.api.common
import autograder.api.config

API_ENDPOINT = 'metadata/describe'
API_PARAMS = []

DESCRIPTION = 'Describe all endpoints on the server.'

def send(arguments, **kwargs):
    return autograder.api.common.handle_api_request(arguments, API_PARAMS, API_ENDPOINT, **kwargs)

def _get_parser():
    parser = autograder.api.config.get_argument_parser(
        description = DESCRIPTION,
        params = API_PARAMS)

    return parser
