"""
The `autograder.cli.courses.assignment.submissions.fetch` package contains tools to
query submissions to the autograder.
"""

import sys

import autograder.util.cli

def main():
    autograder.util.cli.auto_list()
    return 0

if (__name__ == '__main__'):
    sys.exit(main())
