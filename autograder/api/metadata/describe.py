import autograder.api.common
import autograder.api.config

API_ENDPOINT = 'metadata/describe'
API_PARAMS = [
    autograder.api.config.APIParam('force-compute',
        'Force compute metadata descriptions, ignoring any existing cache.',
        required = False,
        parser_options = {'action': 'store_true', 'default': False})
]

DESCRIPTION = 'Describe all endpoints on the server.'

def send(arguments, **kwargs):
    return autograder.api.common.handle_api_request(arguments, API_PARAMS, API_ENDPOINT, **kwargs)

def _get_parser():
    parser = autograder.api.config.get_argument_parser(
        description = DESCRIPTION,
        params = API_PARAMS)

    return parser
