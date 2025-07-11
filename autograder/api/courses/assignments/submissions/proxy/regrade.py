import autograder.api.common
import autograder.api.config

API_ENDPOINT = 'courses/assignments/submissions/proxy/regrade'
API_PARAMS = [
    autograder.api.config.PARAM_COURSE_ID,
    autograder.api.config.PARAM_USER_EMAIL,
    autograder.api.config.PARAM_USER_PASS,
    autograder.api.config.PARAM_ASSIGNMENT_ID,

    autograder.api.config.PARAM_COURSE_USER_REFERENCES,
    autograder.api.config.PARAM_REGRADE_CUTOFF,

    autograder.api.config.PARAM_DRY_RUN,
    autograder.api.config.PARAM_OVERWRITE_RECORDS,
    autograder.api.config.PARAM_WAIT_FOR_COMPLETION,
]

DESCRIPTION = 'Proxy regrade an assignment for all target users using their most recent submission.'

def send(arguments, **kwargs):
    return autograder.api.common.handle_api_request(arguments, API_PARAMS, API_ENDPOINT, **kwargs)

def _get_parser():
    parser = autograder.api.config.get_argument_parser(
        description = DESCRIPTION,
        params = API_PARAMS)

    return parser
