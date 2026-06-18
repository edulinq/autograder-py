import autograder.api.config
import autograder.api.metadata.heartbeat
import autograder.testing.asserts
import autograder.testing.model
import autograder.testing.server

class TestHeartbeat(autograder.testing.server.ServerTest):
    """ Test getting a heartbeat. """

    def test_base(self) -> None:
        """ Test base functionality. """

        # [(config (and overrides), kwargs, expected, error substring), ...]
        test_cases: typing.List[typing.Tuple[
            autograder.model.config.Config,
            typing.Dict[str, typing.Any],
            typing.Any,
            typing.Union[str, None],
        ]] = [
            (
                autograder.model.config.Config(
                    auth_user = 'course-owner@test.edulinq.org',
                    auth_pass = 'course-owner',
                ),
                {},
                {
                    'server-version': {
                        'base-version': autograder.testing.constants.TEST_BASE_VERSION,
                        'git-hash': autograder.testing.constants.TEST_GIT_HASH,
                        'is-dirty': autograder.testing.constants.TEST_IS_DIRTY,
                    },
                },
                None,
            ),
        ]

        self.base_api_test(autograder.api.metadata.heartbeat.send, test_cases, actual_clean_func = autograder.testing.asserts.normalize_dict)
