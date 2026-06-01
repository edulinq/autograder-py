import typing

import edq.testing.unittest

import autograder.util.math

class TestFileOp(edq.testing.unittest.BaseTest):
    """ Test file operations. """

    def test_number_to_str(self):
        """ Test formatting numbers. """

        # [(number, precision, exact precision, expected, error substring), ...]
        test_cases: typing.List[typing.Tuple[
                typing.Union[int, float],
                int,
                bool,
                str,
                typing.Union[str, None]
        ]] = [
            # Non-Exact Precision, Base
            (
                1.23,
                0,
                False,
                '1',
                None
            ),
            (
                1.23,
                1,
                False,
                '1.2',
                None
            ),
            (
                1.23,
                2,
                False,
                '1.23',
                None
            ),
            (
                1.23,
                3,
                False,
                '1.23',
                None
            ),
            (
                1.23,
                4,
                False,
                '1.23',
                None
            ),

            # Exact Precision, Base
            (
                1.23,
                0,
                True,
                '1',
                None
            ),
            (
                1.23,
                1,
                True,
                '1.2',
                None
            ),
            (
                1.23,
                2,
                True,
                '1.23',
                None
            ),
            (
                1.23,
                3,
                True,
                '1.230',
                None
            ),
            (
                1.23,
                4,
                True,
                '1.2300',
                None
            ),

            # Round
            (
                1.251,
                1,
                False,
                '1.3',
                None
            ),
            (
                1.251,
                1,
                True,
                '1.3',
                None
            ),

            # Int
            (
                1,
                2,
                False,
                '1',
                None
            ),
            (
                1.0,
                2,
                False,
                '1',
                None
            ),
            (
                1,
                2,
                True,
                '1.00',
                None
            ),
        ]

        for (i, test_case) in enumerate(test_cases):
            (number, precision, exact_precision, expected, error_substring) = test_case

            with self.subTest(msg = f"Case {i} ({number}):"):
                try:
                    actual = autograder.util.math.number_to_str(number, precision, exact_precision)
                except Exception as ex:
                    error_string = self.format_error_string(ex)
                    if (error_substring is None):
                        self.fail(f"Unexpected error: '{error_string}'.")

                    self.assertIn(error_substring, error_string, 'Error is not as expected.')

                    continue

                if (error_substring is not None):
                    self.fail(f"Did not get expected error: '{error_substring}'.")

                self.assertEqual(expected, actual)
