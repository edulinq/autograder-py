import typing

import edq.util.time
import lms.model.base

METRIC_TYPES: typing.List[str] = [
    'api-request',
    'code-analysis-time',
    'grading-time',
    'cpu-usage',
    'mem-usage',
    'net-in',
    'net-out',
    'task-time',
]

class Metric(lms.model.base.BaseType):
    """
    A metric value.
    """

    CORE_FIELDS = [
        'timestamp',
        'type',
        'value',
    ]

    def __init__(self,
            type: str,
            timestamp: edq.util.time.Timestamp,
            value: float,
            attributes: typing.Union[typing.Dict[str, typing.Any], None] = None,
            **kwargs: typing.Any) -> None:
        super().__init__(**kwargs)

        self.type: str = type
        """ The type of metric. """

        self.timestamp: edq.util.time.Timestamp = timestamp
        """ Metric collection time. """

        self.value: float = value
        """ The metric's value. """

        if (attributes is None):
            attributes = {}

        self.attributes: typing.Dict[str, typing.Any] = attributes
        """ Additional attributes attatched to the metric record. """

    @classmethod
    def from_api(cls, data: typing.Dict[str, typing.Any]) -> 'Metric':
        """ Convert a dict coming from autograder API JSON. """

        data = data.copy()

        data['timestamp'] = edq.util.time.Timestamp(data['timestamp'])

        return Metric(**data)
