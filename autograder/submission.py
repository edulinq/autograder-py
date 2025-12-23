import glob
import json
import os
import subprocess
import sys
import traceback
import typing

import edq.util.dirent
import edq.util.json
import edq.util.time

import autograder.assignment
import autograder.fileop
import autograder.filespec

TEST_SUBMISSION_FILENAME: str = 'test-submission.json'
GRADER_FILENAME: str = 'grader.py'
GRADING_RESULT_FILENAME: str = 'result.json'

CONFIG_KEY_STATIC_FILES: str = 'static-files'
CONFIG_KEY_PRE_STATIC_OPS: str = 'pre-static-file-ops'
CONFIG_KEY_POST_STATIC_OPS: str = 'post-static-file-ops'
CONFIG_KEY_POST_SUB_OPS: str = 'post-submission-file-ops'

INPUT_DIRNAME: str = 'input'
OUTPUT_DIRNAME: str = 'output'
WORK_DIRNAME: str = 'work'

def copy_assignment_files(
        source_dir: str,
        dest_dir: str,
        op_dir: str,
        files: typing.List[str],
        only_contents = False,
        pre_ops: typing.Union[typing.List[autograder.fileop.FileOp], None] = None,
        post_ops: typing.Union[typing.List[autograder.fileop.FileOp], None] = None,
        ) -> None:
    """
    Copy over assignment files.

    Full procedure::
    1) Do pre-copy operations.
    2) Copy.
    3) Do post-copy operations.
    """

    if (pre_ops is None):
        pre_ops = []

    if (post_ops is None):
        post_ops = []

    # Do pre operations.
    autograder.fileop.exec_file_operations(pre_ops, op_dir)

    # Copy over the assignment's files.
    for filespec_text in files:
        spec = autograder.filespec.parse(filespec_text)
        autograder.filespec.copy(spec, source_dir, dest_dir, only_contents)

    # Do post operations.
    autograder.fileop.exec_file_operations(post_ops, op_dir)

def fetch_test_submissions(path: str) -> typing.List[str]:
    """
    Fetch all test submission files (named TEST_SUBMISSION_FILENAME) within the given path,
    or the path itself if it is already pointing to a test submission.
    """

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

def prep_grading_dir(
        assignment_config_path: str,
        submission_dir: str,
        grading_dir: typing.Union[str, None] = None,
        skip_static = False,
        ) -> str:
    """
    Create and return a directory for grading a submission.

    Procedure:
    1) If the base out dir is None, create a temp dir.
    2) Create the three core directories (input/output/work) in the base dir.
    3) Copy over the static files (includng pre/post operations).
    4) Copy over the submission files (includng pre/post operations).
    5) Return the dirs.
    """

    if (grading_dir is None):
        grading_dir = edq.util.dirent.get_temp_path(prefix = 'ag-py-submission-')

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

def make_core_dirs(base_dir: str) -> typing.Tuple[str, str, str]:
    """
    Create and return the three core grading directories (input, output, work).
    """

    input_dir = os.path.join(base_dir, INPUT_DIRNAME)
    os.makedirs(input_dir, exist_ok = True)

    output_dir = os.path.join(base_dir, OUTPUT_DIRNAME)
    os.makedirs(output_dir, exist_ok = True)

    work_dir = os.path.join(base_dir, WORK_DIRNAME)
    os.makedirs(work_dir, exist_ok = True)

    return input_dir, output_dir, work_dir

def run_test_submission(assignment_config_path: str, submission_config_path: str) -> bool:
    """ Run a test submission and return if the output matches the expected submission output. """

    print("Testing assignment '%s' and submission '%s'." % (assignment_config_path,
        submission_config_path))

    grading_dir = prep_grading_dir(assignment_config_path, os.path.dirname(submission_config_path))

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

def compare_test_submission(
        test_config_path: str,
        actual_result: autograder.assignment.GradedAssignment,
        print_result: bool = True,
        ) -> bool:
    """
    Compare a grading result against the expected output of a test submission.
    Return true if the two match.
    """

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

def run_submission(
        grading_dir: str,
        assignment_config_path: typing.Union[str, None] = None,
        grader_path: typing.Union[str, None] = None,
        ) -> typing.Union[autograder.assignment.GradedAssignment, None]:
    """
    Run a submission from a pre-populated grading directory and return the result.
    The grader path (or default grader path) will be checked first for a Python grader (GRADER_FILENAME),
    which will be run if it exists.
    Otherwise, the assignment config will be checked for the grader.
    """

    if (grader_path is None):
        grader_path = os.path.join(grading_dir, WORK_DIRNAME, GRADER_FILENAME)

    if (os.path.exists(grader_path)):
        return run_python_grader(grader_path, grading_dir)

    if (assignment_config_path is None):
        raise ValueError("No assignment config path has been supplied for running a grader.")

    return run_external_grader(assignment_config_path, grading_dir)

def run_python_grader(grader_path: str, grading_dir: str) -> typing.Union[autograder.assignment.GradedAssignment, None]:
    """
    Run a standard Python-based grader.
    Returns None on grading failure.
    """

    input_dir = os.path.join(grading_dir, INPUT_DIRNAME)
    output_dir = os.path.join(grading_dir, OUTPUT_DIRNAME)
    work_dir = os.path.join(grading_dir, WORK_DIRNAME)

    assignment_class = autograder.assignment.fetch_assignment_class(grader_path)
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

def run_external_grader(assignment_config_path: str, grading_dir: str) -> autograder.assignment.GradedAssignment:
    """ Run a grader that is not a standard Python-based grader. """

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

class SubmissionSummary(edq.util.json.DictConverter):
    """
    A summary of a grading submission.
    """

    def __init__(self,
            id: str = '',
            max_points: float = 0,
            score: float = 0,
            message: str = '',
            grading_start_time: typing.Union[edq.util.time.Timestamp, int, None] = None,
            **kwargs: typing.Any):
        self.id: str = id
        """ An identifier for this submission. """

        self.max_points: float = max_points
        """ The maximum number of points possible for this assignment (excluding extra credit). """

        self.score: float = score
        """ The score earned for this submission. """

        self.message: str = message
        """ A message/feedback for the student. """

        if (grading_start_time is None):
            grading_start_time = edq.util.time.Timestamp()

        self.grading_start_time: typing.Any = edq.util.time.Timestamp(grading_start_time)
        """ When grading started. """

    def to_dict(self) -> typing.Dict[str, typing.Any]:
        return {
            'id': self.id,
            'max_points': self.max_points,
            'score': self.score,
            'message': self.message,
            'grading_start_time': self.grading_start_time,
        }

    @staticmethod
    def from_dict(data: typing.Dict[str, typing.Any]) -> 'SubmissionSummary':
        return SubmissionSummary(**data)

    def short_id(self) -> str:
        """ Get the short ID for this submission. """

        return self.id.split('::')[-1]

    def __repr__(self) -> str:
        message = '.'
        if ((self.message is not None) and (self.message != '')):
            message = ", Message: '%s'." % (self.message)

        return f"Submission ID: {self.short_id()}, Score: {self.score} / {self.max_points}, Time: {self.grading_start_time.pretty()}{message}"
