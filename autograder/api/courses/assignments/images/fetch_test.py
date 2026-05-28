import typing

import autograder.api.config
import autograder.api.courses.assignments.images.fetch
import autograder.testing.constants
import autograder.testing.server

class TestCourseAssignmentsImagesFetch(autograder.testing.server.ServerTest):
    """ Test fetching assignment images. """

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
                    "bytes": autograder.testing.constants.TEST_PAYLOAD_B64_GZIP_BYTES,
                    "gzip": True,
                    "image-info": {
                        "built": True,
                        "created-timestamp": autograder.testing.constants.TEST_TIMESTAMP,
                        "gzip-size-bytes": len(autograder.testing.constants.TEST_PAYLOAD_GZIP_BYTES),
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

        self.base_api_test(autograder.api.courses.assignments.images.fetch.send, test_cases, actual_clean_func = _clean_response)

def _clean_response(response: typing.Dict[str, typing.Any]) -> typing.Any:
    """ Normalize the image bytes. """

    # Set the bytes to a constant.

    response['bytes'] = autograder.testing.constants.TEST_PAYLOAD_B64_GZIP_BYTES
    response['image-info']['created-timestamp'] = autograder.testing.constants.TEST_TIMESTAMP
    response['image-info']['gzip-size-bytes'] = len(autograder.testing.constants.TEST_PAYLOAD_GZIP_BYTES)
    response['image-info']['size-bytes'] = len(autograder.testing.constants.TEST_PAYLOAD_BYTES)

    return response
