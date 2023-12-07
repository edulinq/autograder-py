import sys
import autograder.api.submission.removesubmission

def run(arguments):
    result = autograder.api.submission.removesubmission.send(arguments, exit_on_error = True)
    if (result == 0):
        print("Invalid Input")
    elif (result == 1):
        print("Exiting program")
    elif (not result['found-user']):
        print("No matching user found.")
        return 1
    elif (not result['found-submission']):
        print("No matching submission found.")
        return 2
    else:
        print("Submission removed.")
    return 0
        


def main():
    return run(_get_parser().parse_args())

def _get_parser():
    parser = autograder.api.submission.removesubmission._get_parser()
    return parser

if (__name__ == '__main__'):
    sys.exit(main())
