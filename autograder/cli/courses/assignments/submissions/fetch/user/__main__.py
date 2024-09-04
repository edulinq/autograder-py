"""
The `autograder.cli.courses.assignment.submissions.fetch.user` package contains tools to
query submissions to the autograder at a user level.
"""

import sys

import autograder.util.cli

def main():
    return autograder.util.cli.main()

if (__name__ == '__main__'):
    sys.exit(main())
