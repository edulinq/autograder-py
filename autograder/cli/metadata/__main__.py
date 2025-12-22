"""
The `autograder.cli.metadata` package contains tools to access autograder metadata.
"""

import sys

import autograder.util.cli

def main() -> int:
    return autograder.util.cli.main()

if (__name__ == '__main__'):
    sys.exit(main())
