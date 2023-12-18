import sys

import autograder.api.admin.updatecourse

def run(arguments):
    result = autograder.api.admin.updatecourse.send(arguments, exit_on_error = True)

    if (result['course-updated']):
        print("Course updated.")
    else:
        print("Course not updated. The request was successful, does the course have a source?")

    return 0

def main():
    return run(_get_parser().parse_args())

def _get_parser():
    return autograder.api.admin.updatecourse._get_parser()

if (__name__ == '__main__'):
    sys.exit(main())
