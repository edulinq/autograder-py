import autograder.api.common
import autograder.api.config

API_ENDPOINT = 'courses/assignments/submissions/analysis/individual'
API_PARAMS = [
    autograder.api.config.PARAM_USER_EMAIL,
    autograder.api.config.PARAM_USER_PASS,

    autograder.api.config.PARAM_SUBMISSION_SPECS,
    autograder.api.config.PARAM_WAIT_FOR_COMPLETION,
]

DESCRIPTION = 'Get the result of a individual analysis for the specified submissions'

def send(arguments, **kwargs):
    return autograder.api.common.handle_api_request(arguments, API_PARAMS, API_ENDPOINT, **kwargs)

def _get_parser():
    parser = autograder.api.config.get_argument_parser(
        description = DESCRIPTION,
        params = API_PARAMS)

    return parser
