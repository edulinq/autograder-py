"""
Handle timestamp operations.
All datetimes/timestamps passed by the autograder are ints (milliseconds since UNIX epoch (UTC)).
We will handle timestamps the same way (with the exception of pretty strings).
"""

import datetime
import re
import time

PRETTY_TIMESTAMP_FORMAT = '%Y-%m-%d %H:%M'
UNKNOWN_TIMESTAMP = "<Unknown Time (%s)>"
MISSING_TIMESTAMP = "<Missing Time>"

def get(source = None, pretty = False, adjust_tz = True):
    if (source == MISSING_TIMESTAMP):
        return source

    if (isinstance(source, str) and ('Unknown Time' in source)):
        return source

    timestamp, clean_source = _parse_timestamp(source)
    if (timestamp is None):
        return UNKNOWN_TIMESTAMP % (clean_source)

    if (pretty):
        return _to_string(timestamp, adjust_tz = adjust_tz)

    return timestamp

def _parse_timestamp(source = None):
    if (source is None):
        return _now(), None

    if (isinstance(source, datetime.datetime)):
        return _timestamp_from_pytime(source)

    if (source == ''):
        return None, ''

    if (isinstance(source, (int, float))):
        # Unix timestamp.
        return int(source), None

    if (not isinstance(source, str)):
        raise ValueError("Unknown type ('%s') for timestamp source." % (type(source)))

    source = source.strip()

    # Parse out some cases that Python <= 3.10 cannot deal with.
    # This will remove fractional seconds.
    source = re.sub(r'Z$', '+00:00', source)

    try:
        value = datetime.datetime.fromisoformat(source)
        return _timestamp_from_pytime(value), None
    except Exception:
        pass

    return None, source

def _timestamp_from_pytime(pytime):
    return int(pytime.timestamp() * 1000)

def _pytime_from_timestamp(timestamp):
    return datetime.datetime.utcfromtimestamp(timestamp / 1000)

def _now():
    return int(time.time() * 1000)

def _to_string(timestamp, adjust_tz = True):
    pytime = _pytime_from_timestamp(timestamp)
    if (adjust_tz):
        pytime = pytime.astimezone()

    return pytime.strftime(PRETTY_TIMESTAMP_FORMAT)
