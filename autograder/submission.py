import glob
import json
import os
import shutil
import subprocess
import sys
import traceback

import autograder.assignment
import autograder.filespec
import autograder.util.dirent
import autograder.util.timestamp

TEST_SUBMISSION_FILENAME = 'test-submission.json'
GRADER_FILENAME = 'grader.py'
GRADING_RESULT_FILENAME = 'result.json'

CONFIG_KEY_STATIC_FILES = 'static-files'
CONFIG_KEY_PRE_STATIC_OPS = 'pre-static-files-ops'
CONFIG_KEY_POST_STATIC_OPS = 'post-static-files-ops'
CONFIG_KEY_POST_SUB_OPS = 'post-submission-files-ops'

INPUT_DIRNAME = 'input'
OUTPUT_DIRNAME = 'output'
WORK_DIRNAME = 'work'

def do_file_operation(operation, op_dir):
    if ((operation is None) or (len(operation) == 0)):
        raise ValueError("File operation is empty.")

    if (operation[0] == 'mv'):
        if (len(operation) != 3):
            raise ValueError("Incorrect number of argument for 'mv' file operation."
                + " Expected 2, found %d." % ((len(operation) - 1)))

        shutil.move(os.path.join(op_dir, operation[1]), os.path.join(op_dir, operation[2]))
    elif (operation[0] == 'cp'):
        if (len(operation) != 3):
            raise ValueError("Incorrect number of argument for 'cp' file operation."
                + " Expected 2, found %d." % ((len(operation) - 1)))

        autograder.util.dirent.copy(os.path.join(op_dir, operation[1]), os.path.join(op_dir,
            operation[2]))
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
    for filespec_text in files:
        spec = autograder.filespec.parse(filespec_text)
        autograder.filespec.copy(spec, source_dir, dest_dir, only_contents)

    # Do post operations.
    for file_operation in post_ops:
        do_file_operation(file_operation, op_dir)

def fetch_test_submissions(path):
    path = os.path.abspath(path)
    test_submissions = []

    if (os.path.isfile(path)):
        if (os.path.basename(path) != TEST_SUBMISSION_FILENAME):
            raise ValueError("Passed in submission is not named like a test submission ('%s')." % (
                TEST_SUBMISSION_FILENAME))

        test_submissions.append(path)
    else:
        test_submissions += glob.glob(os.path.join(path, '**', TEST_SUBMISSION_FILENAME),
                recursive = True)

    return test_submissions

def prep_grading_dir(assignment_config_path, submission_dir, grading_dir = None,
        skip_static = False, debug = False):
    """
    Create a directory for grading a submission.
    1) If the base out dir is None, create a temp dir.
    2) Create the three core directories (input/output/work) in the base dir.
    3) Copy over the static files (includng pre/post operations).
    4) Copy over the submission files (includng pre/post operations).
    5) Return the dirs.
    """

    if (grading_dir is None):
        grading_dir = autograder.util.dirent.get_temp_path(prefix = 'autograder-submission-',
                rm = (not debug))

    os.makedirs(grading_dir, exist_ok = True)

    input_dir, output_dir, work_dir = make_core_dirs(grading_dir)

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
        copy_assignment_files(assignment_base_dir, work_dir, grading_dir,
                assignment_config.get(CONFIG_KEY_STATIC_FILES, []),
                pre_ops = assignment_config.get(CONFIG_KEY_PRE_STATIC_OPS, []),
                post_ops = assignment_config.get(CONFIG_KEY_POST_STATIC_OPS, []))

    # Copy submission files.
    copy_assignment_files(submission_dir, input_dir, grading_dir,
        ['.'], only_contents = True,
        pre_ops = [],
        post_ops = assignment_config.get(CONFIG_KEY_POST_SUB_OPS, []))

    return grading_dir

def make_core_dirs(base_dir):
    """
    Make the three core directories.
    """

    input_dir = os.path.join(base_dir, INPUT_DIRNAME)
    os.makedirs(input_dir, exist_ok = True)

    output_dir = os.path.join(base_dir, OUTPUT_DIRNAME)
    os.makedirs(output_dir, exist_ok = True)

    work_dir = os.path.join(base_dir, WORK_DIRNAME)
    os.makedirs(work_dir, exist_ok = True)

    return input_dir, output_dir, work_dir

def run_test_submission(assignment_config_path, submission_config_path, debug = False):
    print("Testing assignment '%s' and submission '%s'." % (assignment_config_path,
        submission_config_path))

    grading_dir = prep_grading_dir(assignment_config_path,
        os.path.dirname(submission_config_path), debug = debug)

    try:
        # Keep track of new top-level keys in sys.modules (imports) after the submission runs.
        # This is to prevent any import of submission code that gets cached.
        # This is in no way a complete solution, but also does not matter when run in Docker.
        old_module_keys = set(sys.modules.keys())

        actual_result = run_submission(grading_dir, assignment_config_path = assignment_config_path)
    finally:
        new_module_keys = set(sys.modules.keys())
        for new_module_key in (new_module_keys - old_module_keys):
            # Numpy and SciPy are special cases that are sensitive to reloads.
            # Note that this would be a security concern (e.g., a submission hijacking numpy),
            # but this is not used in docker-based grading.
            if (new_module_key.startswith('numpy') or new_module_key.startswith('scipy')):
                continue

            if (new_module_key in sys.modules):
                del sys.modules[new_module_key]

    if (actual_result is None):
        return False

    return compare_test_submission(submission_config_path, actual_result)

