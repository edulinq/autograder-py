import sys

import autograder.api.courses.assignments.submissions.fetch.user.peek
import autograder.assignment

def run(arguments):
    result = autograder.api.courses.assignments.submissions.fetch.user.peek.send(arguments,
            exit_on_error = True)

    if (not result['found-user']):
        print("No matching user found.")
        return 1

    if (not result['found-submission']):
        print("No matching submission found.")
        return 2

    submission = autograder.assignment.GradedAssignment.from_dict(result['submission-result'])
    print(submission.report())
    return 0

def main():
    return run(_get_parser().parse_args())

def _get_parser():
    parser = autograder.api.courses.assignments.submissions.fetch.user.peek._get_parser()
    return parser

if (__name__ == '__main__'):
    sys.exit(main())
