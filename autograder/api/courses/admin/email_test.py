import typing

import autograder.api.config
import autograder.api.courses.admin.email
import autograder.model.config
import autograder.testing.server

class TestCoursesAdminEmail(autograder.testing.server.ServerTest):
    """ Test emailing course users. """

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
                    auth_pass = 'server-admin',
                    course = 'course101',

                    dry_run = True,
                    email_html = False,

                    to = [
                        '*',
                    ],
                    subject = 'Test Subject',
                ),
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
