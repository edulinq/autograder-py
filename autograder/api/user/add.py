import autograder.api.common
import autograder.api.config

API_ENDPOINT = 'user/add'
API_PARAMS = [
    autograder.api.config.PARAM_COURSE_ID,
    autograder.api.config.PARAM_USER_EMAIL,
    autograder.api.config.PARAM_USER_PASS,

    autograder.api.config.PARAM_FORCE,
    autograder.api.config.PARAM_DRY_RUN,
    autograder.api.config.PARAM_SKIP_EMAILS,
    autograder.api.config.PARAM_SKIP_LMS_SYNC,

    autograder.api.config.APIParam('new-users',
        'A list of users to add or modify.',
        required = True, cli_param = False),
]

DESCRIPTION = ('Add one or more users to the course.'
        + ' When force is true, this becomes an upsert (update if exists, otherwise insert).')

def send(arguments, **kwargs):
    return autograder.api.common.handle_api_request(arguments, API_PARAMS, API_ENDPOINT, **kwargs)

def _get_parser():
    parser = autograder.api.config.get_argument_parser(
        description = DESCRIPTION,
        params = API_PARAMS)

    return parser
