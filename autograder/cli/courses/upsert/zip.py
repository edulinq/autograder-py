"""
Upsert a course using a zip file or directory.
"""

import argparse
import os
import sys

import edq.util.json

import autograder.api.courses.upsert.zip
import autograder.cli.parser
import autograder.error
import autograder.util.zip

def run_cli(args: argparse.Namespace) -> int:
    """ Run the CLI. """

    config = args._config_info.config

    try:
        zip_path = _prep_zip(args.path)
    except autograder.error.AutograderError as ex:
        print(str(ex))
        return 10

    result = autograder.api.courses.upsert.zip.send(config, post_paths = [zip_path], exit_on_error = True)
    print(edq.util.json.dumps(result, indent = 4))

    return 0

def _prep_zip(path: str) -> str:
    """
    Ensure that a zip file is ready for upload.
    If the path is already a zip, just return the existing path.
    If the path is a dir, zip it and return the new path.
    """

    if (not os.path.exists(path)):
        raise autograder.error.AutograderError(f"Path does not exist: '{path}'.")

    if (os.path.isfile(path)):
        extension = os.path.splitext(path)[1]
        if (extension != '.zip'):
            raise autograder.error.AutograderError(f"Expecting '.zip' extension, found '{extension}': '{path}'.")

        return path

    return autograder.util.zip.archive_dir(path)

def main() -> int:
    """ Get a parser, parse the args, and call run. """

    return run_cli(_get_parser().parse_args())

def _get_parser() -> argparse.ArgumentParser:
    """ Get a parser for this operation. """

    parser = autograder.cli.parser.get_parser(
        __doc__.strip(),
        autograder.api.courses.upsert.zip.API_PARAMS)

    return parser

if (__name__ == '__main__'):
    sys.exit(main())
