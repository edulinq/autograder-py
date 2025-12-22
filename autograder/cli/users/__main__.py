"""
The `autograder.cli.users` package contains tools to manage autograder users.
"""

import sys

import autograder.util.cli

def main() -> int:
    return autograder.util.cli.main()

if (__name__ == '__main__'):
    sys.exit(main())
