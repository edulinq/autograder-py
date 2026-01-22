"""
The `autograder.cli.system` package contains tools for interacting with the system/server running the autograder.
"""

import sys

import edq.util.cli

def main() -> int:
    """ List this CLI dir. """

    return edq.util.cli.main()

if (__name__ == '__main__'):
    sys.exit(main())
