import os

import edq.util.gzip
import edq.util.encoding

THIS_DIR: str = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
ROOT_DIR: str = os.path.join(THIS_DIR, '..', '..')
TESTDATA_DIR: str = os.path.join(ROOT_DIR, 'testdata')

NOCOMPILE_PYTHON_PATH: str = os.path.join(THIS_DIR, '..', 'testdata', 'submission', 'nocompile', 'submission.py')

SUBMODULE_TESTDATA_DIR: str = os.path.join(TESTDATA_DIR, 'autograder-testdata')
SUBMODULE_SERVER_DIR: str = os.path.join(SUBMODULE_TESTDATA_DIR, 'autograder-server')
SUBMODULE_SERVER_TESTDATA_DIR: str = os.path.join(SUBMODULE_SERVER_DIR, 'testdata')

SUBMODULE_SERVER_USERS_PATH: str = os.path.join(SUBMODULE_SERVER_TESTDATA_DIR, 'users.json')
COURSE_101_DIR: str = os.path.join(SUBMODULE_SERVER_DIR, SUBMODULE_SERVER_TESTDATA_DIR, 'course101')
COURSE_LANGUAGES_DIR: str = os.path.join(SUBMODULE_SERVER_DIR, SUBMODULE_SERVER_TESTDATA_DIR, 'course-languages')

COURSE_101_CONFIG_FILE: str = os.path.join(COURSE_101_DIR, 'course.json')
COURSE_LANGUAGES_CONFIG_FILE: str = os.path.join(COURSE_LANGUAGES_DIR, 'course.json')

TEST_SUBMISSIONS_BASH_DIR: str = os.path.join(COURSE_LANGUAGES_DIR, 'bash', 'test-submissions')
TEST_SUBMISSIONS_BASH_SOLUTION_PATH: str = os.path.join(TEST_SUBMISSIONS_BASH_DIR, 'solution', 'assignment.sh')
TEST_SUBMISSIONS_BASH_NI_PATH: str = os.path.join(TEST_SUBMISSIONS_BASH_DIR, 'not-implemented', 'assignment.sh')
TEST_SUBMISSIONS_BASH_BAD_PATH: str = os.path.join(TEST_SUBMISSIONS_BASH_DIR, 'solution', 'test-submission.json')
TEST_SUBMISSIONS_BASH_CRASH_PATH: str = os.path.join(TEST_SUBMISSIONS_BASH_DIR, 'crash', 'assignment.sh')

COURSE_101_ZIP_PATH: str = os.path.join(TESTDATA_DIR, 'data', 'course101.zip')

TEST_TIMESTAMP: int = 123456789

TEST_PAYLOAD_STR: str = "Hello, World!\n"
TEST_PAYLOAD_BYTES: bytes = TEST_PAYLOAD_STR.encode(edq.util.dirent.DEFAULT_ENCODING)
TEST_PAYLOAD_GZIP_BYTES: bytes = edq.util.gzip.compress(TEST_PAYLOAD_BYTES)
TEST_PAYLOAD_B64_GZIP_BYTES: str = edq.util.encoding.to_base64(TEST_PAYLOAD_GZIP_BYTES)

TEST_BASE_VERSION: str = '1.2.3'
TEST_GIT_HASH: str = 'abcd1234'
TEST_IS_DIRTY: bool = False

TEST_TOKEN_CLEARTEXT: str = 'test-token-cleartext'
TEST_TOKEN_ID: str = 'test-token-id'

TEST_CRASH_EPILOGUE: str = ("Submission could not be graded because of the following error:"
        + "\n<TESTING STACK TRACE>"
        + "\nModuleNotFoundError: No module named 'ZZZ'")
