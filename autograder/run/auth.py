import sys

import autograder.cli.users.auth as alias

def main():
    return alias.run(_get_parser().parse_args())

def _get_parser():
    parser = alias._get_parser()
    parser.epilog = "This is an alias for `%s`." % (alias.__name__)
    return parser

if (__name__ == '__main__'):
    sys.exit(main())
