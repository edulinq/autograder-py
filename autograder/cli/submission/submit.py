import sys

import autograder.api.submission.submit
import autograder.assignment
from autograder.util.confirm import confirm

def run(arguments):
    result = autograder.api.submission.submit.send(arguments, arguments.files, exit_on_error = True)

    message = result['message']
    if (message != ''):
        print("--- Message from Autograder ---")
        print(message)
        print("-------------------------------")

    if (result['rejected']):
        if result['require-late-acknowledgment']:
            if confirm("This assignment is past the due date and the late policy will be applied. Do you want to continue?"):
                setattr(arguments, "late-acknowledgment", True)
                return run(arguments)
        print("Submission was rejected by the autograder.")
        return 1

    if (not result['grading-success']):
        print("Grading failed.")
        return 2

    submission = autograder.assignment.GradedAssignment.from_dict(result['result'])
    print(submission.report())
    return 0

def main():
    return run(_get_parser().parse_args())

def _get_parser():
    parser = autograder.api.submission.submit._get_parser()

    parser.add_argument('files', metavar = 'FILE',
        action = 'store', type = str, nargs = '+',
        help = 'The path to your submission file(s).')

    return parser

if (__name__ == '__main__'):
    sys.exit(main())
