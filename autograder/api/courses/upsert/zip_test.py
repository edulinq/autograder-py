import typing

import autograder.api.config
import autograder.api.courses.upsert.zip
import autograder.model.config
import autograder.testing.constants
import autograder.testing.server

class TestCoursesUpsertZip(autograder.testing.server.ServerTest):
    """ Test upserting a course with a zip. """

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

                    dry_run = False,
                    skip_emails = False,
                    skip_source_sync = False,
                    skip_lms_sync = False,
                    skip_build_images = True,
                    skip_template_files = False,
                ),
                {
                    'post_paths': [
                        autograder.testing.constants.COURSE_101_ZIP_PATH,
                    ],
                },
                {
                    "results": [
                        {
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
                    ]
                },
                None,
            ),

        ]

        self.base_api_test(autograder.api.courses.upsert.zip.send, test_cases)
