import typing

import edq.testing.unittest
import edq.util.json

TEST_BASE_VERSION: str = '1.2.3'
TEST_GIT_HASH: str = 'abcd1234'
TEST_IS_DIRTY: bool = False

def content_equals_noramlize_json(test: edq.testing.unittest.BaseTest, expected: str, actual: str) -> None:
    """
    A CLI test assertion function for JSON output.
    The output will be converted to a dict and then compared with edq.testing.unittest.BaseTest.assertJSONDictEqual().
    """

    # Convert both to dicts.
    expected_dict = edq.util.json.loads(expected)
    actual_dict = edq.util.json.loads(actual)

    # Normalize the actual data (the expected should already be normalized (by the tester)).
    actual_dict = normalize_dict(actual_dict)

    test.assertJSONDictEqual(expected_dict, actual_dict)

def normalize_dict(data: typing.Dict[str, typing.Any]) -> typing.Dict[str, typing.Any]:
    """ Noramlize a dict that typically comes from testing output. """

    data = _noramlize_version(data)

    return data

def _noramlize_version(data: typing.Dict[str, typing.Any]) -> typing.Dict[str, typing.Any]:
    """ Normalize server version information. """

    if ('server-version' not in data):
        return data

    data['server-version']['base-version'] = TEST_BASE_VERSION
    data['server-version']['git-hash'] = TEST_GIT_HASH
    data['server-version']['is-dirty'] = TEST_IS_DIRTY

    return data
