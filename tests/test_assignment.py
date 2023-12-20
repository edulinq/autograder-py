import unittest
import time

import autograder.question
import autograder.assignment
import autograder.util.invoke

class TestAssignment(unittest.TestCase):
    class Q1(autograder.question.Question):
        def score_question(self, submission):
            result = submission()

            if (result):
                self.full_credit()
            else:
                self.fail("Got a False.")

    def test_base_full_credit(self):
        questions = [
            TestAssignment.Q1(1),
        ]

        class TA(autograder.assignment.Assignment):
            def _prepare_submission(self):
                return lambda: True

        assignment = TA('test_base_full_credit', questions)
        result = assignment.grade(show_exceptions = True)

        total_score, max_score = result.get_score()

        self.assertEqual(total_score, 1)
        self.assertEqual(max_score, 1)

    def test_base_fail(self):
        questions = [
            TestAssignment.Q1(1),
        ]

        class TA(autograder.assignment.Assignment):
            def _prepare_submission(self):
                return lambda: False

        assignment = TA('test_base_fail', questions)
        result = assignment.grade(show_exceptions = True)

        total_score, max_score = result.get_score()

        self.assertEqual(total_score, 0)
        self.assertEqual(max_score, 1)

    def test_sleep_fail(self):
        questions = [
            TestAssignment.Q1(1, timeout = 0.05),
        ]

        def submission():
            time.sleep(0.25)
            return True

        class TA(autograder.assignment.Assignment):
            def _prepare_submission(self):
                return submission

        # Shorten the reap time for testing.
        old_reap_time = autograder.util.invoke.REAP_TIME_SEC
        autograder.util.invoke.REAP_TIME_SEC = 0.01

        try:
            assignment = TA('test_sleep_fail', questions)
            result = assignment.grade(show_exceptions = True)
        finally:
            autograder.util.invoke.REAP_TIME_SEC = old_reap_time

        total_score, max_score = result.get_score()

        self.assertEqual(total_score, 0)
        self.assertEqual(max_score, 1)
