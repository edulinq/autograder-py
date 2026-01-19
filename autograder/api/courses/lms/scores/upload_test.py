import autograder.api.config
import autograder.api.courses.lms.scores.upload
import autograder.testing.server

class TestCoursesLMSScoresUpload(autograder.testing.server.ServerTest):
    """ Test uploading scores to the LMS. """

    def test_base(self):
        """ Test base functionality. """

        # [(config (and overrides), kwargs, expected, error substring), ...]
        test_cases = [
            # Base
            (
                {
                    autograder.api.config.PARAM_USER_EMAIL.config_key: 'server-admin@test.edulinq.org',
                    autograder.api.config.PARAM_USER_PASS.config_key: 'server-admin',

                    autograder.api.config.PARAM_COURSE.config_key: 'course101',

                    autograder.api.config.PARAM_DRY_RUN.config_key: False,
                },
                {},
                {
                    "dry-run": False,
                    "results": []
                },
                None,
            ),

        ]

        self.base_api_test(autograder.api.courses.lms.scores.upload.send, test_cases)
