"""
The `autograder.cli.grading` package contains tools to grade submissions
or help in the grading process.
"""

import sys

import autograder.util.cli

def main():
    return autograder.util.cli.main()

if (__name__ == '__main__'):
    sys.exit(main())
