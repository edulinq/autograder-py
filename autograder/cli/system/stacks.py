import json
import sys

import autograder.api.system.stacks

def run(arguments):
    result = autograder.api.system.stacks.send(arguments, exit_on_error = True)
    print(json.dumps(result, indent = 4))
    return 0

def main():
    return run(_get_parser().parse_args())

def _get_parser():
    parser = autograder.api.system.stacks._get_parser()

    return parser

if (__name__ == '__main__'):
    sys.exit(main())
