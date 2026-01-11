"""
The `autograder.cli.courses.assignment.submissions.fetch` package contains tools to
query submissions to the autograder.
"""

import sys

import edq.util.cli

def main() -> int:
    """ List this CLI dir. """

    return edq.util.cli.main()

if (__name__ == '__main__'):
    sys.exit(main())
