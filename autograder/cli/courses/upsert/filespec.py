"""
Upsert a course using a file specification (FileSpec).
"""

import argparse
import sys
import typing

import edq.util.json

import autograder.api.courses.upsert.filespec
import autograder.cli.parser
import autograder.filespec

def run_cli(args: argparse.Namespace) -> int:
    """ Run the CLI. """

    config = args._config

    config['filespec'] = _build_filespec(config)

    result = autograder.api.courses.upsert.filespec.send(config)
    print(edq.util.json.dumps(result, indent = 4))

    return 0

def _build_filespec(config: typing.Dict[str, typing.Any]) -> autograder.filespec.FileSpec:
    data = {
        'type': config['filespec_type'],
        'path': config['filespec_path'],
    }

    for base_key in ['reference', 'username', 'token']:
        value = config.get(f"filespec_{base_key}", None)
        if (value is None):
            continue

        data[base_key] = value

    return autograder.filespec.parse(data)

def main() -> int:
    """ Get a parser, parse the args, and call run. """

    return run_cli(_get_parser().parse_args())

def _get_parser() -> argparse.ArgumentParser:
    """ Get a parser for this operation. """

    parser = autograder.cli.parser.get_parser(
        __doc__.strip(),
        autograder.api.courses.upsert.filespec.API_PARAMS)

    return parser

if (__name__ == '__main__'):
    sys.exit(main())
