import json
import sys

import autograder.api.stats.apirequest.query

def run(arguments):
    result = autograder.api.stats.apirequest.query.send(arguments, exit_on_error = True)
    print(json.dumps(result['results'], indent = 4))
    return 0

def main():
    return run(_get_parser().parse_args())

def _get_parser():
    parser = autograder.api.stats.apirequest.query._get_parser()

    return parser

if (__name__ == '__main__'):
    sys.exit(main())
