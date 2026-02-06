import os

THIS_DIR: str = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
ROOT_DIR: str = os.path.join(THIS_DIR, '..', '..')
TESTDATA_DIR: str = os.path.join(ROOT_DIR, 'testdata')

NOCOMPILE_PYTHON_PATH: str = os.path.join(THIS_DIR, '..', 'testdata', 'submission', 'nocompile', 'submission.py')

SUBMODULE_TESTDATA_DIR: str = os.path.join(TESTDATA_DIR, 'autograder-testdata')
SUBMODULE_SERVER_DIR: str = os.path.join(SUBMODULE_TESTDATA_DIR, 'autograder-server')

COURSE_101_DIR: str = os.path.join(SUBMODULE_SERVER_DIR, 'testdata', 'course101')
COURSE_LANGUAGES_DIR: str = os.path.join(SUBMODULE_SERVER_DIR, 'testdata', 'course-languages')

COURSE_101_CONFIG_FILE: str = os.path.join(COURSE_101_DIR, 'course.json')
COURSE_LANGUAGES_CONFIG_FILE: str = os.path.join(COURSE_LANGUAGES_DIR, 'course.json')

TEST_SUBMISSIONS_BASH_DIR: str = os.path.join(COURSE_LANGUAGES_DIR, 'bash', 'test-submissions')
TEST_SUBMISSIONS_BASH_SOLUTION_PATH: str = os.path.join(TEST_SUBMISSIONS_BASH_DIR, 'solution', 'assignment.sh')
TEST_SUBMISSIONS_BASH_NI_PATH: str = os.path.join(TEST_SUBMISSIONS_BASH_DIR, 'not-implemented', 'assignment.sh')
TEST_SUBMISSIONS_BASH_BAD_PATH: str = os.path.join(TEST_SUBMISSIONS_BASH_DIR, 'solution', 'test-submission.json')
TEST_SUBMISSIONS_BASH_CRASH_PATH: str = os.path.join(TEST_SUBMISSIONS_BASH_DIR, 'crash', 'assignment.sh')

COURSE_101_ZIP_PATH: str = os.path.join(TESTDATA_DIR, 'data', 'course101.zip')