def compare_test_submission(test_config_path, actual_result, print_result = True):
    with open(test_config_path, 'r') as file:
        test_config = json.load(file)

    expected_result = autograder.assignment.GradedAssignment.from_dict(test_config['result'])
    ignore_messages = test_config.get('ignore_messages', False)

    match = actual_result.equals(expected_result, ignore_messages = ignore_messages)

    if ((not match) and print_result):
        print("Submission does not match expected output: '%s'." % (test_config_path))
        print('Expected:')
        print(expected_result.report(prefix = '    '))
        print('---')
        print('Actual:')
        print(actual_result.report(prefix = '    '))
        print('---')

    return match

def run_submission(grading_dir, assignment_config_path = None, grader_path = None):
    if (grader_path is None):
        grader_path = os.path.join(grading_dir, WORK_DIRNAME, GRADER_FILENAME)

    if (os.path.exists(grader_path)):
        return run_python_grader(grader_path, grading_dir)

    return run_external_grader(assignment_config_path, grading_dir)

def run_python_grader(grader_path, grading_dir):
    input_dir = os.path.join(grading_dir, INPUT_DIRNAME)
    output_dir = os.path.join(grading_dir, OUTPUT_DIRNAME)
    work_dir = os.path.join(grading_dir, WORK_DIRNAME)

    assignment_class = autograder.assignment.fetch_assignment(grader_path)
    if (assignment_class is None):
        print("Failed to fetch assignment class from '%s'." % (grader_path))
        return None

    try:
        assignment = assignment_class(input_dir = input_dir, output_dir = output_dir,
                work_dir = work_dir)
        return assignment.grade()
    except Exception as ex:
        print("Failed to run assignment (%s) on submission '%s': '%s'." % (
            assignment_class.__name__, input_dir, ex))
        traceback.print_exc()
        return None

def run_external_grader(assignment_config_path, grading_dir):
    work_dir = os.path.join(grading_dir, WORK_DIRNAME)
    output_dir = os.path.join(grading_dir, OUTPUT_DIRNAME)

    try:
        with open(assignment_config_path, 'r') as file:
            assignment_config = json.load(file)
    except Exception as ex:
        raise ValueError("Failed to load assignment config: " + assignment_config_path) from ex

    invocation = assignment_config.get('invocation', [])
    if (len(invocation) == 0):
        raise ValueError(("External (any grader not using the standard Python setup)"
            + " graders must have a non-empty 'invocation' key in their assignment config."))

    subprocess.run(invocation, cwd = work_dir, check = True)

    out_path = os.path.join(output_dir, GRADING_RESULT_FILENAME)
    if (not os.path.isfile(out_path)):
        raise ValueError("Could not find result after external grader ran: '%s'." % (out_path))

    try:
        with open(out_path, 'r') as file:
            result = json.load(file)
    except Exception as ex:
        raise ValueError("Failed to grading result: " + out_path) from ex

    return autograder.assignment.GradedAssignment.from_dict(result)

class SubmissionSummary(object):
    """
    A summary of a grading submission.
    """

    def __init__(self,
            id = '',
            max_points = 0, score = 0,
            message = '',
            grading_start_time = None,
            **kwargs):
        self.id = id

        self.max_points = max_points
        self.score = score

        self.message = message

        self.grading_start_time = autograder.util.timestamp.MISSING_TIMESTAMP
        if (grading_start_time is not None):
            self.grading_start_time = autograder.util.timestamp.get(grading_start_time)

    def to_dict(self):
        """
        Convert to all simple structures that can be later converted to JSON.
        """

        return {
            'id': self.id,
            'max_points': self.max_points,
            'score': self.score,
            'message': self.message,
            'grading_start_time': self.grading_start_time,
        }

    @staticmethod
    def from_dict(data):
        """
        Partner to to_dict().
        """

        return SubmissionSummary(**data)

    def short_id(self):
        return self.id.split('::')[-1]

    def pretty_time(self):
        return autograder.util.timestamp.get(self.grading_start_time, pretty = True)

    def __repr__(self):
        """
        Get a string that represents the summary.
        """

        message = '.'
        if ((self.message is not None) and (self.message != '')):
            message = ", Message: '%s'." % (self.message)

        return "Submission ID: %s, Score: %s / %s, Time: %s%s" % (
            self.short_id(), self.score, self.max_points,
            self.pretty_time(),
            message)
