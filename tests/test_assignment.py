import json
import unittest
import time

import autograder.question
import autograder.assignment
import autograder.util.invoke

BASE_ERROR_MESSAGE = "Bad result for question."
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

    class QuestionAlwaysHardFail(autograder.question.Question):
        def score_question(self, submission):
            submission()

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
        # question, question, submission, score, graded_question, graded_question.
        test_cases = [
            # Incorrect submission, (fail, fail).
            (
                TestAssignment.QuestionBase(1), TestAssignment.QuestionBase(1),
                False, 0,
                {
                    "name": "QuestionBase",
                    "max_points": 1,
                    "score": 0,
                    "hard_fail": False,
                    "skipped": False,
                    "message": BASE_ERROR_MESSAGE
                },
                {
                    "name": "QuestionBase",
                    "max_points": 1,
                    "score": 0,
                    "hard_fail": False,
                    "skipped": False,
                    "message": BASE_ERROR_MESSAGE
                },
            ),

            # Incorrect submission, (fail, hard fail).
            (
                TestAssignment.QuestionBase(1), TestAssignment.QuestionHardFail(1),
                False, 0,
                {
                    "name": "QuestionBase",
                    "max_points": 1,
                    "score": 0,
                    "hard_fail": False,
                    "skipped": False,
                    "message": BASE_ERROR_MESSAGE
                },
                {
                    "name": "QuestionHardFail",
                    "max_points": 1,
                    "score": 0,
                    "hard_fail": True,
                    "skipped": False,
                    "message": BASE_ERROR_MESSAGE
                },
            ),

            # Incorrect submission, (hard fail, skip).
            (
                TestAssignment.QuestionHardFail(1), TestAssignment.QuestionBase(1),
                False, 0,
                {
                    "name": "QuestionHardFail",
                    "max_points": 1,
                    "score": 0,
                    "hard_fail": True,
                    "skipped": False,
                    "message": BASE_ERROR_MESSAGE
                },
                {
                    "name": "QuestionBase",
                    "max_points": 1,
                    "score": 0,
                    "hard_fail": False,
                    "skipped": True,
                    "message": SKIPPING_QUESTION_MESSAGE
                },
            ),
            (
                TestAssignment.QuestionHardFail(1), TestAssignment.QuestionHardFail(1),
                False, 0,
                {
                    "name": "QuestionHardFail",
                    "max_points": 1,
                    "score": 0,
                    "hard_fail": True,
                    "skipped": False,
                    "message": BASE_ERROR_MESSAGE
                },
                {
                    "name": "QuestionHardFail",
                    "max_points": 1,
                    "score": 0,
                    "hard_fail": False,
                    "skipped": True,
                    "message": SKIPPING_QUESTION_MESSAGE
                },
            ),

            # Correct submissions, possible question (hard fails only on error).
            # Expected graded questions (success, success).
            (
                TestAssignment.QuestionBase(1), TestAssignment.QuestionBase(1),
                True, 2,
                {
                    "name": "QuestionBase",
                    "max_points": 1,
                    "score": 1,
                    "hard_fail": False,
                    "skipped": False,
                    "message": ""
                },
                {
                    "name": "QuestionBase",
                    "max_points": 1,
                    "score": 1,
                    "hard_fail": False,
                    "skipped": False,
                    "message": ""
                },
            ),
            (
                TestAssignment.QuestionBase(1), TestAssignment.QuestionHardFail(1),
                True, 2,
                {
                    "name": "QuestionBase",
                    "max_points": 1,
                    "score": 1,
                    "hard_fail": False,
                    "skipped": False,
                    "message": ""
                },
                {
                    "name": "QuestionHardFail",
                    "max_points": 1,
                    "score": 1,
                    "hard_fail": False,
                    "skipped": False,
                    "message": ""
                },
            ),
            (
                TestAssignment.QuestionHardFail(1), TestAssignment.QuestionBase(1),
                True, 2,
                {
                    "name": "QuestionHardFail",
                    "max_points": 1,
                    "score": 1,
                    "hard_fail": False,
                    "skipped": False,
                    "message": ""
                },
                {
                    "name": "QuestionBase",
                    "max_points": 1,
                    "score": 1,
                    "hard_fail": False,
                    "skipped": False,
                    "message": ""
                },
            ),
            (
                TestAssignment.QuestionHardFail(1), TestAssignment.QuestionHardFail(1),
                True, 2,
                {
                    "name": "QuestionHardFail",
                    "max_points": 1,
                    "score": 1,
                    "hard_fail": False,
                    "skipped": False,
                    "message": ""
                },
                {
                    "name": "QuestionHardFail",
                    "max_points": 1,
                    "score": 1,
                    "hard_fail": False,
                    "skipped": False,
                    "message": ""
                },
            ),

            # Matrix of possible questions and impossible questions that always hard fail.
            # Correct submission, (success, hard fail).
            (
                TestAssignment.QuestionBase(1), TestAssignment.QuestionAlwaysHardFail(1),
                True, 1,
                {
                    "name": "QuestionBase",
                    "max_points": 1,
                    "score": 1,
                    "hard_fail": False,
                    "skipped": False,
                    "message": ""
                },
                {
                    "name": "QuestionAlwaysHardFail",
                    "max_points": 1,
                    "score": 0,
                    "hard_fail": True,
                    "skipped": False,
                    "message": BASE_ERROR_MESSAGE
                },
            ),
            (
                TestAssignment.QuestionHardFail(1), TestAssignment.QuestionAlwaysHardFail(1),
                True, 1,
                {
                    "name": "QuestionHardFail",
                    "max_points": 1,
                    "score": 1,
                    "hard_fail": False,
                    "skipped": False,
                    "message": ""
                },
                {
                    "name": "QuestionAlwaysHardFail",
                    "max_points": 1,
                    "score": 0,
                    "hard_fail": True,
                    "skipped": False,
                    "message": BASE_ERROR_MESSAGE
                },
            ),

            # Correct submission, impossible start (hard fail, skip).
            (
                TestAssignment.QuestionAlwaysHardFail(1), TestAssignment.QuestionBase(1),
                True, 0,
                {
                    "name": "QuestionAlwaysHardFail",
                    "max_points": 1,
                    "score": 0,
                    "hard_fail": True,
                    "skipped": False,
                    "message": BASE_ERROR_MESSAGE
                },
                {
                    "name": "QuestionBase",
                    "max_points": 1,
                    "score": 0,
                    "hard_fail": False,
                    "skipped": True,
                    "message": SKIPPING_QUESTION_MESSAGE
                },
            ),
            (
                TestAssignment.QuestionAlwaysHardFail(1), TestAssignment.QuestionHardFail(1),
                True, 0,
                {
                    "name": "QuestionAlwaysHardFail",
                    "max_points": 1,
                    "score": 0,
                    "hard_fail": True,
                    "skipped": False,
                    "message": BASE_ERROR_MESSAGE
                },
                {
                    "name": "QuestionHardFail",
                    "max_points": 1,
                    "score": 0,
                    "hard_fail": False,
                    "skipped": True,
                    "message": SKIPPING_QUESTION_MESSAGE
                },
            ),
            (
                TestAssignment.QuestionAlwaysHardFail(1), TestAssignment.QuestionAlwaysHardFail(1),
                True, 0,
                {
                    "name": "QuestionAlwaysHardFail",
                    "max_points": 1,
                    "score": 0,
                    "hard_fail": True,
                    "skipped": False,
                    "message": BASE_ERROR_MESSAGE
                },
                {
                    "name": "QuestionAlwaysHardFail",
                    "max_points": 1,
                    "score": 0,
                    "hard_fail": False,
                    "skipped": True,
                    "message": SKIPPING_QUESTION_MESSAGE
                },
            ),
        ]

        for i in range(len(test_cases)):
            with self.subTest(i = i):
                (
                    question_a, question_b,
                    submission, score,
                    graded_question_a, graded_question_b
                ) = test_cases[i]

                class TA(autograder.assignment.Assignment):
                    def _prepare_submission(self):
                        return lambda: submission

                questions = [question_a, question_b]

                assignment_name = f'test_hard_fail_{i}'
                assignment = TA(assignment_name, questions)
                result = assignment.grade(show_exceptions = True)

                total_score, max_score = result.get_score()

                self.assertEqual(total_score, score)
                self.assertEqual(max_score, 2)

                expected_result = autograder.assignment.GradedAssignment.from_dict({
                    "name": assignment_name,
                    "questions": [
                        graded_question_a,
                        graded_question_b,
                    ]
                })

                self.assertEqual(result, expected_result, "Unexpected result:"
                    + f" Expected: '{json.dumps(expected_result.to_dict(), indent = 4)}',"
                    + f" actual: '{json.dumps(result.to_dict(), indent = 4)}'.")
