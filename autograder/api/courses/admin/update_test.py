import typing

import autograder.api.config
import autograder.api.courses.admin.update
import autograder.model.config
import autograder.testing.server

class TestCoursesAdminUpdate(autograder.testing.server.ServerTest):
    """ Test update a course. """

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

                    dry_run = False,
                    skip_emails = False,
                    skip_source_sync = False,
                    skip_lms_sync = False,
                    skip_build_images = True,
                    skip_template_files = False,
                ),
                {},
                TEST_RESPONSE,
                None,
            ),
            (
                autograder.model.config.Config(
                    auth_user = 'course-admin@test.edulinq.org',
                    auth_pass = 'course-admin',
                    course = 'course101',

                    dry_run = False,
                    skip_emails = False,
                    skip_source_sync = False,
                    skip_lms_sync = False,
                    skip_build_images = True,
                    skip_template_files = False,
                ),
                {},
                TEST_RESPONSE,
                None,
            ),
        ]

        self.base_api_test(autograder.api.courses.admin.update.send, test_cases)

TEST_RESPONSE: typing.Dict[str, typing.Any] = {
    "result": {
        "assignment-template-files": {
            "hw0": [
                "submission.py"
            ]
        },
        "built-assignment-images": None,
        "course-id": "course101",
        "created": False,
        "lms-sync-result": {
            "assignment-sync": {
                "ambiguous-matches": [],
                "non-matched-assignments": [],
                "synced-assignments": [],
                "unchanged-assignments": []
            },
            "user-sync": [
                {
                    "email": "course-admin@test.edulinq.org",
                    "skipped": True
                },
                {
                    "email": "course-grader@test.edulinq.org",
                    "skipped": True
                },
                {
                    "email": "course-other@test.edulinq.org",
                    "skipped": True
                },
                {
                    "email": "course-owner@test.edulinq.org",
                    "skipped": True
                },
                {
                    "email": "course-student@test.edulinq.org",
                    "skipped": True
                }
            ]
        },
        "message": "",
        "success": True,
        "updated": True
    }
}
