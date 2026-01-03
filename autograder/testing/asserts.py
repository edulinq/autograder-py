import os
import re
import typing

import edq.testing.unittest
import edq.util.json

THIS_DIR: str = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
ROOT_DIR: str = os.path.join(THIS_DIR, '..', '..')
AUTOGRADER_TESTDATA_REPO: str = os.path.join(ROOT_DIR, 'testdata', 'autograder-testdata')
AUTOGRADER_SERVER_REPO: str = os.path.join(AUTOGRADER_TESTDATA_REPO, 'autograder-server')
API_DESCRIPTION_PATH: str = os.path.join(AUTOGRADER_SERVER_REPO, 'resources', 'api.json')

TEST_BASE_VERSION: str = '1.2.3'
TEST_GIT_HASH: str = 'abcd1234'
TEST_IS_DIRTY: bool = False

TOKEN_CLEARTEXT_PATTERN: str = r'\w{32}'
TOKEN_ID_PATTERN: str = r'\w{8}-\w{4}-\w{4}-\w{4}-\w{12}'

TEST_TOKEN_CLEARTEXT: str = 'test-token-cleartext'
TEST_TOKEN_ID: str = 'test-token-id'

_cached_api_description: typing.Union[typing.Dict[str, typing.Any], None] = None  # pylint: disable=invalid-name

def get_expected_api_description() -> typing.Dict[str, typing.Any]:
    """ Get the expected API description from the submodule (or the cache). """

    global _cached_api_description  # pylint: disable=global-statement

    if (_cached_api_description is not None):
        return _cached_api_description

    _cached_api_description = edq.util.json.load_path(API_DESCRIPTION_PATH, strict = True)

    return _cached_api_description

def content_equals_noramlize_json(test: edq.testing.unittest.BaseTest, expected: str, actual: str) -> None:
    """
    A CLI test assertion function for JSON output.
    The output will be converted to a dict and then compared with edq.testing.unittest.BaseTest.assertJSONDictEqual().
    """

    # Convert both to dicts.
    expected_dict = edq.util.json.loads(expected, strict = True)
    actual_dict = edq.util.json.loads(actual, strict = True)

    # Normalize the actual data (the expected should already be normalized (by the tester)).
    actual_dict = normalize_dict(actual_dict)

    test.assertJSONDictEqual(expected_dict, actual_dict)

def normalize_dict(data: typing.Dict[str, typing.Any]) -> typing.Dict[str, typing.Any]:
    """ Noramlize a dict that typically comes from testing output. """

    data = _noramlize_version(data)
    data = _noramlize_tokens(data)

    return data

def _noramlize_version(data: typing.Dict[str, typing.Any]) -> typing.Dict[str, typing.Any]:
    """ Normalize server version information. """

    if ('server-version' not in data):
        return data

    data['server-version']['base-version'] = TEST_BASE_VERSION
    data['server-version']['git-hash'] = TEST_GIT_HASH
    data['server-version']['is-dirty'] = TEST_IS_DIRTY

    return data

def _noramlize_tokens(data: typing.Dict[str, typing.Any]) -> typing.Dict[str, typing.Any]:
    """ Normalize token identifiers. """

    if ('token-id' in data):
        data['token-id'] = TEST_TOKEN_ID

    if ('token-cleartext' in data):
        data['token-cleartext'] = TEST_TOKEN_CLEARTEXT

    return data

def equals_api_description(test: edq.testing.unittest.BaseTest, expected: str, actual: str) -> None:
    """ A CLI test assertion function for the API description (read from a submodule). """

    expected_dict = get_expected_api_description()
    actual_dict = edq.util.json.loads(actual, strict = True)

    test.assertJSONDictEqual(expected_dict, actual_dict)

def equals_clean_tokens(test: edq.testing.unittest.BaseTest, expected: str, actual: str) -> None:
    """ A CLI test assertion function for text that contains tokens. """

    expected = re.sub(TOKEN_CLEARTEXT_PATTERN, TEST_TOKEN_CLEARTEXT, expected)
    expected = re.sub(TOKEN_ID_PATTERN, TEST_TOKEN_ID, expected)

    actual = re.sub(TOKEN_CLEARTEXT_PATTERN, TEST_TOKEN_CLEARTEXT, actual)
    actual = re.sub(TOKEN_ID_PATTERN, TEST_TOKEN_ID, actual)

    test.assertEqual(expected, actual)
