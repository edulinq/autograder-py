import autograder.api.config
import autograder.api.courses.upsert.zip
import autograder.testing.constants
import autograder.testing.server

class TestCoursesUpsertZip(autograder.testing.server.ServerTest):
    """ Test upserting a course with a zip. """

    def test_base(self):
        """ Test base functionality. """

        # [(config (and overrides), kwargs, expected, error substring), ...]
        test_cases = [
            # Base
            (
                {
                    autograder.api.config.PARAM_USER_EMAIL.config_key: 'server-admin@test.edulinq.org',
                    autograder.api.config.PARAM_USER_PASS.config_key: 'server-admin',

                    autograder.api.config.PARAM_DRY_RUN.config_key: False,
                    autograder.api.config.PARAM_SKIP_EMAILS.config_key: False,
                    autograder.api.config.PARAM_SKIP_SOURCE_SYNC.config_key: False,
                    autograder.api.config.PARAM_SKIP_LMS_SYNC.config_key: False,
                    autograder.api.config.PARAM_SKIP_BUILD_IMAGES.config_key: True,
                    autograder.api.config.PARAM_SKIP_TEMPLATE_FILES.config_key: False,
                },
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
