"""
The `autograder.cli.testing` package contains tools for testing.
"""

import sys

import autograder.util.cli

def main() -> int:
    return autograder.util.cli.main()

if (__name__ == '__main__'):
    sys.exit(main())
