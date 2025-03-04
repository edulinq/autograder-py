import unittest
import time

import autograder.question
import autograder.assignment
import autograder.util.invoke

BASE_ERROR_MESSAGE = "Got a False."
SKIPPING_QUESTION_MESSAGE = "Grading stopped because of a hard error, skipping question..."

class TestAssignment(unittest.TestCase):
    class QuestionBase(autograder.question.Question):
        def score_question(self, submission):
            result = submission()

            if (result):
                self.full_credit()
            else:
                self.fail(BASE_ERROR_MESSAGE)

    class QuestionHardFail(autograder.question.Question):
        def score_question(self, submission):
            result = submission()

            if (result):
                self.full_credit()
            else:
                self.hard_fail(BASE_ERROR_MESSAGE)

    def test_base_full_credit(self):
        questions = [
            TestAssignment.QuestionBase(1),
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
            TestAssignment.QuestionBase(1),
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
            TestAssignment.QuestionBase(1, timeout = 0.05),
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

    def test_hard_fail(self):
        test_cases = [
            (
                [TestAssignment.QuestionBase(1), TestAssignment.QuestionBase(1)],
                [(False, False), (False, False)]
            ),
            (
                [TestAssignment.QuestionBase(1), TestAssignment.QuestionHardFail(1)],
                [(False, False), (True, False)]
            ),
            (
                [TestAssignment.QuestionHardFail(1), TestAssignment.QuestionBase(1)],
                [(True, False), (False, True)]
            ),
            (
                [TestAssignment.QuestionHardFail(1), TestAssignment.QuestionHardFail(1)],
                [(True, False), (False, True)]
            ),
        ]

        class TA(autograder.assignment.Assignment):
            def _prepare_submission(self):
                return lambda: False

        for i in range(len(test_cases)):
            with self.subTest(i = i):
                questions, expected_results = test_cases[i]

                assignment = TA(f'test_hard_fail_{i}', questions)
                result = assignment.grade(show_exceptions = True)

                total_score, max_score = result.get_score()

                self.assertEqual(total_score, 0)
                self.assertEqual(max_score, 2)

                for j in range(len(expected_results)):
                    (expected_hard_fail, expected_skipped) = expected_results[j]

                    self.assertEqual(expected_hard_fail, result.questions[j].hard_fail)
                    self.assertEqual(expected_skipped, result.questions[j].skipped)

                    if (expected_skipped):
                        self.assertIn(SKIPPING_QUESTION_MESSAGE, result.questions[j].message)
                    else:
                        self.assertIn(BASE_ERROR_MESSAGE, result.questions[j].message)

    def test_hard_fail_full_credit(self):
        test_cases = [
            [TestAssignment.QuestionBase(1), TestAssignment.QuestionBase(1)],
            [TestAssignment.QuestionBase(1), TestAssignment.QuestionHardFail(1)],
            [TestAssignment.QuestionHardFail(1), TestAssignment.QuestionBase(1)],
            [TestAssignment.QuestionHardFail(1), TestAssignment.QuestionHardFail(1)],
        ]

        class TA(autograder.assignment.Assignment):
            def _prepare_submission(self):
                return lambda: True

        for i in range(len(test_cases)):
            with self.subTest(i = i):
                questions = test_cases[i]

                assignment = TA(f'test_hard_fail_full_credit_{i}', questions)
                result = assignment.grade(show_exceptions = True)

                total_score, max_score = result.get_score()

                self.assertEqual(total_score, 2)
                self.assertEqual(max_score, 2)

                for j in range(len(questions)):
                    self.assertEqual(False, result.questions[j].hard_fail)
                    self.assertEqual(False, result.questions[j].skipped)

                    self.assertNotIn(BASE_ERROR_MESSAGE, result.questions[j].message)
