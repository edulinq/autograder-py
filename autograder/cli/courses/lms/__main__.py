"""
The `autograder.cli.courses.lms` package contains tools for
interacting with the given course's LMS.
"""

import sys

import autograder.util.cli

def main():
    return autograder.util.cli.main()

if (__name__ == '__main__'):
    sys.exit(main())
