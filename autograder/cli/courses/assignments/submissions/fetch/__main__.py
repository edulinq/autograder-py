"""
The `autograder.cli.courses.assignment.submissions.fetch` package contains tools to
query submissions to the autograder.
"""

import sys

import autograder.util.cli

def main():
    return autograder.util.cli.main()

if (__name__ == '__main__'):
    sys.exit(main())
