# pylint: disable=invalid-name

"""
Pull the code from a file and output the sanitized version as if it was being graded.
"""

import argparse
import sys

import edq.util.dirent

import autograder.cli.parser
import autograder.code

def run_cli(args: argparse.Namespace) -> int:
    """ Run the CLI. """

    text = autograder.code.extract_code(args.path)
    ast = autograder.code.parse_module_code(text)
    source = autograder.code.ast_to_source(ast)

    if (args.out_path is None):
        print(source)
        return 0

    edq.util.dirent.write_file(args.out_path, source)

    return 0

def main() -> int:
    """ Get a parser, parse the args, and call run. """
    return run_cli(_get_parser().parse_args())

def _get_parser() -> argparse.ArgumentParser:
    parser = autograder.cli.parser.get_parser(__doc__.strip())

    parser.add_argument('path', metavar = 'PATH',
        action = 'store', type = str,
        help = 'Path to the file to extract code from.')

    parser.add_argument('-o', '--out-path', dest = 'out_path',
        action = 'store', type = str, default = None,
        help = 'If specified, the code will be written here instead of output on stdout.')

    return parser

if (__name__ == '__main__'):
    sys.exit(main())
