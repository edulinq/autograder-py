import os
import unittest
import sys

import autograder.fileop
import autograder.util.dir
import autograder.util.file

ALREADY_EXISTS_DIRNAME = "already_exists"
ALREADY_EXISTS_FILENAME = "already_exists.txt"
ALREADY_EXISTS_FILE_POSIX_RELPATH = ALREADY_EXISTS_DIRNAME + "/" + ALREADY_EXISTS_FILENAME
ALREADY_EXISTS_FILE_RELPATH = os.path.join(ALREADY_EXISTS_DIRNAME, ALREADY_EXISTS_FILENAME)
ALREADY_EXISTS_FILENAME_ALT = "already_exists_alt.txt"
ALREADY_EXISTS_FILE_ALT_POSIX_RELPATH = ALREADY_EXISTS_DIRNAME + "/" + ALREADY_EXISTS_FILENAME_ALT
ALREADY_EXISTS_FILE_ALT_RELPATH = os.path.join(ALREADY_EXISTS_DIRNAME, ALREADY_EXISTS_FILENAME_ALT)
STARTING_EMPTY_DIRNAME = "empty_start"

class TestFileOp(unittest.TestCase):
    @unittest.skipIf(sys.platform.startswith("win"), "fileops require POSIX")
    def test_fileop_validation(self):
        test_cases = [
            # Base
            (["copy", "a", "b"], ["copy", "a", "b"], None),
            (["cp", "a", "b"], ["copy", "a", "b"], None),
            (["move", "a", "b"], ["move", "a", "b"], None),
            (["mv", "a", "b"], ["move", "a", "b"], None),
            (["make-dir", "a"], ["make-dir", "a"], None),
            (["mkdir", "a"], ["make-dir", "a"], None),
            (["remove", "a"], ["remove", "a"], None),
            (["rm", "a"], ["remove", "a"], None),

            # Casing
            (["Copy", "a", "b"], ["copy", "a", "b"], None),
            (["COPY", "a", "b"], ["copy", "a", "b"], None),
            (["CoPy", "a", "b"], ["copy", "a", "b"], None),

            # Normalize Paths
            (["copy", "c/../a", "b"], ["copy", "a", "b"], None),
            (["copy", "a/", "b"], ["copy", "a", "b"], None),
            (["copy", "a//b", "b"], ["copy", "a/b", "b"], None),
            (["copy", "./a", "b"], ["copy", "a", "b"], None),
            (["copy", "*/*/..", "b"], ["copy", "*", "b"], None),

            # Glob Paths
            (["copy", "a/*", "b"], ["copy", "a/*", "b"], None),
            (["copy", "a/?", "b"], ["copy", "a/?", "b"], None),
            (["move", "a/*", "b"], ["move", "a/*", "b"], None),
            (["move", "a/?", "b"], ["move", "a/?", "b"], None),
            # Validation does not raise an error on malformed globs.
            # They are treated as path literals, following glob.glob().
            (["copy", "*/[a-z", "b"], ["copy", "*/[a-z", "b"], None),

            # Errors

            # Empty
            (None, None, "File operation is None"),
            ([], None, "File operation is empty"),

            # Number of Args
            (["copy", "a"], None, "Incorrect number of arguments"),
            (["copy", "a", "b", "c"], None, "Incorrect number of arguments"),
            (["move", "a"], None, "Incorrect number of arguments"),
            (["move", "a", "b", "c"], None, "Incorrect number of arguments"),
            (["make-dir"], None, "Incorrect number of arguments"),
            (["make-dir", "a", "b"], None, "Incorrect number of arguments"),
            (["remove"], None, "Incorrect number of arguments"),
            (["remove", "a", "b"], None, "Incorrect number of arguments"),

            # Unknown Command
            (["zzz", "a", "b"], None, "Unknown file operation"),

            # Path Errors
            (["copy", "a\\b", "b"], None, "contains a backslash"),
            (["copy", "/a", "b"], None, "is an absolute path"),
            (["copy", "..", "b"], None, "points outside of the its base directory"),
            (["copy", "../a", "b"], None, "points outside of the its base directory"),
            (["copy", "a/../..", "b"], None, "points outside of the its base directory"),
            (["copy", "a/../../b", "b"], None, "points outside of the its base directory"),
            (["copy", "*/../..", "b"], None, "points outside of the its base directory"),
            (["copy", "*/../../*", "b"], None, "points outside of the its base directory"),
            (["copy", ".", "b"], None, "cannot point just to the current directory"),
            (["copy", "a/..", "b"], None, "cannot point just to the current directory"),
            (["copy", "*/..", "b"], None, "cannot point just to the current directory"),
        ]

        for i in range(len(test_cases)):
            with self.subTest(msg = f"Case {i}"):
                (operation, expected, error_substring) = test_cases[i]

                try:
                    autograder.fileop.validate(operation)
                except Exception as ex:
                    if (error_substring is None):
                        self.fail(f"Unexpected error: '{str(ex)}'.")

                    self.assertIn(error_substring, str(ex), 'Error is not as expected.')
                    continue

                if (error_substring is not None):
                    self.fail(f"Did not get expected error: '{error_substring}'.")

                self.assertListEqual(operation, expected, 'Operation not as expected.')

    @unittest.skipIf(sys.platform.startswith("win"), "fileops require POSIX")
    def test_fileop_exec_copy(self):
        test_cases = [
            (ALREADY_EXISTS_FILE_POSIX_RELPATH, "a", None),
            (ALREADY_EXISTS_FILE_POSIX_RELPATH, "a.txt", None),
            (ALREADY_EXISTS_DIRNAME, "a", None),
            (ALREADY_EXISTS_DIRNAME, "a.txt", None),
            (ALREADY_EXISTS_FILE_POSIX_RELPATH, ALREADY_EXISTS_DIRNAME + "/a", None),
            (ALREADY_EXISTS_FILE_POSIX_RELPATH, "a/b", None),
            (ALREADY_EXISTS_FILE_POSIX_RELPATH, ALREADY_EXISTS_DIRNAME, None),
            (ALREADY_EXISTS_FILENAME, ALREADY_EXISTS_DIRNAME, None),
            ("a", "b", "No such file or directory"),
            (ALREADY_EXISTS_DIRNAME, ALREADY_EXISTS_FILE_POSIX_RELPATH, "File exists"),
        ]

        for i in range(len(test_cases)):
            with self.subTest(msg = f"Case {i}"):
                (source, dest, error_substring) = test_cases[i]

                operation = ["cp", source, dest]

                def post_check(operation, temp_dir):
                    expected_source = os.path.normpath(os.path.join(temp_dir, source))
                    expected_dest = os.path.normpath(os.path.join(temp_dir, dest))

                    self.assertTrue(os.path.exists(expected_dest),
                        f"Dest does not exist '{expected_dest}'.")

                    self.assertTrue(os.path.exists(expected_source),
                        f"Source does not exist '{expected_source}'.")

                self._run_fileop_exec_test(operation, error_substring, post_check)

    @unittest.skipIf(sys.platform.startswith("win"), "fileops require POSIX")
    def test_fileop_exec_copy_glob(self):
        # [(source, dest, expected_paths, not_expected_paths, error_substring), ...]
        test_cases = [
            (
                ALREADY_EXISTS_DIRNAME + "/*",
                STARTING_EMPTY_DIRNAME,
                [
                    ALREADY_EXISTS_FILE_RELPATH,
                    ALREADY_EXISTS_FILE_ALT_RELPATH,
                    os.path.join(STARTING_EMPTY_DIRNAME, ALREADY_EXISTS_FILENAME),
                    os.path.join(STARTING_EMPTY_DIRNAME, ALREADY_EXISTS_FILENAME_ALT),
                ],
                [
                    os.path.join(STARTING_EMPTY_DIRNAME, ALREADY_EXISTS_DIRNAME)
                ],
                None
            ),
            (
                ALREADY_EXISTS_DIRNAME + "/*.txt",
                STARTING_EMPTY_DIRNAME,
                [
                    ALREADY_EXISTS_FILE_RELPATH,
                    ALREADY_EXISTS_FILE_ALT_RELPATH,
                    os.path.join(STARTING_EMPTY_DIRNAME, ALREADY_EXISTS_FILENAME),
                    os.path.join(STARTING_EMPTY_DIRNAME, ALREADY_EXISTS_FILENAME_ALT),
                ],
                [
                    os.path.join(STARTING_EMPTY_DIRNAME, ALREADY_EXISTS_DIRNAME)
                ],
                None
            ),
            (
                ALREADY_EXISTS_DIRNAME,
                STARTING_EMPTY_DIRNAME,
                [
                    ALREADY_EXISTS_DIRNAME,
                    ALREADY_EXISTS_FILE_RELPATH,
                    ALREADY_EXISTS_FILE_ALT_RELPATH,
                    os.path.join(STARTING_EMPTY_DIRNAME, ALREADY_EXISTS_DIRNAME),
                    os.path.join(STARTING_EMPTY_DIRNAME, ALREADY_EXISTS_FILE_RELPATH),
                    os.path.join(STARTING_EMPTY_DIRNAME, ALREADY_EXISTS_FILE_ALT_RELPATH),
                ],
                [],
                None
            ),
            (
                STARTING_EMPTY_DIRNAME,
                "a.txt",
                [
                    STARTING_EMPTY_DIRNAME,
                    "a.txt",
                ],
                [
                    os.path.join("a.txt", STARTING_EMPTY_DIRNAME)
                ],
                None
            ),
            (
                ALREADY_EXISTS_DIRNAME + "/*.txt",
                ALREADY_EXISTS_FILENAME,
                [],
                [],
                "File exists"
            ),
            (
                ALREADY_EXISTS_DIRNAME,
                ALREADY_EXISTS_FILENAME,
                [],
                [],
                "File exists"
            ),
        ]

        for i in range(len(test_cases)):
            with self.subTest(msg = f"Case {i}"):
                (source, dest, expected_paths, not_expected_paths, error_substring) = test_cases[i]

                operation = ["cp", source, dest]

                def post_check(operation, temp_dir):
                    for expected_path in expected_paths:
                        path = os.path.normpath(os.path.join(temp_dir, expected_path))
                        self.assertTrue(os.path.exists(path),
                                        f"Expected path does not exist '{path}'.")

                    for not_expected_path in not_expected_paths:
                        path = os.path.normpath(os.path.join(temp_dir, not_expected_path))
                        self.assertFalse(os.path.exists(path),
                                         f"Unexpected path exists '{path}'.")

                self._run_fileop_exec_test(operation, error_substring, post_check)

    @unittest.skipIf(sys.platform.startswith("win"), "fileops require POSIX")
    def test_fileop_exec_move(self):
        test_cases = [
            (ALREADY_EXISTS_FILE_POSIX_RELPATH, "a", None),
            (ALREADY_EXISTS_FILE_POSIX_RELPATH, "a.txt", None),
            (ALREADY_EXISTS_DIRNAME, "a", None),
            (ALREADY_EXISTS_DIRNAME, "a.txt", None),
            (ALREADY_EXISTS_FILE_POSIX_RELPATH, ALREADY_EXISTS_DIRNAME + "/a", None),
            ("a", "b", "No such file or directory"),
            (ALREADY_EXISTS_DIRNAME, ALREADY_EXISTS_FILE_POSIX_RELPATH, "into itself"),
            (ALREADY_EXISTS_FILENAME, ALREADY_EXISTS_DIRNAME, None),
        ]

        for i in range(len(test_cases)):
            with self.subTest(msg = f"Case {i}"):
                (source, dest, error_substring) = test_cases[i]

                operation = ["mv", source, dest]

                def post_check(operation, temp_dir):
                    expected_source = os.path.normpath(os.path.join(temp_dir, source))
                    expected_dest = os.path.normpath(os.path.join(temp_dir, dest))

                    self.assertTrue(os.path.exists(expected_dest),
                        f"Dest does not exist '{expected_dest}'.")

                    self.assertFalse(os.path.exists(expected_source),
                        f"Source exists '{expected_source}'.")

                self._run_fileop_exec_test(operation, error_substring, post_check)

    @unittest.skipIf(sys.platform.startswith("win"), "fileops require POSIX")
    def test_fileop_exec_move_glob(self):
        # [(source, dest, expected_paths, not_expected_paths, error_substring), ...]
        test_cases = [
            (
                "*",
                "a",
                [
                    os.path.join("a", ALREADY_EXISTS_FILENAME),
                    os.path.join("a", ALREADY_EXISTS_DIRNAME),
                    os.path.join("a", STARTING_EMPTY_DIRNAME),
                    os.path.join("a", ALREADY_EXISTS_FILE_RELPATH),
                    os.path.join("a", ALREADY_EXISTS_FILE_ALT_RELPATH),
                ],
                [
                    ALREADY_EXISTS_FILENAME,
                    ALREADY_EXISTS_DIRNAME,
                    STARTING_EMPTY_DIRNAME,
                    ALREADY_EXISTS_FILE_RELPATH,
                    ALREADY_EXISTS_FILE_ALT_RELPATH,
                ],
                None
            ),
            (
                ALREADY_EXISTS_DIRNAME,
                ALREADY_EXISTS_DIRNAME,
                [
                    ALREADY_EXISTS_FILENAME,
                    ALREADY_EXISTS_DIRNAME,
                    ALREADY_EXISTS_FILE_RELPATH,
                    ALREADY_EXISTS_FILE_ALT_RELPATH,
                    STARTING_EMPTY_DIRNAME,
                ],
                [
                    os.path.join(ALREADY_EXISTS_DIRNAME, ALREADY_EXISTS_DIRNAME),
                    os.path.join(ALREADY_EXISTS_DIRNAME, ALREADY_EXISTS_FILE_RELPATH),
                    os.path.join(ALREADY_EXISTS_DIRNAME, ALREADY_EXISTS_FILE_ALT_RELPATH),
                ],
                None
            ),
            (
                ALREADY_EXISTS_DIRNAME + "/*",
                "a",
                [
                    os.path.join("a", ALREADY_EXISTS_FILENAME),
                    os.path.join("a", ALREADY_EXISTS_FILENAME_ALT),
                ],
                [
                    ALREADY_EXISTS_FILE_RELPATH,
                    ALREADY_EXISTS_FILE_ALT_RELPATH,
                ],
                None
            ),
            (
                ALREADY_EXISTS_DIRNAME + "/*.txt",
                "a",
                [
                    os.path.join("a", ALREADY_EXISTS_FILENAME),
                    os.path.join("a", ALREADY_EXISTS_FILENAME_ALT),
                ],
                [
                    ALREADY_EXISTS_FILE_RELPATH,
                    ALREADY_EXISTS_FILE_ALT_RELPATH,
                ],
                None
            ),
            (
                ALREADY_EXISTS_DIRNAME,
                STARTING_EMPTY_DIRNAME,
                [
                    os.path.join(STARTING_EMPTY_DIRNAME, ALREADY_EXISTS_FILE_RELPATH),
                    os.path.join(STARTING_EMPTY_DIRNAME, ALREADY_EXISTS_FILE_ALT_RELPATH),
                ],
                [
                    ALREADY_EXISTS_FILE_RELPATH,
                    ALREADY_EXISTS_FILE_ALT_RELPATH,
                ],
                None
            ),
            (
                ALREADY_EXISTS_DIRNAME + "/*.txt",
                ALREADY_EXISTS_FILENAME,
                [],
                [],
                "File exists",
            ),
            # Fails to move ALREADY_EXISTS_FILENAME to ALREADY_EXISTS_FILE_RELPATH.
            (
                "*",
                ALREADY_EXISTS_DIRNAME,
                [
                    os.path.join(ALREADY_EXISTS_DIRNAME, STARTING_EMPTY_DIRNAME),
                    ALREADY_EXISTS_FILE_RELPATH,
                    ALREADY_EXISTS_FILE_ALT_RELPATH,
                ],
                [
                    ALREADY_EXISTS_FILENAME,
                    STARTING_EMPTY_DIRNAME,
                ],
                None,
            ),
        ]

        for i in range(len(test_cases)):
            with self.subTest(msg = f"Case {i}"):
                (source, dest, expected_paths, not_expected_paths, error_substring) = test_cases[i]

                operation = ["mv", source, dest]

                def post_check(operation, temp_dir):
                    for expected_path in expected_paths:
                        path = os.path.normpath(os.path.join(temp_dir, expected_path))
                        self.assertTrue(os.path.exists(path),
                                        f"Expected path does not exist '{path}'.")

                    for not_expected_path in not_expected_paths:
                        path = os.path.normpath(os.path.join(temp_dir, not_expected_path))
                        self.assertFalse(os.path.exists(path),
                                         f"Unexpected path exists '{path}'.")

                self._run_fileop_exec_test(operation, error_substring, post_check)

    @unittest.skipIf(sys.platform.startswith("win"), "fileops require POSIX")
    def test_fileop_exec_mkdir(self):
        test_cases = [
            ("a", None),
            ("a/b", None),
            ("a/../b", None),
            (ALREADY_EXISTS_DIRNAME, None),
            (ALREADY_EXISTS_DIRNAME + "/a", None),
            (ALREADY_EXISTS_FILE_POSIX_RELPATH, "File exists"),
            (ALREADY_EXISTS_FILE_POSIX_RELPATH + "/a", "Not a directory"),
        ]

        for i in range(len(test_cases)):
            with self.subTest(msg = f"Case {i}"):
                (path, error_substring) = test_cases[i]

                operation = ["mkdir", path]

                def post_check(operation, temp_dir):
                    expected_path = os.path.normpath(os.path.join(temp_dir, path))

                    self.assertTrue(os.path.isdir(expected_path),
                        f"Target does not exist or is not a dir '{expected_path}'.")

                self._run_fileop_exec_test(operation, error_substring, post_check)

    @unittest.skipIf(sys.platform.startswith("win"), "fileops require POSIX")
    def test_fileop_exec_remove(self):
        test_cases = [
            ("a", None, None),
            ("a/b", None, None),
            ("a/../b", None, None),
            (ALREADY_EXISTS_DIRNAME, None, None),
            (ALREADY_EXISTS_DIRNAME + "/a", None, None),
            (ALREADY_EXISTS_FILE_POSIX_RELPATH, None, None),
            (
                ALREADY_EXISTS_DIRNAME + "/*",
                [
                    ALREADY_EXISTS_FILE_RELPATH,
                    ALREADY_EXISTS_FILE_ALT_RELPATH
                ],
                None
            ),
            (
                ALREADY_EXISTS_DIRNAME + "/*.txt",
                [
                    ALREADY_EXISTS_FILE_RELPATH,
                    ALREADY_EXISTS_FILE_ALT_RELPATH
                ],
                None
            ),
            (
                "*",
                [
                    ALREADY_EXISTS_FILENAME,
                    ALREADY_EXISTS_DIRNAME,
                    STARTING_EMPTY_DIRNAME,
                    ALREADY_EXISTS_FILE_RELPATH,
                    ALREADY_EXISTS_FILE_ALT_RELPATH
                ],
                None
            ),
        ]

        for i in range(len(test_cases)):
            with self.subTest(msg = f"Case {i}"):
                (path, expected_paths, error_substring) = test_cases[i]
                if (expected_paths is None):
                    expected_paths = [path]

                operation = ["rm", path]

                def post_check(operation, temp_dir):
                    for rel_expected_path in expected_paths:
                        expected_path = os.path.normpath(os.path.join(temp_dir, rel_expected_path))

                        self.assertFalse(os.path.exists(expected_path),
                            f"Target exists '{expected_path}'.")

                self._run_fileop_exec_test(operation, error_substring, post_check)

    def _run_fileop_exec_test(self, operation, error_substring, post_exec):
        temp_dir = autograder.util.dir.get_temp_dir(prefix = "ag-py-testing-fileop-execute-")

        # Make some existing entries.
        autograder.util.dir.mkdir(os.path.join(temp_dir, ALREADY_EXISTS_DIRNAME))
        autograder.util.file.write(os.path.join(temp_dir, ALREADY_EXISTS_FILE_RELPATH), "AAA")
        autograder.util.file.write(os.path.join(temp_dir, ALREADY_EXISTS_FILE_ALT_RELPATH), "BBB")
        autograder.util.file.write(os.path.join(temp_dir, ALREADY_EXISTS_FILENAME), "CCC")
        autograder.util.dir.mkdir(os.path.join(temp_dir, STARTING_EMPTY_DIRNAME))

        try:
            autograder.fileop.execute(operation, temp_dir)
        except Exception as ex:
            if (error_substring is None):
                self.fail(f"Unexpected error: '{str(ex)}'.")

            self.assertIn(error_substring, str(ex), 'Error is not as expected.')
            return

        if (error_substring is not None):
            self.fail(f"Did not get expected error: '{error_substring}'.")

        post_exec(operation, temp_dir)
