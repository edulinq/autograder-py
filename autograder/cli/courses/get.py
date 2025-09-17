import json
import sys

import autograder.api.courses.get

def run(arguments):
    result = autograder.api.courses.get.send(arguments, exit_on_error = True)
    print(json.dumps(result, indent = 4))
    return 0

def main():
    return run(_get_parser().parse_args())

def _get_parser():
    return autograder.api.courses.get._get_parser()

if (__name__ == '__main__'):
    sys.exit(main())
