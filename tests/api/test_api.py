import glob
import json
import importlib
import os

import tests.server.base

THIS_DIR = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
DATA_DIR = os.path.join(THIS_DIR, "testdata")

REWRITE_TOKEN_ID = '<TOKEN_ID>'
REWRITE_TOKEN_CLEARTEXT = '<TOKEN_CLEARTEXT>'

class APITest(tests.server.base.ServerBaseTest):
    """
    Test API calls by mocking a server.

    Note that the same test output is used by the server to respond to a request
    and the test to verify the output (making the equality assertion seem redundant).
    However, the autograder server will verify that the output is correct in it's own test suite.
    """

    def _get_test_info(self, path):
        with open(path, 'r') as file:
            data = json.load(file)

        import_module_name = data.get('module', None)
        if (import_module_name is None):
            parts = data['endpoint'].split('/')
            prefix = parts[0]
            suffix = ''.join(parts[1:])

            import_module_name = '.'.join(['autograder', 'api', prefix, suffix])

        arguments = self.get_base_arguments()
        for key, value in data.get('arguments', {}).items():
            arguments[key] = value

        is_error = data.get('error', False)

        output_modifier = clean_output_noop
        if ('output-modifier' in data):
            modifier_name = data['output-modifier']

            if (modifier_name not in globals()):
                raise ValueError("Could not find API output modifier function: '%s'." % (
                    modifier_name))

            output_modifier = globals()[modifier_name]

        return import_module_name, arguments, data['output'], is_error, output_modifier

def _discover_api_tests():
    for path in sorted(glob.glob(os.path.join(DATA_DIR, "**", "*.json"), recursive = True)):
        try:
            _add_api_test(path)
        except Exception as ex:
            raise ValueError("Failed to parse test case '%s'." % (path)) from ex

def _add_api_test(path):
    test_name = os.path.splitext(os.path.basename(path))[0]
    setattr(APITest, 'test_' + test_name, _get_api_test_method(path))

def _get_api_test_method(path):
    def __method(self):
        module_name, arguments, expected, is_error, output_modifier = self._get_test_info(path)

        api_module = importlib.import_module(module_name)

        try:
            actual = api_module.send(arguments)
        except Exception as ex:
            if (not is_error):
                raise ex

            python_message = expected.get('python-message', "")
            self.assertEqual(python_message, str(ex))

            code = expected.get('code', None)
            self.assertEqual(code, ex.code)

            return

        if (is_error):
            self.fail("Test case does not raise an error when one was expected: '%s'." % (path))
            return

        actual = output_modifier(actual)

        self.assertDictEqual(actual, expected)

    return __method

def clean_output_noop(output):
    return output

def clean_token(output):
    output['token-id'] = REWRITE_TOKEN_ID
    output['token-cleartext'] = REWRITE_TOKEN_CLEARTEXT

    return output

def clean_output_logs(output):
    record_set_values = {
        'unix-time': 0,
    }

    attribute_set_values = {
        'path': '/some/path/course.json'
    }

    if (output.get('results') is None):
        return output

    for record in output['results']:
        for (key, value) in record_set_values.items():
            record[key] = value

        if ('attributes' not in record):
            continue

        for (key, value) in attribute_set_values.items():
            record['attributes'][key] = value

    return output

_discover_api_tests()
