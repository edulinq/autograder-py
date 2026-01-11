"""
The `autograder.cli.courses.assignment.submissions.fetch.user` package contains tools to
query submissions to the autograder at a user level.
"""

import sys

import edq.util.cli

def main() -> int:
    """ List this CLI dir. """

    return edq.util.cli.main()

if (__name__ == '__main__'):
    sys.exit(main())
