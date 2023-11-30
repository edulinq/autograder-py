import sys

import autograder.api.submission.submit
import autograder.assignment

def run(arguments):
    result = autograder.api.submission.submit.send(arguments, arguments.files, exit_on_error = True)

    if (not result['grading-success']):
        print("Grading failed.")
        return 1

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
