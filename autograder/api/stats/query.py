import autograder.api.common
import autograder.api.config

API_ENDPOINT = 'stats/query'
API_PARAMS = [
    autograder.api.config.PARAM_USER_EMAIL,
    autograder.api.config.PARAM_USER_PASS,

    autograder.api.config.PARAM_QUERY_TYPE,

    autograder.api.config.PARAM_QUERY_LIMIT,
    autograder.api.config.PARAM_QUERY_AFTER,
    autograder.api.config.PARAM_QUERY_BEFORE,
    autograder.api.config.PARAM_QUERY_SORT,
    autograder.api.config.PARAM_QUERY_WHERE,
]

DESCRIPTION = 'Query stats from the sever.'

def send(arguments, **kwargs):
    return autograder.api.common.handle_api_request(arguments, API_PARAMS, API_ENDPOINT, **kwargs)

def _get_parser():
    parser = autograder.api.config.get_argument_parser(
        description = DESCRIPTION,
        params = API_PARAMS)

    return parser
