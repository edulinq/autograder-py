import autograder.api.common
import autograder.api.config

API_ENDPOINT = 'lms/upload/scores'
API_PARAMS = [
    autograder.api.config.PARAM_COURSE_ID,
    autograder.api.config.PARAM_USER_EMAIL,
    autograder.api.config.PARAM_USER_PASS,

    autograder.api.config.APIParam('assignment-lms-id',
        'The LMS ID of the assignment to upload scores to.',
        required = True),

    autograder.api.config.APIParam('scores',
        'A list of scores to upload.',
        required = True, cli_param = False),
]

DESCRIPTION = ("Upload scores from a tab-separated file to the course's LMS."
        + " The file should not have headers, and should have two columns: email and score.")

def send(arguments, **kwargs):
    return autograder.api.common.handle_api_request(arguments, API_PARAMS, API_ENDPOINT, **kwargs)

def _get_parser():
    parser = autograder.api.config.get_argument_parser(
        description = DESCRIPTION,
        params = API_PARAMS)

    return parser
