import autograder.api.common
import autograder.api.config

API_ENDPOINT = 'stats/system/query'
API_PARAMS = [
    autograder.api.config.PARAM_USER_EMAIL,
    autograder.api.config.PARAM_USER_PASS,

    autograder.api.config.APIParam('limit',
            'The maximum number of records to return.',
            required = False, parser_options = {'action': 'store', 'type': int}),

    autograder.api.config.APIParam('after',
            'If supplied, only return stat records after this timestamp.',
            required = False),

    autograder.api.config.APIParam('before',
            'If supplied, only return stat records before this timestamp.',
            required = False),

    autograder.api.config.APIParam('sort',
            'Sort the results. -1 for ascending, 0 for no sorting, 1 for descending.',
            required = False, parser_options = {'action': 'store', 'type': int}),
]

DESCRIPTION = 'Query system stats from the autograder server.'

def send(arguments, **kwargs):
    return autograder.api.common.handle_api_request(arguments, API_PARAMS, API_ENDPOINT, **kwargs)

def _get_parser():
    parser = autograder.api.config.get_argument_parser(
        description = DESCRIPTION,
        params = API_PARAMS)

    return parser
