"""
Query log entries from the autograder server.
"""

import typing

import autograder.api.common
import autograder.api.config
import autograder.error
import autograder.model.log

API_ENDPOINT: str = 'logs/query'
API_WRITE: bool = False
API_PARAMS: typing.List[autograder.api.config.APIParam] = [
    autograder.api.config.PARAM_SERVER,
    autograder.api.config.PARAM_USER_EMAIL,
    autograder.api.config.PARAM_USER_PASS,

    autograder.api.config.PARAM_QUERY_USE_TESTING_DATA,

    autograder.api.config.PARAM_QUERY_LOG_LEVEL,
    autograder.api.config.PARAM_QUERY_AFTER,
    autograder.api.config.PARAM_QUERY_PAST,

    autograder.api.config.PARAM_QUERY_TARGET_COURSE,
    autograder.api.config.PARAM_QUERY_TARGET_ASSIGNMENT,
    autograder.api.config.PARAM_QUERY_TARGET_EMAIL,
]

def send(
        config: typing.Dict[str, typing.Any],
        **kwargs: typing.Any,
        ) -> typing.Tuple[typing.Union[str, None], typing.List[autograder.model.log.LogRecord]]:
    """
    Send a request to the autograder.
    Returns: (error, log records).
    """

    result = autograder.api.common.make_api_request(API_ENDPOINT, config, API_PARAMS, write = API_WRITE, **kwargs)

    error = result.get('error', None)
    if (error is not None):
        return f"Error: '{error['message']}', Locator: '{error['locator']}'.", []

    records = [autograder.model.log.LogRecord.from_api(data) for data in result['results']]

    return None, records
