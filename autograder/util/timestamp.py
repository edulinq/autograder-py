"""
Handle timestamp operations.
All datetimes that may be serialized should be produced by this module and handled as strings.
Likewise, all datetimes that come from the autograder should go through here.
"""

import datetime
import re

PRETTY_TIMESTAMP_FORMAT = '%Y-%m-%d %H:%M'
UNKNOWN_TIMESTAMP = "<Unknown Time (%s)>"
MISSING_TIMESTAMP = "<Missing Time>"

def get(source = None, pretty = False, adjust_tz = True):
    if (source == MISSING_TIMESTAMP):
        return source

    if (isinstance(source, str) and ('Unknown Time' in source)):
        return source

    instance, clean_source = _get_as_datetime(source)
    if (instance is None):
        return UNKNOWN_TIMESTAMP % (clean_source)

    return _to_string(instance, pretty = pretty, adjust_tz = adjust_tz)

def _get_as_datetime(source = None):
    if (source is None):
        return datetime.datetime.now(datetime.timezone.utc), None

    if (isinstance(source, datetime.datetime)):
        return source, None

    if (source == ''):
        return None, ''

    if (isinstance(source, (int, float))):
        # Unix timestamp.
        return datetime.datetime.fromtimestamp(source), None

    if (not isinstance(source, str)):
        raise ValueError("Unknown type ('%s') for timestamp source." % (type(source)))

    # Parse out some cases that Python <= 3.10 cannot deal with.
    # This will remove fractional seconds.
    source = re.sub(r'Z$', '+00:00', source)
    source = re.sub(r'(\d\d:\d\d)(\.\d+)', r'\1', source)

    try:
        return datetime.datetime.fromisoformat(source), None
    except Exception:
        pass

    return None, source

def _to_string(instance, pretty = False, adjust_tz = True):
    if (pretty):
        if (adjust_tz):
            return instance.astimezone().strftime(PRETTY_TIMESTAMP_FORMAT)
        else:
            return instance.strftime(PRETTY_TIMESTAMP_FORMAT)

    return instance.isoformat()
