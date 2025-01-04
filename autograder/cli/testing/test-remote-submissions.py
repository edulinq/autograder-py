import os
import sys
import traceback

import autograder.api.courses.assignments.submissions.submit
import autograder.submission

def run(arguments):
    try:
        test_submissions = autograder.submission.fetch_test_submissions(arguments.submissions)
    except Exception as ex:
        print("Failed to load submission(s) from '%s': '%s'." % (arguments.submissions, ex))
        traceback.print_exc()
        return 101

    errors = 0
    for test_submission in test_submissions:
        paths = _get_files(test_submission)

        try:
            result = autograder.api.courses.assignments.submissions.submit.send(arguments,
                    files = paths)
        except Exception as ex:
            print("Failed to run submission '%s': '%s'." % (test_submission, ex))
            traceback.print_exc()
            errors += 1
            continue

        if (not result['grading-success']):
            print("Autograder failed to grade the submission.")
            errors += 1
            continue

        result = autograder.assignment.GradedAssignment.from_dict(result['result'])
        if (not autograder.submission.compare_test_submission(test_submission, result)):
            errors += 1

    print("Encountered %d error(s) while testing %d submissions." % (errors, len(test_submissions)))

    if (errors > 0):
        print("Faiure")
    else:
        print("Success")

    return errors

def _get_files(test_submission):
    paths = []

    test_submission = os.path.abspath(test_submission)

    submission_dir = os.path.dirname(test_submission)
    for dirent in os.listdir(submission_dir):
        path = os.path.join(submission_dir, dirent)
        if (not os.path.samefile(test_submission, path)):
            paths.append(path)

    return paths

def _get_parser():
    parser = autograder.api.courses.assignments.submissions.submit._get_parser()

    parser.description = ('Submit multiple assignments to an autograder'
        + ' and ensure the output is as expected.')

    parser.add_argument('submissions', metavar = 'SUBMISSIONS_DIR',
        action = 'store', type = str,
        help = 'The path to a dir containing one or more test submissions.')

    return parser

def main():
    return run(_get_parser().parse_args())

if (__name__ == '__main__'):
    sys.exit(main())
