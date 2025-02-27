import autograder.api.common
import autograder.api.config

API_ENDPOINT = 'stats/apirequest/query'
API_PARAMS = [
    autograder.api.config.PARAM_USER_EMAIL,
    autograder.api.config.PARAM_USER_PASS,

    autograder.api.config.PARAM_QUERY_LIMIT,
    autograder.api.config.PARAM_QUERY_AFTER,
    autograder.api.config.PARAM_QUERY_BEFORE,
    autograder.api.config.PARAM_QUERY_SORT,

    autograder.api.config.PARAM_QUERY_TARGET_SENDER,
    autograder.api.config.PARAM_QUERY_TARGET_ENDPOINT,
    autograder.api.config.PARAM_QUERY_TARGET_EMAIL,
    autograder.api.config.PARAM_QUERY_TARGET_COURSE,
    autograder.api.config.PARAM_QUERY_TARGET_ASSIGNMENT,
    autograder.api.config.PARAM_QUERY_TARGET_LOCATOR,
]

DESCRIPTION = 'Query stats for API requests.'

def send(arguments, **kwargs):
    return autograder.api.common.handle_api_request(arguments, API_PARAMS, API_ENDPOINT, **kwargs)

def _get_parser():
    parser = autograder.api.config.get_argument_parser(
        description = DESCRIPTION,
        params = API_PARAMS)

    return parser
