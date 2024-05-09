import sys

import autograder.api.report.fetchcourse

def run(arguments):
    result = autograder.api.report.fetchcourse.send(arguments, exit_on_error = True)

    if (not result['course-report']):
        print("No matching course report found.")
        return 1 
      
    return 0

def main():
    return run(_get_parser().parse_args())

def _get_parser():
    parser = autograder.api.report.fetchcourse._get_parser()
    return parser

if (__name__ == '__main__'):
    sys.exit(main())