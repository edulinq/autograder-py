import sys

import autograder.api.submissions.submit
import autograder.assignment

def run(arguments):
    result = autograder.api.submissions.submit.send(arguments, arguments.files,
            exit_on_error = True)

    message = result['message']
    if (message != ''):
        print("--- Message from Autograder ---")
        print(message)
        print("-------------------------------")

    if (result['rejected']):
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
    parser = autograder.api.submissions.submit._get_parser()

    parser.add_argument('files', metavar = 'FILE',
        action = 'store', type = str, nargs = '+',
        help = 'The path to your submission file(s).')

    return parser

if (__name__ == '__main__'):
    sys.exit(main())
