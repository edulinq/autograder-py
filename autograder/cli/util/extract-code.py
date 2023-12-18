import argparse
import sys

import autograder.code

def run(args):
    text = autograder.code.extract_code(args.path)
    ast = autograder.code.sanitize_code(text)
    source = autograder.code.ast_to_source(ast)

    if (args.out_path is None):
        print(source)
        return 0

    with open(args.out_path, 'w') as file:
        file.write(source + "\n")

def _get_parser():
    parser = argparse.ArgumentParser(description =
        "Pull the code from a file and output the sanitized version as if it was being graded."
        + " Requires Python >= 3.9.")

    parser.add_argument('path', metavar = 'PATH',
        action = 'store', type = str,
        help = 'Path to the file to extract code from.')

    parser.add_argument('-o', '--out-path', dest = 'out_path',
        action = 'store', type = str, default = None,
        help = 'If specified, the code will be written here instead of output on stdout.')

    return parser

def main():
    return run(_get_parser().parse_args())

if (__name__ == '__main__'):
    sys.exit(main())
