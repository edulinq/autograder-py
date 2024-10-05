import json
import sys

import autograder.api.courses.admin.update

def run(arguments):
    result = autograder.api.courses.admin.update.send(arguments, exit_on_error = True)
    result = result['result']

    exit_status = 0
    if (not result['success']):
        exit_status = 1

    if (arguments.full_output):
        print(json.dumps(result, indent = 4))
        return exit_status

    if (result['success']):
        print("Course updated.")
    else:
        print("Course not updated.")
        print("Message from server: '%s'." % (result.get('message', '')))

    return exit_status

def main():
    return run(_get_parser().parse_args())

def _get_parser():
    parser = autograder.api.courses.admin.update._get_parser()

    parser.add_argument('--full-output', dest = 'full_output',
        action = 'store_true', default = False,
        help = 'See the full course update output (as JSON) (default: %(default)s).')

    return parser

if (__name__ == '__main__'):
    sys.exit(main())
