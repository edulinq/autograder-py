import os
import typing

import edq.testing.cli
import edq.testing.httpserver
import lms.model.base

import autograder.api.common

THIS_DIR: str = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
ROOT_DIR: str = os.path.join(THIS_DIR, '..', '..')
EXCHANGES_DIR: str = os.path.join(ROOT_DIR, 'testdata', 'autograder-testdata')

CLI_TESTDATA_DIR: str = os.path.join(ROOT_DIR, 'autograder', 'cli', 'testdata')
CLI_TESTS_DIR: str = os.path.join(CLI_TESTDATA_DIR, 'tests')
CLI_DATA_DIR: str = os.path.join(CLI_TESTDATA_DIR, 'data')
CLI_GLOBAL_CONFG_PATH: str = os.path.join(CLI_DATA_DIR, 'testing-autograder.json')

BASE_ARGUMENTS: typing.Dict[str, typing.Any] = {
    'user': 'course-owner@test.edulinq.org',
    'pass': 'course-owner',

    # Will be set with the correct port when the test is run.
    'server': None,
}

class ServerTest(edq.testing.httpserver.HTTPServerTest):
    """
    A special test suite that is common across all tests that require a test autograder server.
    """

    def __init__(self, *args: typing.Any, **kwargs: typing.Any) -> None:
        super().__init__(*args, **kwargs)

    @classmethod
    def child_class_setup(cls):
        # Make the API request source information consistent.
        autograder.api.common.set_testing_source_info()

    @classmethod
    def setup_server(cls, server: edq.testing.httpserver.HTTPTestServer) -> None:
        edq.testing.httpserver.HTTPServerTest.setup_server(server)
        server.load_exchanges_dir(EXCHANGES_DIR)

    def modify_cli_test_info(self, test_info: edq.testing.cli.CLITestInfo) -> None:
        """ Adjust the CLI test info to include core info (like server information). """

        test_info.arguments += [
            '--config-global', CLI_GLOBAL_CONFG_PATH,
            '--server', self.get_server_url(),
        ]

    def base_api_test(self,
            api_function: typing.Callable,
            test_cases: typing.List[typing.Tuple[typing.Dict[str, typing.Any], typing.Dict[str, typing.Any], typing.Any, typing.Union[str, None]]],
            actual_clean_func: typing.Union[typing.Callable, None] = None,
            expected_clean_func: typing.Union[typing.Callable, None] = None,
            assertion_func: typing.Union[typing.Callable, None] = None,
            ) -> None:
        """
        A common test for the base API functionality.
        Test cases are passed in as: `[(configs (and overrides), kwargs, expected, error substring), ...]`.
        """

        for (i, test_case) in enumerate(test_cases):
            (config, kwargs, expected, error_substring) = test_case

            with self.subTest(msg = f"Case {i}:"):
                args = BASE_ARGUMENTS.copy()
                args['server'] = self.get_server_url()
                args.update(config)

                try:
                    actual = api_function(args, **kwargs)
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

    @classmethod
    def get_test_basename(cls, path: str) -> str:
        """ Get the test's name based off of its filename and location. """

        path = os.path.abspath(path)

        name = os.path.splitext(os.path.basename(path))[0]

        ancestors = os.path.dirname(path).replace(CLI_TESTS_DIR, '')
        prefix = ancestors.replace(os.sep, '_')

        if (prefix.startswith('_')):
            prefix = prefix.replace('_', '', 1)

        if (len(prefix) > 0):
            name =  f"{prefix}_{name}"

        return name

# Attach CLI tests.
edq.testing.cli.discover_test_cases(ServerTest, CLI_TESTS_DIR, CLI_DATA_DIR)
