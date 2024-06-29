"""
The `autograder.cli.grading` package contains tools to grade submissions
or help in the grading process.
"""

import sys

import autograder.util.cli

def main():
    autograder.util.cli.auto_list()
    return 0

if (__name__ == '__main__'):
    sys.exit(main())
