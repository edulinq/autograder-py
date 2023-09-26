import argparse
import sys
import traceback

import autograder.submission

DEFAULT_ASSIGNMENT = 'assignment.json'

def run(args):
    try:
        test_submissions = autograder.submission.fetch_test_submissions(args.submissions)
    except Exception as ex:
        print("Failed to load submission(s) from '%s': '%s'." % (args.submissions, ex))
        traceback.print_exc()
        return 101

    errors = 0
    for test_submission in test_submissions:
        success = False

        try:
            success = autograder.submission.run_test_submission(args.assignment,
                test_submission, args.debug)
        except Exception as ex:
            print("Failed to run submission '%s': '%s'." % (test_submission, ex))
            traceback.print_exc()

        if (not success):
            errors += 1

    print("Encountered %d error(s) while testing %d submissions." % (errors, len(test_submissions)))

    if (errors > 0):
        print("Faiure")
    else:
        print("Success")

    return errors

def _get_parser():
    parser = argparse.ArgumentParser(description =
        'Run a grader against multiple test assignments and ensure the output'
        + ' matches the expected output.')

    parser.add_argument('-a', '--assignment',
        action = 'store', type = str, required = False, default = DEFAULT_ASSIGNMENT,
        help = 'The path to a JSON file describing an assignment (default: %(default)s).')

    parser.add_argument('-s', '--submissions',
        action = 'store', type = str, required = True,
        help = 'The path to a dir containing one or more test submissions.')

    parser.add_argument('-d', '--debug', dest = 'debug',
        action = 'store_true', default = False,
        help = 'Enable additional output and leave behind grading artifacts (default: %(default)s)')

    return parser

def main():
    return run(_get_parser().parse_args())

if (__name__ == '__main__'):
    sys.exit(main())
