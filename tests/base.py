import json
import unittest

FORMAT_STR = "\n--- Expected ---\n%s\n--- Actual ---\n%s\n---\n"

class BaseTest(unittest.TestCase):
    """
    A base class for tests.
    """

    maxDiff = None

    def assertListEqual(self, a, b):
        a_json = json.dumps(a, indent = 4)
        b_json = json.dumps(b, indent = 4)

        super().assertListEqual(a, b, FORMAT_STR % (a_json, b_json))

    def assertDictEqual(self, a, b):
        a_json = json.dumps(a, indent = 4)
        b_json = json.dumps(b, indent = 4)

        super().assertDictEqual(a, b, FORMAT_STR % (a_json, b_json))
