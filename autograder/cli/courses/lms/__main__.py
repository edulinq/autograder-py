"""
The `autograder.cli.courses.lms` package contains tools for interacting with the given course's LMS.
All LMS operations are done within the context of the autograder.
For more general LMS functionality, see the [LMS Toolkit](https://github.com/edulinq/lms-toolkit).
"""

import sys

import edq.util.cli

def main() -> int:
    """ List this CLI dir. """

    return edq.util.cli.main()

if (__name__ == '__main__'):
    sys.exit(main())
