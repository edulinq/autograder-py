import os
import typing

import edq.net.exchangeserver
import edq.testing.httpserver
import edq.util.serial
import lms.model.base

import autograder.api.common
import autograder.error
import autograder.model.config

THIS_DIR: str = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
ROOT_DIR: str = os.path.join(THIS_DIR, '..', '..')
EXCHANGES_DIR: str = os.path.join(ROOT_DIR, 'testdata', 'autograder-testdata')

# TEST - Remove?
BASE_ARGUMENTS: typing.Dict[str, typing.Any] = {
    # Will be set with the correct port when the test is run.
    'server': None,
}

# Exchange tests are unnecessary.
delattr(edq.testing.httpserver.HTTPServerTest, 'test_exchanges_base')

@typing.runtime_checkable
class CleanFunction(typing.Protocol):
    """ A function for cleaning a test result (expected or actual) before assertion. """

    def __call__(self, raw: typing.Any) -> typing.Any:
        """
        Clean and return data for assertion.
        """

@typing.runtime_checkable
class AssertionFunction(typing.Protocol):
    """ A function for asserting during a test. """

    def __call__(self, expected: typing.Any, actual: typing.Any) -> typing.Any:
        """
        Assert the relationship between expected and actual.
        """

class ServerTest(edq.testing.httpserver.HTTPServerTest):
    """
    A special test suite that is common across all tests that require a test autograder server.
    """

    # Use the same server for all test classes.
    tear_down_server = False

    @classmethod
    def child_class_setup(cls) -> None:
        # Make the API request source information consistent.
        autograder.api.common.set_testing_source_info()

        # Don't exit on error.
        autograder.error._exit_on_error_for_testing = False

    @classmethod
    def setup_server(cls, server: edq.net.exchangeserver.HTTPExchangeServer) -> None:
        context = edq.util.serial.SerializationContext(json_options = {
            'strict': True,
        })

        edq.testing.httpserver.HTTPServerTest.setup_server(server)
        server.load_exchanges_dir(EXCHANGES_DIR, context = context)

    def base_api_test(self,
            api_function: typing.Callable,
            test_cases: typing.List[typing.Tuple[autograder.model.config.Config, typing.Dict[str, typing.Any], typing.Any, typing.Union[str, None]]],
            actual_clean_func: typing.Union[CleanFunction, None] = None,
            expected_clean_func: typing.Union[CleanFunction, None] = None,
            assertion_func: typing.Union[AssertionFunction, None] = None,
            ) -> None:
        """
        A common test for the base API functionality.
        Test cases are passed in as: `[(configs (and overrides), kwargs, expected, error substring), ...]`.
        """

        for (i, test_case) in enumerate(test_cases):
            (config, kwargs, expected, error_substring) = test_case

            with self.subTest(msg = f"Case {i}:"):
                config.server = self.get_server_url()

                try:
                    actual = api_function(config, **kwargs)
                except Exception as ex:
                    error_string = self.format_error_string(ex)
                    if (error_substring is None):
                        self.fail(f"Unexpected error: '{error_string}'.")

                    self.assertIn(error_substring, error_string, 'Error is not as expected.')

                    continue

                if (error_substring is not None):
                    self.fail(f"Did not get expected error: '{error_substring}'.")

                if (actual_clean_func is not None):
                    actual = actual_clean_func(actual)

                if (expected_clean_func is not None):
                    expected = expected_clean_func(expected)

                # If we expect a tuple, compare the tuple contents instead of the tuple itself.
                if (isinstance(expected, tuple)):
                    if (not isinstance(actual, tuple)):
                        raise ValueError(f"Expected results to be a tuple, found '{type(actual)}'.")

                    if (len(expected) != len(actual)):
                        raise ValueError(f"Result size mismatch. Expected: {len(expected)}, Actual: {len(actual)}.")
                else:
                    # Wrap the results in a tuple.
                    expected = (expected, )
                    actual = (actual, )

                for i in range(len(expected)):  # pylint: disable=consider-using-enumerate
                    expected_value = expected[i]
                    actual_value = actual[i]

                    if (assertion_func is not None):
                        assertion_func(expected_value, actual_value)
                    elif (isinstance(expected_value, lms.model.base.BaseType)):
                        self.assertJSONEqual(expected_value, actual_value)
                    elif (isinstance(expected_value, dict)):
                        self.assertJSONDictEqual(expected_value, actual_value)
                    elif (isinstance(expected_value, list)):
                        self.assertJSONListEqual(expected_value, actual_value)
                    else:
                        self.assertEqual(expected_value, actual_value)
