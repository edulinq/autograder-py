import autograder.api.common
import autograder.api.config

API_ENDPOINT = 'courses/assignments/submissions/proxy/submit'
API_PARAMS = [
    autograder.api.config.PARAM_COURSE_ID,
    autograder.api.config.PARAM_USER_EMAIL,
    autograder.api.config.PARAM_USER_PASS,
    autograder.api.config.PARAM_ASSIGNMENT_ID,
    autograder.api.config.PARAM_SUBMISSION_MESSAGE,

    autograder.api.config.PARAM_PROXY_EMAIL,
    autograder.api.config.PARAM_PROXY_TIME,
]

DESCRIPTION = 'Proxy submit an assignment submission to the autograder.'

def send(arguments, **kwargs):
    return autograder.api.common.handle_api_request(arguments, API_PARAMS, API_ENDPOINT, **kwargs)

def _get_parser():
    parser = autograder.api.config.get_argument_parser(
        description = DESCRIPTION,
        params = API_PARAMS)

    return parser
