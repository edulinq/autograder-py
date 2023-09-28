import unittest

import autograder.utils

class TestDate(unittest.TestCase):
    def test_timestamp_conversions(self):
        cases = [
            ('2023-09-28', '2023-09-28T00:00:00'),
            ('2023-09-28T00:00:00', '2023-09-28T00:00:00'),
            ('2023-09-28T04:00:20.683684Z', '2023-09-28T04:00:20+00:00'),
            ('2023-09-28T04:00:20.683684+00:00', '2023-09-28T04:00:20+00:00'),
            ('2023-09-28T13:10:44.432050+00:00', '2023-09-28T13:10:44+00:00'),
            ('2023-09-28T13:10:44.43205+00:00', '2023-09-28T13:10:44+00:00'),
        ]

        for (source, expected_string) in cases:
            first_timestamp = autograder.utils.get_timestamp(source)
            string = autograder.utils.timestamp_to_string(first_timestamp)
            second_timestamp = autograder.utils.get_timestamp(string)

            if (expected_string is not None):
                self.assertEquals(string, expected_string)

            self.assertEquals(first_timestamp, second_timestamp)
