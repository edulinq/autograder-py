"""
The `autograder.cli.courses.assignment.submissions.fetch.course` package contains tools to
query submissions to the autograder at a course level.
"""

import sys

import autograder.util.cli

def main():
    return autograder.util.cli.main()

if (__name__ == '__main__'):
    sys.exit(main())
