"""
Fetch an assignment's Docker image.
"""

import argparse
import os
import sys

import edq.util.dirent
import edq.util.encoding
import edq.util.json

import autograder.api.courses.assignments.images.fetch
import autograder.cli.parser

def run_cli(args: argparse.Namespace) -> int:
    """ Run the CLI. """

    config = args._config

    result = autograder.api.courses.assignments.images.fetch.send(config)

    print(edq.util.json.dumps(result['image-info'], indent = 4))
    print('---')

    if (not result['image-info']['built']):
        print("Image has not been built, nothing to write to disk.")
        return 1

    edq.util.dirent.mkdir(args.out_dir)
    out_path = os.path.abspath(os.path.join(args.out_dir, result['image-info']['name'] + '.tar.gz'))

    gzip_bytes = edq.util.encoding.from_base64(result['bytes'])
    edq.util.dirent.write_file_bytes(out_path, gzip_bytes)
    print(f"Wrote image '{result['image-info']['name']}' to '{out_path}'.")

    return 0

def main() -> int:
    """ Get a parser, parse the args, and call run. """

    return run_cli(_get_parser().parse_args())

def _get_parser() -> argparse.ArgumentParser:
    """ Get a parser for this operation. """

    parser = autograder.cli.parser.get_parser(
        __doc__.strip(),
        autograder.api.courses.assignments.images.fetch.API_PARAMS)

    return parser

if (__name__ == '__main__'):
    sys.exit(main())
