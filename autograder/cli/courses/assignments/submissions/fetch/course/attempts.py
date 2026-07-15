"""
Get all recent submissions and grading information for this assignment.
"""

import argparse
import sys

import autograder.api.courses.assignments.submissions.fetch.course.attempts
import autograder.cli.parser
import autograder.util.grading

def run_cli(args: argparse.Namespace) -> int:
    """ Run the CLI. """

    config = args._config_info.application_config

    grading_results = autograder.api.courses.assignments.submissions.fetch.course.attempts.send(config, exit_on_error = True)

    count = 0
    for grading_result in grading_results.values():
        if (grading_result is None):
            continue

        autograder.util.grading.output_grading_result(grading_result, base_dir = config.out_dir)
        count += 1

    print(f"Wrote {count} attempts to '{config.out_dir}'.")

    return 0

def main() -> int:
    """ Get a parser, parse the args, and call run. """

    return run_cli(_get_parser().parse_args())

def _get_parser() -> argparse.ArgumentParser:
    """ Get a parser for this operation. """

    parser = autograder.cli.parser.get_parser(
        __doc__.strip(),
        autograder.api.courses.assignments.submissions.fetch.course.attempts.API_PARAMS)

    return parser

if (__name__ == '__main__'):
    sys.exit(main())
