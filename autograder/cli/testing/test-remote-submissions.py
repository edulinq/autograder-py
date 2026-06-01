# pylint: disable=invalid-name

"""
Submit multiple assignments to an autograder and ensure the output is as expected.
"""

import argparse
import os
import sys
import traceback
import typing

import autograder.cli.courses.assignments.submissions.common
import autograder.api.courses.assignments.submissions.submit
import autograder.cli.parser
import autograder.submission

def run_cli(args: argparse.Namespace) -> int:
    """ Run the CLI. """

    config = args._config_info.config

    try:
        test_submission_paths = autograder.submission.fetch_test_submissions(args.submissions)
    except Exception as ex:
        print(f"Failed to load submission(s) from '{args.submissions}': '{ex}'.")
        traceback.print_exc()
        return 101

    errors = 0
    for test_submission_path in sorted(test_submission_paths):
        paths = _get_files(test_submission_path)

        try:
            api_response, grading_result = autograder.api.courses.assignments.submissions.submit.send(config,
                    post_paths = paths, exit_on_error = True)
        except Exception as ex:
            print(f"Failed to run submission '{test_submission_path}': '{ex}'.")
            traceback.print_exc()
            errors += 1
            continue

        if (not api_response['grading-success']):
            print("Autograder failed to grade the submission.")
            errors += 1
            continue

        if (not autograder.submission.compare_test_submission(test_submission_path, grading_result)):
            errors += 1

    print(f"Encountered {errors} error(s) while testing {len(test_submission_paths)} submissions.")

    if (errors > 0):
        print("Faiure")
    else:
        print("Success")

    return errors

def _get_files(test_submission_path: str) -> typing.List[str]:
    """ Collect the submission file paths. """

    paths = []

    test_submission_path = os.path.abspath(test_submission_path)

    submission_dir = os.path.dirname(test_submission_path)
    for dirent in os.listdir(submission_dir):
        path = os.path.join(submission_dir, dirent)
        if (not os.path.samefile(test_submission_path, path)):
            paths.append(path)

    return paths

def main() -> int:
    """ Get a parser, parse the args, and call run. """

    return run_cli(_get_parser().parse_args())

def _get_parser() -> argparse.ArgumentParser:
    """ Get a parser for this operation. """

    parser = autograder.cli.parser.get_parser(
        __doc__.strip(),
        autograder.api.courses.assignments.submissions.submit.BASE_API_PARAMS)

    parser.add_argument('submissions', metavar = 'SUBMISSIONS_DIR',
        action = 'store', type = str,
        help = 'The path to a dir containing one or more test submissions.')

    return parser

if (__name__ == '__main__'):
    sys.exit(main())
