import typing

import autograder.api.config
import autograder.api.metadata.heartbeat
import autograder.testing.model
import autograder.testing.server

TEST_BASE_VERSION: str = '1.2.3'
TEST_GIT_HASH: str = 'abcd1234'
TEST_IS_DIRTY: bool = False

class TestHeartbeat(autograder.testing.server.ServerTest):
    def test_base(self):
        # [(config (and overrides), kwargs, expected, error substring), ...]
        test_cases = [
            (
                {},
                {},
                {
                    'server-version': {
                        'base-version': TEST_BASE_VERSION,
                        'git-hash': TEST_GIT_HASH,
                        'is-dirty': TEST_IS_DIRTY,
                    },
                },
                None,
            ),
        ]

        self.base_api_test(autograder.api.metadata.heartbeat.send, test_cases, actual_clean_func = _clean_func)

def _clean_func(actual: typing.Dict[str, typing.Any]) -> typing.Dict[str, typing.Any]:
    """ Clean the heartbeat response to make consistent comparisons. """

    actual['server-version']['base-version'] = TEST_BASE_VERSION
    actual['server-version']['git-hash'] = TEST_GIT_HASH
    actual['server-version']['is-dirty'] = TEST_IS_DIRTY

    return actual
