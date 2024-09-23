import json
import sys

import autograder.api.admin.fetchlogs
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
    result = autograder.api.admin.fetchlogs.send(arguments, exit_on_error = True)

    if (not result['success']):
        print("Error fetching logs:")
        for message in result['error-messages']:
            print("    " + message)

        return 1

    if (arguments.json):
        print(json.dumps(result['results'], indent = 4))
    else:
        for record in result['results']:
            print(_log_record_str(record))

    return 0

def _log_record_str(record):
    level = "Unknown (%d)" % (record['level'])
    if (record['level'] in LEVEL_TO_STRING):
        level = LEVEL_TO_STRING[record['level']]

    timestamp = autograder.util.timestamp.get(record['timestamp'], pretty = True)

    message = record['message']

    attributes = record.get('attributes', {})

    for key in ['course', 'assignment', 'user']:
        if (key in record):
            attributes[key] = record[key]

    if (len(attributes) > 0):
        message += (" | " + json.dumps(attributes))

    return "%s [%5s] %s" % (timestamp, level, message)

def main():
    return run(_get_parser().parse_args())

def _get_parser():
    parser = autograder.api.admin.fetchlogs._get_parser()

    parser.add_argument('--json', dest = 'json',
        action = 'store_true', default = False,
        help = ('Output the results as a JSON array instead of a more human-readable format'
            + ' (default: %(default)s).'))

    return parser

if (__name__ == '__main__'):
    sys.exit(main())
