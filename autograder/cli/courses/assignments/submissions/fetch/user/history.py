"""
Get the most recent scores for this user and assignment.
"""

import argparse
import sys

import lms.model.base

import autograder.api.courses.assignments.submissions.fetch.user.history
import autograder.cli.parser

def run_cli(args: argparse.Namespace) -> int:
    """ Run the CLI. """

    config = args._config

    found_user, scores = autograder.api.courses.assignments.submissions.fetch.user.history.send(config)

    if (not found_user):
        print(f"No matching user found: '{config.get('target_email', '')}'.", file = sys.stderr)
        return 1

    output = lms.model.base.base_list_to_output_format(scores, args.output_format,
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
        autograder.api.courses.assignments.submissions.fetch.user.history.API_PARAMS,
        include_output_format = True)

    return parser

if (__name__ == '__main__'):
    sys.exit(main())
