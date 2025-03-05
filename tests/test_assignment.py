import json
import unittest
import time

import autograder.question
import autograder.assignment
import autograder.util.invoke

BASE_ERROR_MESSAGE = "Bad result for question."
HARD_FAIL_ERROR_MESSAGE = "Fix your code! Hard failing..."
SKIPPING_QUESTION_MESSAGE = "Grading stopped because of a hard error, skipping question..."

class TestAssignment(unittest.TestCase):
    class QuestionBase(autograder.question.Question):
        def score_question(self, submission):
            result = submission()

            if (result):
                self.full_credit()
            else:
                self.fail(BASE_ERROR_MESSAGE)

    class QuestionAlwaysPass(autograder.question.Question):
        def score_question(self, submission):
            self.full_credit()

    class QuestionAlwaysFail(autograder.question.Question):
        def score_question(self, submission):
            self.fail(BASE_ERROR_MESSAGE)

    class QuestionAlwaysHardFail(autograder.question.Question):
        def score_question(self, submission):
            self.hard_fail(HARD_FAIL_ERROR_MESSAGE)

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
        # Each test case is a tuple of question, question, graded_question, graded_question.
        test_cases = [
            # 2 points, (success, success).
            (
                TestAssignment.QuestionAlwaysPass(1), TestAssignment.QuestionAlwaysPass(1),
                {
                    "name": "QuestionAlwaysPass",
                    "max_points": 1,
                    "score": 1,
                    "hard_fail": False,
                    "skipped": False,
                    "message": ""
                },
                {
                    "name": "QuestionAlwaysPass",
                    "max_points": 1,
                    "score": 1,
                    "hard_fail": False,
                    "skipped": False,
                    "message": ""
                },
            ),

            # 1 point, (success, hard fail).
            (
                TestAssignment.QuestionAlwaysPass(1), TestAssignment.QuestionAlwaysHardFail(1),
                {
                    "name": "QuestionAlwaysPass",
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
                    "message": HARD_FAIL_ERROR_MESSAGE
                },
            ),

            # 0 points, (hard fail, skip).
            (
                TestAssignment.QuestionAlwaysHardFail(1), TestAssignment.QuestionAlwaysPass(1),
                {
                    "name": "QuestionAlwaysHardFail",
                    "max_points": 1,
                    "score": 0,
                    "hard_fail": True,
                    "skipped": False,
                    "message": HARD_FAIL_ERROR_MESSAGE
                },
                {
                    "name": "QuestionAlwaysPass",
                    "max_points": 1,
                    "score": 0,
                    "hard_fail": False,
                    "skipped": True,
                    "message": SKIPPING_QUESTION_MESSAGE
                },
            ),
            (
                TestAssignment.QuestionAlwaysHardFail(1), TestAssignment.QuestionAlwaysHardFail(1),
                {
                    "name": "QuestionAlwaysHardFail",
                    "max_points": 1,
                    "score": 0,
                    "hard_fail": True,
                    "skipped": False,
                    "message": HARD_FAIL_ERROR_MESSAGE
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

            # 1 point, (success, fail).
            (
                TestAssignment.QuestionAlwaysPass(1), TestAssignment.QuestionAlwaysFail(1),
                {
                    "name": "QuestionAlwaysPass",
                    "max_points": 1,
                    "score": 1,
                    "hard_fail": False,
                    "skipped": False,
                    "message": ""
                },
                {
                    "name": "QuestionAlwaysFail",
                    "max_points": 1,
                    "score": 0,
                    "hard_fail": False,
                    "skipped": False,
                    "message": BASE_ERROR_MESSAGE
                },
            ),

            # 1 point, (fail, success).
            (
                TestAssignment.QuestionAlwaysFail(1), TestAssignment.QuestionAlwaysPass(1),
                {
                    "name": "QuestionAlwaysFail",
                    "max_points": 1,
                    "score": 0,
                    "hard_fail": False,
                    "skipped": False,
                    "message": BASE_ERROR_MESSAGE
                },
                {
                    "name": "QuestionAlwaysPass",
                    "max_points": 1,
                    "score": 1,
                    "hard_fail": False,
                    "skipped": False,
                    "message": ""
                },
            ),

            # 0 points, (fail, fail).
            (
                TestAssignment.QuestionAlwaysFail(1), TestAssignment.QuestionAlwaysFail(1),
                {
                    "name": "QuestionAlwaysFail",
                    "max_points": 1,
                    "score": 0,
                    "hard_fail": False,
                    "skipped": False,
                    "message": BASE_ERROR_MESSAGE
                },
                {
                    "name": "QuestionAlwaysFail",
                    "max_points": 1,
                    "score": 0,
                    "hard_fail": False,
                    "skipped": False,
                    "message": BASE_ERROR_MESSAGE
                },
            ),

            # 0 points, (hard fail, skip).
            (
                TestAssignment.QuestionAlwaysHardFail(1), TestAssignment.QuestionAlwaysFail(1),
                {
                    "name": "QuestionAlwaysHardFail",
                    "max_points": 1,
                    "score": 0,
                    "hard_fail": True,
                    "skipped": False,
                    "message": HARD_FAIL_ERROR_MESSAGE
                },
                {
                    "name": "QuestionAlwaysFail",
                    "max_points": 1,
                    "score": 0,
                    "hard_fail": False,
                    "skipped": True,
                    "message": SKIPPING_QUESTION_MESSAGE
                },
            ),

            # 0 points, (fail, hard fail).
            (
                TestAssignment.QuestionAlwaysFail(1), TestAssignment.QuestionAlwaysHardFail(1),
                {
                    "name": "QuestionAlwaysFail",
                    "max_points": 1,
                    "score": 0,
                    "hard_fail": False,
                    "skipped": False,
                    "message": BASE_ERROR_MESSAGE
                },
                {
                    "name": "QuestionAlwaysHardFail",
                    "max_points": 1,
                    "score": 0,
                    "hard_fail": True,
                    "skipped": False,
                    "message": HARD_FAIL_ERROR_MESSAGE
                },
            ),
        ]

        class TA(autograder.assignment.Assignment):
            def _prepare_submission(self):
                pass

        for i in range(len(test_cases)):
            with self.subTest(i = i):
                (question_a, question_b, graded_question_a, graded_question_b) = test_cases[i]

                questions = [question_a, question_b]

                assignment_name = f'test_hard_fail_{i}'
                assignment = TA(assignment_name, questions)
                result = assignment.grade(show_exceptions = True)

                total_score, max_score = result.get_score()
                expected_score = graded_question_a["score"] + graded_question_b["score"]

                self.assertEqual(total_score, expected_score)
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
