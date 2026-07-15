import typing

import edq.util.crypto

import autograder.api.config
import autograder.api.courses.assignments.images.info
import autograder.model.config
import autograder.testing.constants
import autograder.testing.server

class TestCourseAssignmentsImagesInfo(autograder.testing.server.ServerTest):
    """ Test getting info on assignment images. """

    def test_base(self) -> None:
        """ Test base functionality. """

        # pylint: disable=line-too-long
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
                    assignment = 'hw0',
                ),
                {},
                {
                    "image-info": {
                        "built": True,
                        "created-timestamp": autograder.testing.constants.TEST_TIMESTAMP,
                        "name": "autograder.course101.hw0",
                        "size-bytes": len(autograder.testing.constants.TEST_PAYLOAD_BYTES),
                        "source-info": {
                            "image": "ghcr.io/edulinq/grader.python:0.1.1.0-alpine",
                            "max-runtime-secs": 300,
                            "static-files": [
                                {
                                    "path": "grader.py",
                                    "type": "path"
                                }
                            ]
                        },
                    }
                },
                None,
            ),
        ]

        self.base_api_test(autograder.api.courses.assignments.images.info.send, test_cases, actual_clean_func = _clean_response)

def _clean_response(response: typing.Dict[str, typing.Any]) -> typing.Any:
    """ Normalize the image bytes. """

    # Set the bytes to a constant.

    response['image-info']['created-timestamp'] = autograder.testing.constants.TEST_TIMESTAMP
    response['image-info']['size-bytes'] = len(autograder.testing.constants.TEST_PAYLOAD_BYTES)

    return response
