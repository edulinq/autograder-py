import autograder.api.common
import autograder.api.config

API_ENDPOINT = 'logs/query'
API_PARAMS = [
    autograder.api.config.PARAM_USER_EMAIL,
    autograder.api.config.PARAM_USER_PASS,

    autograder.api.config.APIParam('level',
            'The minimum level of log records to return (defaults to INFO).',
            required = False, parser_options = {'action': 'store', 'default': 'INFO'}),

    autograder.api.config.APIParam('after',
            'If supplied, only return log records after this datetime (as an RFC3339 string).',
            required = False),

    autograder.api.config.APIParam('past',
            ('If supplied, only return log records in this duration'
                + ' (using "h", "m", or "s" suffixes) (e.g., "24h", "10m", or "1h10m10s").'),
            required = False),

    autograder.api.config.APIParam('target-course',
            'If supplied, only return log records for this assignment.',
            required = False),

    autograder.api.config.APIParam('target-assignment',
            'If supplied, only return log records for this assignment.',
            required = False),

    autograder.api.config.APIParam('target-email',
            'If supplied, only return log records for this user.',
            required = False),
]

DESCRIPTION = 'Query log entries from the autograder server.'

def send(arguments, **kwargs):
    return autograder.api.common.handle_api_request(arguments, API_PARAMS, API_ENDPOINT, **kwargs)

def _get_parser():
    parser = autograder.api.config.get_argument_parser(
        description = DESCRIPTION,
        params = API_PARAMS)

    return parser
