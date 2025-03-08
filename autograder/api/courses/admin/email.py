import autograder.api.common
import autograder.api.config

API_ENDPOINT = 'courses/admin/email'
API_PARAMS = [
    autograder.api.config.PARAM_USER_EMAIL,
    autograder.api.config.PARAM_USER_PASS,

    autograder.api.config.PARAM_COURSE_ID,

    autograder.api.config.PARAM_EMAIL_TO,
    autograder.api.config.PARAM_EMAIL_CC,
    autograder.api.config.PARAM_EMAIL_BCC,
    autograder.api.config.PARAM_EMAIL_SUBJECT,
    autograder.api.config.PARAM_EMAIL_BODY,
    autograder.api.config.PARAM_EMAIL_HTML,

    autograder.api.config.PARAM_DRY_RUN,
]

DESCRIPTION = 'Send an email to course users.'

def send(arguments, **kwargs):
    return autograder.api.common.handle_api_request(arguments, API_PARAMS, API_ENDPOINT, **kwargs)

def _get_parser():
    parser = autograder.api.config.get_argument_parser(
        description = DESCRIPTION,
        params = API_PARAMS)

    return parser
