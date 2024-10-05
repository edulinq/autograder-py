import json
import sys

import autograder.api.logs.query
import autograder.util.timestamp

LEVEL_TO_STRING = {
    -20: 'TRACE',
    -10: 'DEBUG',
    0: 'INFO',
    10: 'WARN',
    20: 'ERROR',
    30: 'FATAL',
    100: 'OFF',
}

def run(arguments):
    result = autograder.api.logs.query.send(arguments, exit_on_error = True)

    if (not result['success']):
        print("Error fetching logs:")
        print(json.dumps(result['error'], indent = 4))

        return 1

    if (arguments.json):
        print(_log_records_json(result['results']))
    else:
        for record in result['results']:
            print(_log_record_str(record))

    return 0

def _log_records_json(records):
    records = records.copy()

    for record in records:
        raw_level = record['level']
        record['level'] = _get_level_str(raw_level)
        record['_raw_level_'] = raw_level

        raw_timestamp = record['timestamp']
        record['timestamp'] = autograder.util.timestamp.get(record['timestamp'], pretty = True)
        record['_raw_timestamp_'] = raw_timestamp

    return json.dumps(records, indent = 4)

def _get_level_str(raw_level):
    level = "Unknown (%d)" % (raw_level)
    if (raw_level in LEVEL_TO_STRING):
        level = LEVEL_TO_STRING[raw_level]

    return level

def _log_record_str(record):
    level = _get_level_str(record['level'])
    timestamp = autograder.util.timestamp.get(record['timestamp'], pretty = True)
    message = record['message']
    attributes = record.get('attributes', {})

    for key in ['course', 'assignment', 'user']:
        if (key in record):
            attributes[key] = record[key]

    error = record.get('error', None)
    if (error is not None):
        attributes['_error_'] = error

    if (len(attributes) > 0):
        message += (" | " + json.dumps(attributes))

    return "%s [%5s] %s" % (timestamp, level, message)

def main():
    return run(_get_parser().parse_args())

def _get_parser():
    parser = autograder.api.logs.query._get_parser()

    parser.add_argument('--json', dest = 'json',
        action = 'store_true', default = False,
        help = ('Output the results as a JSON array instead of a more human-readable format'
            + ' (default: %(default)s).'))

    return parser

if (__name__ == '__main__'):
    sys.exit(main())
