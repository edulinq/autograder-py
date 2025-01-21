"""
The `autograder.cli.courses.assignment.submissions.analyze` package contains tools to
work with submission-level code analysis provided by the autograder.
"""

import sys

import autograder.util.cli

def main():
    return autograder.util.cli.main()

if (__name__ == '__main__'):
    sys.exit(main())
