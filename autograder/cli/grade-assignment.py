import sys

import autograder.cmd.gradeassignment

def main():
    return autograder.cmd.gradeassignment.main()

def _get_parser():
    return autograder.cmd.gradeassignment._get_parser()

if (__name__ == '__main__'):
    sys.exit(main())
