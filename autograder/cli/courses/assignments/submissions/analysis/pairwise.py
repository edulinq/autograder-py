import json
import sys

import autograder.api.courses.assignments.submissions.analysis.pairwise

HEADER = [
    'email', 'has_submission', 'short-id', 'score', 'grading_start_time', 'message',
]

def run(arguments):
    result = autograder.api.courses.assignments.submissions.analysis.pairwise.send(
        arguments, exit_on_error = True)

    print(json.dumps(result, indent = 4))
    return 0

def main():
    return run(_get_parser().parse_args())

def _get_parser():
    parser = autograder.api.courses.assignments.submissions.analysis.pairwise._get_parser()
    return parser

if (__name__ == '__main__'):
    sys.exit(main())
