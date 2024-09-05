import contextlib
import glob
import importlib
import json
import io
import os
import re
import sys

import tests.server.base
import tests.server.server
import autograder.api.error
import autograder.util.dirent

THIS_DIR = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
TEST_CASES_DIR = os.path.join(THIS_DIR, "testdata")
DATA_DIR = os.path.join(THIS_DIR, "data")

TEST_CASE_SEP = '---'
DATA_DIR_ID = '__DATA_DIR__'
TEMP_DIR_ID = '__TEMP_DIR__'

DEFAULT_OUTPUT_CHECK = 'content_equals'

TIME_REGEX = r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}'
TIME_REPLACEMENT = '<TIME>'

class CLITest(tests.server.base.ServerBaseTest):
    """
    Test CLI tools.
    """

    _base_temp_dir = autograder.util.dirent.get_temp_path('autograder_CLITest_')

    def _get_test_info(self, test_name, path):
        options, expected_output = _read_test_file(path)

        temp_dir = os.path.join(CLITest._base_temp_dir, test_name)

        module_name = options['cli']
        exit_status = options.get('exit-status', 0)
        is_error = options.get('error', False)

        output_check_name = options.get('output_check', DEFAULT_OUTPUT_CHECK)
        if (output_check_name not in globals()):
            raise ValueError("Could not find output check function: '%s'." % (output_check_name))
        output_check = globals()[output_check_name]

        if (is_error):
            expected_output = expected_output.strip()

        cli_arguments = self._build_arguments(options)

        # Make any substitutions.
        expected_output = _prepare_string(expected_output, temp_dir)
        for i in range(len(cli_arguments)):
            cli_arguments[i] = _prepare_string(cli_arguments[i], temp_dir)

        return module_name, cli_arguments, expected_output, output_check, exit_status, is_error

    def _build_arguments(self, options):
        # Start with the base arguments
        # (note that later arguments override earlier ones).
        base_arguments = self.get_base_arguments()

        # Remove any base arguments that are not allowed by the parser
        # (e.g. a course where one is not expected).
        allowed_arg_keys = set(self._load_allowed_arg_keys(options['cli']))
        for base_arg_key in list(base_arguments.keys()):
            if (('--' + base_arg_key) not in allowed_arg_keys):
                del base_arguments[base_arg_key]

        # Process overrides.
        for key, value in options.get('overrides', {}).items():
            base_arguments[key] = value

        cli_arguments = []
        for key, value in base_arguments.items():
            cli_arguments += ["--%s" % (str(key)), str(value)]

        cli_arguments += options.get('arguments', [])

        return cli_arguments

    def _load_allowed_arg_keys(self, module_name):
        # argparse will look (without checks) for argv when constructing a parser (which is dumb).
        clear_argv = False
        if (len(sys.argv) == 0):
            clear_argv = True
            sys.argv.append('autograder_cli_test')

        module = importlib.import_module(module_name)

        keys = []
        for action in module._get_parser()._actions:
            keys += action.option_strings

        if (clear_argv):
            sys.argv.clear()

        return keys

def _prepare_string(text, temp_dir):
    replacements = [
        (DATA_DIR_ID, DATA_DIR),
        (TEMP_DIR_ID, temp_dir),
    ]

    for (key, base_dir) in replacements:
        text = _replace_path(text, key, base_dir)

    return text

def _replace_path(text, key, base_dir):
    match = re.search(r'%s\(([^)]*)\)' % (key), text)
    if (match is not None):
        filename = match.group(1)

        # Normalize any path separators.
        filename = os.path.join(*filename.split('/'))

        if (filename == ''):
            path = base_dir
        else:
            path = os.path.join(base_dir, filename)

        text = text.replace(match.group(0), path)

    return text

def _read_test_file(path):
    json_lines = []
    output_lines = []

    with open(path, 'r') as file:
        accumulator = json_lines
        for line in file:
            if (line.strip() == TEST_CASE_SEP):
                accumulator = output_lines
                continue

            accumulator.append(line)

    options = json.loads(''.join(json_lines))
    output = ''.join(output_lines)

    return options, output

def _discover_test_cases():
    for path in sorted(glob.glob(os.path.join(TEST_CASES_DIR, "**", "*.txt"), recursive = True)):
        try:
            _add_test_case(path)
        except Exception as ex:
            raise ValueError("Failed to parse test case '%s'." % (path)) from ex

def _add_test_case(path):
    test_name = 'test_cli__' + os.path.splitext(os.path.basename(path))[0]
    setattr(CLITest, test_name, _get_test_method(test_name, path))

def _get_test_method(test_name, path):
    def __method(self):
        (module_name, cli_arguments, expected_output, output_check,
            expected_exit_status, is_error) = self._get_test_info(test_name, path)
        module = importlib.import_module(module_name)

        old_args = sys.argv
        sys.argv = [module.__file__] + cli_arguments

        try:
            with contextlib.redirect_stdout(io.StringIO()) as output:
                actual_exit_status = module.main()
            actual_output = output.getvalue()

            if (is_error):
                self.fail("No error was not raised when one was expected ('%s')." % (
                    str(expected_output)))
        except autograder.api.error.ConnectionError:
            # Catch errors where the server does not responsed and suppress large connection errors.
            try:
                self.fail("Server had an error. See earlier output from the server.")
            except AssertionError as ex:
                ex.__suppress_context__ = True
                ex.__cause__ = None
                ex.__context__ = None
                raise ex

        except BaseException as ex:
            if (not is_error):
                raise ex

            if (isinstance(ex, SystemExit)):
                if (ex.__context__ is None):
                    self.fail("Unexpected exit without context.")

                ex = ex.__context__

            self.assertEqual(expected_output, str(ex), msg = "error output")
        finally:
            sys.argv = old_args

        self.assertEqual(expected_exit_status, actual_exit_status, msg = "exit status")

        output_check(self, expected_output, actual_output)

    return __method

def content_equals(test_case, expected, actual, **kwargs):
    test_case.assertEqual(expected, actual)

def has_content_100(test_case, expected, actual, **kwargs):
    return has_content(test_case, expected, actual, min_length = 100)

def content_equals_ignore_time(test_case, expected, actual, **kwargs):
    """
    Replace anything that looks like a time.
    """

    expected = re.sub(TIME_REGEX, TIME_REPLACEMENT, expected)
    actual = re.sub(TIME_REGEX, TIME_REPLACEMENT, actual)

    content_equals(test_case, expected, actual)

def json_logs_equal(test_case, expected, actual, **kwargs):
    """
    A special function for JSON logs that understands the log fields.
    """

    expected = json.loads(expected)
    actual = json.loads(actual)

    for records in [expected, actual]:
        for record in records:
            record['unix-time'] = -1

    test_case.assertListEqual(expected, actual)

# Ensure that the output has content.
def has_content(test_case, expected, actual, min_length = 100):
    message = "Output does not meet minimum length of %d, it is only %d." % (
        min_length, len(actual))
    test_case.assertTrue((len(actual) >= min_length), msg = message)

_discover_test_cases()
