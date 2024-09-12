import sys

import autograder.api.courses.admin.update

def run(arguments):
    result = autograder.api.courses.admin.update.send(arguments, exit_on_error = True)

    if (result['course-updated']):
        print("Course updated.")
    else:
        print("Course not updated.")
        print("The request to the server was successful, no errors were encountered.")
        print("Does the course have a source?")

    return 0

def main():
    return run(_get_parser().parse_args())

def _get_parser():
    return autograder.api.courses.admin.update._get_parser()

if (__name__ == '__main__'):
    sys.exit(main())
