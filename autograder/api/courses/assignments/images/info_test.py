import typing

import autograder.api.config
import autograder.api.courses.assignments.images.info
import autograder.testing.constants
import autograder.testing.server

class TestCourseAssignmentsImagesInfo(autograder.testing.server.ServerTest):
    """ Test getting info on assignment images. """

    def test_base(self):
        """ Test base functionality. """

        # pylint: disable=line-too-long
        # [(config (and overrides), kwargs, expected, error substring), ...]
        test_cases = [
            # Base
            (
                {
                    autograder.api.config.PARAM_USER_EMAIL.config_key: 'server-admin@test.edulinq.org',
                    autograder.api.config.PARAM_USER_PASS.config_key: 'server-admin',
                    autograder.api.config.PARAM_COURSE.config_key: 'course101',
                    autograder.api.config.PARAM_ASSIGNMENT.config_key: 'hw0',
                },
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
