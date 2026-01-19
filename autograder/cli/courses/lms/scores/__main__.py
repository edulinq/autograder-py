"""
The `autograder.cli.courses.lms.scores` package contains tools for working with assignment scores for a course's LMS.
"""

import sys

import edq.util.cli

def main() -> int:
    """ List this CLI dir. """

    return edq.util.cli.main()

if (__name__ == '__main__'):
    sys.exit(main())
