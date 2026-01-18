"""
The `autograder.cli.grading` package contains tools to grade submissions or help in the grading process.
"""

import sys

import edq.util.cli

def main() -> int:
    """ List this CLI dir. """

    return edq.util.cli.main()

if (__name__ == '__main__'):
    sys.exit(main())
