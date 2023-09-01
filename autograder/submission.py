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
GRADER_FILENAME = 'grader.py'

CONFIG_KEY_STATIC_FILES = 'static-files'
CONFIG_KEY_PRE_STATIC_OPS = 'pre-static-files-ops'
CONFIG_KEY_POST_STATIC_OPS = 'post-static-files-ops'
CONFIG_KEY_POST_SUB_OPS = 'post-submission-files-ops'

def do_file_operation(operation, op_dir):
    if ((operation is None) or (len(operation) == 0)):
        raise ValueError("File operation is empty.")

    if (operation[0] == 'mv'):
        if (len(operation) != 3):
            raise ValueError("Incorrect number of argument for 'mv' file operation. Expected 2, found %d." % ((len(operation) - 1)))

        shutil.move(os.path.join(op_dir, operation[1]), os.path.join(op_dir, operation[2]))
    elif (operation[0] == 'cp'):
        if (len(operation) != 3):
            raise ValueError("Incorrect number of argument for 'cp' file operation. Expected 2, found %d." % ((len(operation) - 1)))

        autograder.utils.copy_dirent(os.path.join(op_dir, operation[1]), os.path.join(op_dir, operation[2]))
    else:
        raise ValueError("Unknown file operation: '%s'." % (operation[0]))

def copy_assignment_files(source_dir, dest_dir, op_dir, files,
        only_contents = False, pre_ops = [], post_ops = []):
    """
    Copy over assignment files:
    1) Do pre-copy operations.
    2) Copy.
    3) Do post-copy operations.
    """

    # Do pre operations.
    for file_operation in pre_ops:
        do_file_operation(file_operation, op_dir)

    # Copy over the assignment's files.
    for filename in files:
        source_path = os.path.join(source_dir, filename)
        dest_path = os.path.join(dest_dir, os.path.basename(filename))

        if (only_contents):
            autograder.utils.copy_dirent_contents(source_path, dest_path)
        else:
            autograder.utils.copy_dirent(source_path, dest_path)

    # Do post operations.
    for file_operation in post_ops:
        do_file_operation(file_operation, op_dir)

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

def prep_temp_grading_dir(assignment_config_path, submission_dir, debug = False):
    """
    Create a directory for grading a submission.
    1) Create a temp dir.
    2) Create the three core directories (input/output/work) in the temp dir.
    3) Copy over the static files (includng pre/post operations).
    4) Copy over the submission files (includng pre/post operations).
    5) Load the grader class.
    6) Return the temp dir and grader class.
    """

    temp_dir = autograder.utils.get_temp_path(prefix = 'autograder-submission-',
            rm = (not debug))
    os.makedirs(temp_dir)

    if (debug):
        print("Using temp/work dir: '%s'." % (temp_dir))

    input_dir, output_dir, work_dir = prep_grading_dir(assignment_config_path, temp_dir, submission_dir)

    grader_path = os.path.join(work_dir, GRADER_FILENAME)
    assignment_class = autograder.assignment.fetch_assignment(grader_path)

    return ((input_dir, output_dir, work_dir), assignment_class)

def make_core_dirs(base_dir):
    """
    Make the three core directories.
    """

    input_dir = os.path.join(base_dir, 'input')
    os.makedirs(input_dir, exist_ok = True)

    output_dir = os.path.join(base_dir, 'output')
    os.makedirs(output_dir, exist_ok = True)

    work_dir = os.path.join(base_dir, 'work')
    os.makedirs(work_dir, exist_ok = True)

    return input_dir, output_dir, work_dir

def prep_grading_dir(assignment_config_path, base_dir, submission_dir, skip_static = False):
    input_dir, output_dir, work_dir = make_core_dirs(base_dir)

    # Load the assignment config.

    assignment_config_path = os.path.abspath(assignment_config_path)
    assignment_base_dir = os.path.dirname(assignment_config_path)

    try:
        with open(assignment_config_path, 'r') as file:
            assignment_config = json.load(file)
    except Exception as ex:
        raise ValueError("Failed to load assignment config: " + assignment_config_path) from ex

    if (not skip_static):
        # Copy static files.
        copy_assignment_files(assignment_base_dir, work_dir, base_dir,
                assignment_config.get(CONFIG_KEY_STATIC_FILES, []),
                pre_ops = assignment_config.get(CONFIG_KEY_PRE_STATIC_OPS, []),
                post_ops = assignment_config.get(CONFIG_KEY_POST_STATIC_OPS, []))

    # Copy submission files.
    copy_assignment_files(submission_dir, input_dir, base_dir,
            ['.'], only_contents = True,
            pre_ops = [],
            post_ops = assignment_config.get(CONFIG_KEY_POST_SUB_OPS, []))

    return input_dir, output_dir, work_dir

def run_test_submission(assignment_config_path, submission_config_path, debug = False):
    print("Testing assignment '%s' and submission '%s'." % (assignment_config_path, submission_config_path))

    dirs, assignment_class = prep_temp_grading_dir(assignment_config_path,
        os.path.dirname(submission_config_path), debug = debug)
    input_dir, output_dir, work_dir = dirs

    if (assignment_class is None):
        return False

    actual_result = run_submission(assignment_class, input_dir, output_dir, work_dir)
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

def run_submission(assignment_class, input_dir, output_dir, work_dir):
    try:
        assignment = assignment_class(input_dir = input_dir, output_dir = output_dir, work_dir = work_dir)
        return assignment.grade()
    except Exception as ex:
        print("Failed to run assignment (%s) on submission '%s': '%s'." % (assignment_class.__name__, input_dir, ex))
        traceback.print_exc()
        return None

    return result
