import autograder.api.common
import autograder.api.config

API_ENDPOINT = 'submission/remove/submission'
API_PARAMS = [
    autograder.api.config.PARAM_COURSE_ID,
    autograder.api.config.PARAM_USER_EMAIL,
    autograder.api.config.PARAM_USER_PASS,
    autograder.api.config.PARAM_ASSIGNMENT_ID,

    autograder.api.config.PARAM_TARGET_EMAIL,
    autograder.api.config.PARAM_TARGET_SUBMISSION,
]

DESCRIPTION = ('Remove a specified submission.')

def send(arguments, **kwargs):
    
    confirm = input(f'Are you sure you want to remove submission "{getattr(arguments, 'target-submission', None)}" from {getattr(arguments, 'target-email', None)}? (y/n): ' )
    if confirm.lower() == "y" or confirm.lower() == "yes":
        return autograder.api.common.handle_api_request(arguments, API_PARAMS, API_ENDPOINT, **kwargs)
    elif confirm.lower() == "n" or confirm.lower() == "no":
        return 1
    else:
        return 0

def _get_parser():
    parser = autograder.api.config.get_argument_parser(
        description = DESCRIPTION,
        params = API_PARAMS)

    return parser
