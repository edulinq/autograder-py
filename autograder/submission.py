import argparse
import glob
import json
import os
import shutil
import sys
import traceback

import autograder.assignment
import autograder.code
import autograder.utils

TEST_SUBMISSION_FILENAME = 'test-submission.json'

def setup_submission(work_dir, assignment_config_path, submission_base_dir):
    """
    Set up a submission directory for testing:
        1) Load the assignment config.
        2) Copy over the assignment's static files.
        3) Load the assignment class.
        4) Copy over the submission files.
        5) Return the assignment class.
    """

    assignment_config_path = os.path.abspath(assignment_config_path)
    assignment_base_dir = os.path.dirname(assignment_config_path)

    # Load the assignment config.
    try:
        with open(assignment_config_path, 'r') as file:
            assignment_config = json.load(file)
    except Exception as ex:
        print("Failed to load assignment config '%s': '%s'." % (assignment_config_path, ex))
        traceback.print_exc()
        return None

    # Copy over the assignment's static files.
    try:
        static_files = assignment_config.get('static-files', [])
        for static_file in static_files:
            source_path = os.path.join(assignment_base_dir, static_file)
            dest_path = os.path.join(work_dir, static_file)

            shutil.copy2(source_path, dest_path)
    except Exception as ex:
        print("Failed to copy assignment's static files '%s': '%s'." % (assignment_config_path, ex))
        traceback.print_exc()
        return None

    # Load the assignment class from the static files that were just copied.
    assignment_class = None
    try:
        for dirent in os.listdir(work_dir):
            path = os.path.join(work_dir, dirent)
            if (os.path.splitext(dirent)[1] not in autograder.code.ALLOWED_EXTENSIONS):
                continue

        assignment_classes = autograder.assignment.load_assignments(path)
        if (len(assignment_classes) == 1):
            assignment_class = assignment_classes[0]
    except Exception as ex:
        print("Failed to load assignment class from '%s': '%s'." % (assignment_base_dir, ex))
        traceback.print_exc()
        return None

    if (assignment_class is None):
        print("Could not find assignment class for '%s'." % (assignment_config_path))
        return None

    # Copy over the submission files.
    try:
        autograder.utils.copy_contents(submission_base_dir, work_dir)
    except Exception as ex:
        print("Failed to copy submission files from '%s': '%s'." % (submission_base_dir, ex))
        traceback.print_exc()
        return None

    return assignment_class

def fetch_test_submissions(path):
    path = os.path.abspath(path)
    test_submissions = []

    if (os.path.isfile(path)):
        if (os.path.basename(path) != TEST_SUBMISSION_FILENAME):
            raise ValueError("Passed in submission file is not named like a test submission ('%s')." % (TEST_SUBMISSION_FILENAME))

        test_submissions.append(path)
    else:
        test_submissions += glob.glob(os.path.join(path, '**', TEST_SUBMISSION_FILENAME), recursive = True)

    return test_submissions

def prep_temp_work_dir(assignment_config_path, submission_dir, debug = False):
    temp_dir = autograder.utils.get_temp_path(prefix = 'autograder-submission-',
            rm = (not debug))
    os.makedirs(temp_dir)

    if (debug):
        print("Using temp/work dir: '%s'." % (temp_dir))

    assignment_class = setup_submission(temp_dir, assignment_config_path, submission_dir)

    return (temp_dir, assignment_class)

def run_test_submission(assignment_config_path, submission_config_path, debug = False):
    print("Testing assignment '%s' and submission '%s'." % (assignment_config_path, submission_config_path))

    temp_dir, assignment_class = prep_temp_work_dir(assignment_config_path,
        os.path.dirname(submission_config_path), debug = debug)

    if (assignment_class is None):
        return False

    actual_result = run_submission(assignment_class, temp_dir, temp_dir)
    if (actual_result is None):
        return False

    with open(submission_config_path, 'r') as file:
        submission_config = json.load(file)

    expected_result = autograder.assignment.GradedAssignment.from_dict(submission_config['result'])
    ignore_messages = submission_config.get('ignore_messages', False)

    if (actual_result.equals(expected_result, ignore_messages = ignore_messages)):
        return True

    print("Submission does not match expected output: '%s'." % (submission_config_path))
    print('Expected:')
    print(expected_result.report(prefix = '    '))
    print('---')
    print('Actual:')
    print(actual_result.report(prefix = '    '))
    print('---')

    return False

def run_submission(assignment_class, assignment_dir, submission_dir):
    try:
        submission = autograder.utils.prepare_submission(submission_dir)
        assignment = assignment_class(submission_dir = submission_dir, assignment_dir = assignment_dir)
        return assignment.grade(submission)
    except Exception as ex:
        print("Failed to run assignment (%s) on submission '%s': '%s'." % (assignment_class, submission_dir, ex))
        traceback.print_exc()
        return None

    return result
