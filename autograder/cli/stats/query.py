"""
Query stats for the server.
"""

import argparse
import sys

import lms.model.base

import autograder.api.stats.query
import autograder.cli.parser

def run_cli(args: argparse.Namespace) -> int:
    """ Run the CLI. """

    config = args._config_info.application_config

    records = autograder.api.stats.query.send(config, exit_on_error = True)

    output = lms.model.base.base_list_to_output_format(records, config.output_format,
            skip_headers = args.skip_headers,
            pretty_headers = args.pretty_headers,
            include_extra_fields = args.include_extra_fields,
    )
    print(output)

    return 0

def main() -> int:
    """ Get a parser, parse the args, and call run. """

    return run_cli(_get_parser().parse_args())

def _get_parser() -> argparse.ArgumentParser:
    """ Get a parser for this operation. """

    parser = autograder.cli.parser.get_parser(
        __doc__.strip(),
        autograder.api.stats.query.API_PARAMS,
        include_output_format = True,
    )

    return parser

if (__name__ == '__main__'):
    sys.exit(main())
