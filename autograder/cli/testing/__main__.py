"""
The `autograder.cli.testing` package contains tools to
test, debug, and develop courses and assignments.
"""

import sys

import autograder.util.cli

def main():
    return autograder.util.cli.main()

if (__name__ == '__main__'):
    sys.exit(main())
