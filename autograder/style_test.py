import os

import edq.testing.unittest
import edq.util.dirent

import autograder.style

THIS_PATH = os.path.realpath(__file__)

class TestStyle(edq.testing.unittest.BaseTest):
    def test_style_override(self):
        temp_dir = edq.util.dirent.get_temp_dir('autograder-test-style-')

        # Make a copy of this file.
        path = os.path.join(temp_dir, 'test.py')
        edq.util.dirent.copy(THIS_PATH, path)

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
