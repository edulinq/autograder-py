import autograder.api.config
import autograder.api.courses.admin.email
import autograder.testing.server

class TestCoursesAdminEmail(autograder.testing.server.ServerTest):
    """ Test emailing course users. """

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

                    autograder.api.config.PARAM_DRY_RUN.config_key: True,
                    autograder.api.config.PARAM_EMAIL_HTML.config_key: False,

                    autograder.api.config.PARAM_EMAIL_COURSE_TO.config_key: [
                        '*',
                    ],
                    autograder.api.config.PARAM_EMAIL_SUBJECT.config_key: 'Test Subject',
                },
                {},
                {
                    "bcc": [],
                    "cc": [],
                    "to": [
                        "course-admin@test.edulinq.org",
                        "course-grader@test.edulinq.org",
                        "course-other@test.edulinq.org",
                        "course-owner@test.edulinq.org",
                        "course-student@test.edulinq.org"
                    ]
                },
                None,
            ),

        ]

        self.base_api_test(autograder.api.courses.admin.email.send, test_cases)
