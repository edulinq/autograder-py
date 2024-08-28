"""
The `autograder.cli.courses.assignment.submissions.fetch.course` package contains tools to
query submissions to the autograder at a course level.
"""

import sys

import autograder.util.cli

def main():
    autograder.util.cli.auto_list()
    return 0

if (__name__ == '__main__'):
    sys.exit(main())
