import os
import re
import sys

import edq.testing.unittest
import edq.util.dirent

import autograder.style

THIS_DIR: str = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
ROOT_DIR: str = os.path.join(THIS_DIR, '..')
TESTDATA_DIR: str = os.path.join(THIS_DIR, 'testdata', 'code')

class TestStyle(edq.testing.unittest.BaseTest):
    """ Test getting style issues for source code. """

    def test_check_paths_base(self):
        """ Test the base functionality of checking paths. """

        # Create a file with a style violation.
        temp_dir = edq.util.dirent.get_temp_dir('autograder-test-style-')
        bad_style_path = os.path.abspath(os.path.join(temp_dir, 'test.py'))
        contents = edq.util.dirent.read_file(os.path.join(TESTDATA_DIR, 'base.py'))
        long_line = 'test = "' + ('Z' * (autograder.style.DEFAULT_MAX_LINE_LENGTH)) + '"'
        contents += (os.linesep + long_line)
        edq.util.dirent.write_file(bad_style_path, contents)

        # Windows line is off by one.
        bad_style_lineno = 12
        if (sys.platform.startswith("win")):
            bad_style_lineno += 1

        # Testing paths.
        path_base_py = os.path.join(TESTDATA_DIR, 'base.py')
        path_base_ipynb = os.path.join(TESTDATA_DIR, 'base.ipynb')
        path_run_scripts = os.path.join(ROOT_DIR, 'scripts', 'run_tests.sh')

        # pylint: disable=line-too-long
        # [(paths, kwargs, expected count, expected lines, error substring), ...]
        test_cases = [
            # Base
            (
                [
                    path_base_py,
                ],
                {},
                0,
                [
                    (
                        path_base_py,
                        [],
                    )
                ],
                None,
            ),

            # Notebook
            (
                [
                    path_base_ipynb,
                ],
                {},
                0,
                [
                    (
                        path_base_ipynb,
                        [],
                    )
                ],
                None,
            ),

            # Non-Python
            (
                [
                    path_run_scripts,
                ],
                {},
                0,
                [
                ],
                None,
            ),

            # Multiple Paths
            (
                [
                    path_base_py,
                    path_base_ipynb,
                ],
                {},
                0,
                [
                    (
                        path_base_ipynb,
                        [],
                    ),
                    (
                        path_base_py,
                        [],
                    ),
                ],
                None,
            ),

            # Dir
            (
                [
                    TESTDATA_DIR,
                ],
                {},
                0,
                [
                    (
                        os.path.join(TESTDATA_DIR, 'base.ipynb'),
                        [],
                    ),
                    (
                        os.path.join(TESTDATA_DIR, 'base.py'),
                        [],
                    ),
                    (
                        os.path.join(TESTDATA_DIR, 'base_with_raise.ipynb'),
                        [],
                    ),
                    (
                        os.path.join(TESTDATA_DIR, 'base_with_raise.py'),
                        [],
                    ),
                    (
                        os.path.join(TESTDATA_DIR, 'simple.ipynb'),
                        [],
                    ),
                    (
                        os.path.join(TESTDATA_DIR, 'simple.py'),
                        [],
                    ),
                ],
                None,
            ),

            # Ignore Patterns
            (
                [
                    TESTDATA_DIR,
                ],
                {
                    'ignore_patterns': [
                        r'\.ipynb$',
                        re.compile(r'_with_raise'),
                    ],
                },
                0,
                [
                    (
                        os.path.join(TESTDATA_DIR, 'base.py'),
                        [],
                    ),
                    (
                        os.path.join(TESTDATA_DIR, 'simple.py'),
                        [],
                    ),
                ],
                None,
            ),

            # Style Error
            (
                [
                    bad_style_path,
                ],
                {},
                1,
                [
                    (
                        bad_style_path,
                        [
                            f"{bad_style_path}:{bad_style_lineno}:151: E501 line too long (159 > 150 characters)",
                            "test = \"ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ\"",
                            "                                                                                                                                                      ^",
                        ]
                    )
                ],
                None,
            ),
        ]

        for (i, test_case) in enumerate(test_cases):
            (paths, kwargs, expected_count, expected_lines, error_substring) = test_case

            with self.subTest(msg = f"Case {i} ({paths}):"):
                try:
                    actual_count, actual_lines = autograder.style.check_paths(paths, include_clean_paths = True, **kwargs)
                except Exception as ex:
                    error_string = self.format_error_string(ex)
                    if (error_substring is None):
                        self.fail(f"Unexpected error: '{error_string}'.")

                    self.assertIn(error_substring, error_string, 'Error is not as expected.')

                    continue

                if (error_substring is not None):
                    self.fail(f"Did not get expected error: '{error_substring}'.")

                self.assertEqual(expected_count, actual_count)
                self.assertJSONListEqual(expected_lines, actual_lines)

    def test_style_override(self):
        """ Test overriding default functionality. """

        temp_dir = edq.util.dirent.get_temp_dir('autograder-test-style-')
        test_path = os.path.join(TESTDATA_DIR, 'base.py')

        # Make a copy of this file.
        path = os.path.join(temp_dir, 'test.py')
        edq.util.dirent.copy(test_path, path)

        # The style should be clean to start with.
        count, _ = autograder.style.check_file(path)
        self.assertEqual(count, 0, 'Initial style should be clean.')

        # Add in a style violation (a long line).
        contents = edq.util.dirent.read_file(path)
        long_line = 'test = "' + ('Z' * (autograder.style.DEFAULT_MAX_LINE_LENGTH)) + '"'
        contents += (os.linesep + long_line)
        edq.util.dirent.write_file(path, contents)

        # There should now be exactly one violation.
        count, _ = autograder.style.check_file(path)
        self.assertEqual(count, 1, 'Expected exactly one violation.')

        # Override the long line length, now there should be no violations.
        style_overrides = {'max_line_length': 100000}
        count, _ = autograder.style.check_file(path, style_overrides = style_overrides)
        self.assertEqual(count, 0, 'Final style should be clean.')
