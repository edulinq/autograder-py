import sys

import autograder.api.admin.coursereload

def run(arguments):
    autograder.api.admin.coursereload.send(arguments, exit_on_error = True)
    print("Course reloaded.")
    return 0

def main():
    return run(_get_parser().parse_args())

def _get_parser():
    return autograder.api.admin.coursereload._get_parser()

if (__name__ == '__main__'):
    sys.exit(main())
