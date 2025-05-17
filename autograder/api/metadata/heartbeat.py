import autograder.api.common
import autograder.api.config

API_ENDPOINT = 'metadata/heartbeat'
API_PARAMS = []

DESCRIPTION = 'Get server heartbeat.'

def send(arguments, **kwargs):
    return autograder.api.common.handle_api_request(arguments, API_PARAMS, API_ENDPOINT, **kwargs)

def _get_parser():
    parser = autograder.api.config.get_argument_parser(
        description = DESCRIPTION,
        params = API_PARAMS)

    return parser
