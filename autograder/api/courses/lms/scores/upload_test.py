import typing

import edq.util.crypto

import autograder.api.config
import autograder.api.courses.lms.scores.upload
import autograder.model.config
import autograder.testing.server

class TestCoursesLMSScoresUpload(autograder.testing.server.ServerTest):
    """ Test uploading scores to the LMS. """

    def test_base(self) -> None:
        """ Test base functionality. """

        # [(config (and overrides), kwargs, expected, error substring), ...]
        test_cases: typing.List[typing.Tuple[
            autograder.model.config.Config,
            typing.Dict[str, typing.Any],
            typing.Any,
            typing.Union[str, None],
        ]] = [
            # Base
            (
                autograder.model.config.Config(
                    auth_user = 'server-admin@test.edulinq.org',
                    auth_pass = edq.util.crypto.Secret('server-admin'),

                    course = 'course101',

                    dry_run = False,
                ),
                {},
                {
                    "dry-run": False,
                    "results": []
                },
                None,
            ),

        ]

        self.base_api_test(autograder.api.courses.lms.scores.upload.send, test_cases)
