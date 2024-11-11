import os
import unittest

import autograder.util.dirent
import autograder.util.gzip

THIS_DIR = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
DATA_DIR = os.path.join(THIS_DIR, "data")

class TestGzip(unittest.TestCase):
    def test_base(self):
        input_path = os.path.join(DATA_DIR, 'hw0_solution.py')
        with open(input_path, 'rb') as file:
            raw_data = file.read()

        compressed_data = autograder.util.gzip.to_base64(input_path)
        output_data = autograder.util.gzip.from_base64(compressed_data)

        self.assertEqual(raw_data, output_data, 'Decompressed data does not match raw file data.')
