import typing

import edq.util.time
import lms.model.base

LOG_LEVEL_TEXT_TO_INT: typing.Dict[str, int] = {
    'TRACE': -20,
    'DEBUG': -10,
    'INFO': 0,
    'WARN': 10,
    'ERROR': 20,
    'FATAL': 30,
    'OFF': 100,
}
""" Map text API log levels to int values. """

LOG_LEVEL_INT_TO_TEXT: typing.Dict[int, str] = {value: key for (key, value) in LOG_LEVEL_TEXT_TO_INT.items()}
""" Map int API log levels to text. """

class LogRecord(lms.model.base.BaseType):  # type: ignore[misc]
    """
    A logging record.
    """

    CORE_FIELDS = [
        'timestamp',
        'level',
        'message',
        'error',
        'course',
        'assignment',
        'user',
    ]

    def __init__(self,
            level: str,
            timestamp: edq.util.time.Timestamp,
            message: typing.Union[str, None] = None,
            error: typing.Union[str, None] = None,
            course: typing.Union[str, None] = None,
            assignment: typing.Union[str, None] = None,
            user: typing.Union[str, None] = None,
            attributes: typing.Union[typing.Dict[str, typing.Any], None] = None,
            **kwargs: typing.Any) -> None:
        super().__init__(**kwargs)

        self.level: str = level
        """ Logging level. """

        self.timestamp: edq.util.time.Timestamp = timestamp
        """ Log time. """

        self.message: typing.Union[str, None] = message
        """ Log message. """

        self.error: typing.Union[str, None] = error
        """ Log error. """

        self.course: typing.Union[str, None] = course
        """ Log course. """

        self.assignment: typing.Union[str, None] = assignment
        """ Log assignment. """

        self.user: typing.Union[str, None] = user
        """ Log user. """

        if (attributes is None):
            attributes = {}

        self.attributes: typing.Dict[str, typing.Any] = attributes
        """ Additional attributes attatched to the logging record. """

    @classmethod
    def from_api(cls, data: typing.Dict[str, typing.Any]) -> 'LogRecord':
        """ Convert a dict coming from autograder API JSON. """

        data = data.copy()

        data['level'] = LOG_LEVEL_INT_TO_TEXT[data['level']]
        data['timestamp'] = edq.util.time.Timestamp(data['timestamp'])

        return LogRecord(**data)
