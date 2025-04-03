"""
The `autograder.cli.courses.assignment.submissions.proxy` package contains tools to
make proxy submissions to the autograder.
"""

import sys

import autograder.util.cli

def main():
    return autograder.util.cli.main()

if (__name__ == '__main__'):
    sys.exit(main())
