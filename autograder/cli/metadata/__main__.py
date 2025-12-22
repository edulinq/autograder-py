"""
The `autograder.cli.metadata` package contains tools to access autograder metadata.
"""

import sys

import edq.util.cli

def main() -> int:
    """ List this CLI dir. """

    return edq.util.cli.main()

if (__name__ == '__main__'):
    sys.exit(main())
