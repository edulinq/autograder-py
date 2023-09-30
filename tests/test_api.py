import unittest
import sys

import autograder.api.history
import autograder.api.peek
import autograder.assignment
import autograder.question
import tests.server

SERVER_URL = "http://127.0.0.1:%s" % (tests.server.PORT)
FORMAT_STR = "\n--- Expected ---\n%s\n--- Actual ---\n%s\n---\n"

TEST_CREDENTIALS = {
    'user': 'user@test.com',
    'pass': 'password123',
    'course': 'COURSE101',
    'assignment': 'hw0',
}

@unittest.skipUnless(sys.platform.startswith('linux'), 'linux only (multiprocessing)')
class TestAPI(unittest.TestCase):
    """
    Test API calls by mocking a server.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._server_process = None

    def setUp(self):
        self._server_process = tests.server.start()

    def tearDown(self):
        tests.server.stop(self._server_process)
        self._server_process = None

    def test_peek_base(self):
        success, response = autograder.api.peek.send(SERVER_URL, TEST_CREDENTIALS.copy())

        if (not success):
            self.fail("Peek request returned a failure: '%s'." % (response))

        expected = autograder.assignment.GradedAssignment(
            name = 'HW0',
            questions = [
                autograder.question.GradedQuestion(
                    name = 'Q1', max_points = 1, score = 1, message = ''
                ),
                autograder.question.GradedQuestion(
                    name = 'Q2', max_points = 1, score = 1, message = ''
                ),
                autograder.question.GradedQuestion(
                    name = 'Style', max_points = 0, score = 0, message = 'Style is clean!'
                ),
            ],
        )

        self.assertEquals(response, expected, FORMAT_STR % (expected.string(4), response.string(4)))

    def test_history_base(self):
        success, response = autograder.api.history.send(SERVER_URL, TEST_CREDENTIALS.copy())

        if (not success):
            self.fail("History request returned a failure: '%s'." % (response))

        expected = [
            {
                "id": "COURSE101::hw0::user@test.com::1",
                "message": "",
                "max_points": 2,
                "score": 1,
                "grading_start_time": "2023-09-25T22:50:54.225052Z"
            },
            {
                "id": "COURSE101::hw0::user@test.com::2",
                "message": "",
                "max_points": 2,
                "score": 1,
                "grading_start_time": "2023-09-25T22:51:54.225052Z"
            },
        ]

        self.assertEquals(response, expected)
