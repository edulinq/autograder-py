import sys

import autograder.api.courses.assignments.submissions.submit
import autograder.assignment
import autograder.util.timestamp

def run(arguments):
    result = autograder.api.courses.assignments.submissions.submit.send(arguments,
            files = arguments.files, exit_on_error = True)

    message = result.get('message', '')
    if ((message is not None) and (message != '')):
        # Replace any timestamps in the message.
        message = autograder.util.timestamp.convert_message(message, pretty = True)

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
    parser = autograder.api.courses.assignments.submissions.submit._get_parser()

    parser.add_argument('files', metavar = 'FILE',
        action = 'store', type = str, nargs = '+',
        help = 'The path to your submission file(s).')

    return parser

if (__name__ == '__main__'):
    sys.exit(main())
