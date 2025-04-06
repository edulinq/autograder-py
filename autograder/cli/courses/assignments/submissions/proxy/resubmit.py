import sys

import autograder.api.courses.assignments.submissions.proxy.resubmit
import autograder.cli.common
import autograder.cli.config

def run(arguments):
    result = autograder.api.courses.assignments.submissions.proxy.resubmit.send(arguments,
            exit_on_error = True)

    if (not result['found-user']):
        print("Proxy user not found.")
        return 3

    if (not result['found-submission']):
        print("Target submission not found.")
        return 4

    return autograder.cli.common.display_grading_result(result)

def main():
    return run(_get_parser().parse_args())

def _get_parser():
    parser = autograder.api.courses.assignments.submissions.proxy.resubmit._get_parser()

    return parser

if (__name__ == '__main__'):
    sys.exit(main())
