import autograder.api.common
import autograder.api.config

API_ENDPOINT = 'users/upsert'
API_PARAMS = [
    autograder.api.config.PARAM_USER_EMAIL,
    autograder.api.config.PARAM_USER_PASS,

    autograder.api.config.PARAM_DRY_RUN,
    autograder.api.config.PARAM_SKIP_INSERTS,
    autograder.api.config.PARAM_SKIP_UPDATES,

    autograder.api.config.PARAM_SEND_EMAILS,

    autograder.api.config.APIParam('raw-users',
        'A list of users to upsert.',
        required = True, cli_param = False),
]

DESCRIPTION = 'Upsert one or more users to the server (update if exists, insert otherwise).'

def send(arguments, **kwargs):
    return autograder.api.common.handle_api_request(arguments, API_PARAMS, API_ENDPOINT, **kwargs)

def _get_parser():
    parser = autograder.api.config.get_argument_parser(
        description = DESCRIPTION,
        params = API_PARAMS)

    return parser
