import json
import time
import typing

import edq.testing.unittest
import edq.util.time

import autograder.assignment
import autograder.question
import autograder.testing.asserts
import autograder.util.invoke

BASE_ERROR_MESSAGE = "Bad result for question."
HARD_FAIL_ERROR_MESSAGE = "Fix your code! Hard failing..."
SKIPPING_QUESTION_MESSAGE = "Grading stopped because of a hard error, skipping question..."

class TestAssignment(edq.testing.unittest.BaseTest):
    """ Test assignments. """

    class QuestionBase(autograder.question.Question):
        """ A testing question that is nothing special. """

        def score_question(self, submission, **kwargs: typing.Any):
            result = submission()

            if (result):
                self.full_credit()
            else:
                self.fail(BASE_ERROR_MESSAGE)

    class QuestionAlwaysPass(autograder.question.Question):
        """ A testing question that should always pass. """

        def score_question(self, submission, **kwargs: typing.Any):
            self.full_credit()

    class QuestionAlwaysFail(autograder.question.Question):
        """ A testing question that should always fail. """

        def score_question(self, submission, **kwargs: typing.Any):
            self.fail(BASE_ERROR_MESSAGE)

    class QuestionAlwaysHardFail(autograder.question.Question):
        """ A testing question that should always hard fail. """

        def score_question(self, submission, **kwargs: typing.Any):
            self.hard_fail(HARD_FAIL_ERROR_MESSAGE)

    def test_base_full_credit(self):
        """ Test getting full credit. """

        questions = [
            TestAssignment.QuestionBase(1),
        ]

        class TA(autograder.assignment.Assignment):
            """ A test class representing a TA's example submission. """

            def _prepare_submission(self):
                return lambda: True

        assignment = TA('test_base_full_credit', questions)
        result = assignment.grade(show_exceptions = True)

        total_score, max_score = result.get_score()

        self.assertEqual(total_score, 1)
        self.assertEqual(max_score, 1)

    def test_base_fail(self):
        """ Test failing. """

        questions = [
            TestAssignment.QuestionBase(1),
        ]

        class TA(autograder.assignment.Assignment):
            """ A test class representing a TA's example submission. """

            def _prepare_submission(self):
                return lambda: False

        assignment = TA('test_base_fail', questions)
        result = assignment.grade(show_exceptions = True)

        total_score, max_score = result.get_score()

        self.assertEqual(total_score, 0)
        self.assertEqual(max_score, 1)

    def test_sleep_fail(self):
        """ Test failing because of timing out. """

        questions = [
            TestAssignment.QuestionBase(1, timeout = 0.05),
        ]

        def submission():
            time.sleep(0.25)
            return True

        class TA(autograder.assignment.Assignment):
            """ A test class representing a TA's example submission. """

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
        """ Test hard failing. """

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
            """ A test class representing a TA's example submission. """

            def _prepare_submission(self):
                pass

        for (i, test_case) in enumerate(test_cases):
            with self.subTest(i = i):
                (question_a, question_b, graded_question_a, graded_question_b) = test_case

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

    def test_report_score_format(self):
        """ Test the formatting for assignment scores. """

        # [(graded assignment, expected lines), ...]
        test_cases = [
            # Zero
            (
                autograder.assignment.GradedAssignment(
                    name = 'Test Assignment',
                    questions = [],
                    grading_start_time = edq.util.time.Timestamp(123), grading_end_time = edq.util.time.Timestamp(123),
                    proxy_start_time = edq.util.time.Timestamp(123), proxy_end_time = edq.util.time.Timestamp(123),
                ),
                [
                    'Autograder transcript for assignment: Test Assignment',
                    'Grading started at <PRETTY TIME> and ended at <PRETTY TIME>.',
                    '',
                    'Total: 0 / 0',
                ],
            ),

            # Int
            (
                autograder.assignment.GradedAssignment(
                    name = 'Test Assignment',
                    questions = [
                        autograder.question.GradedQuestion(name = 'A', score = 1, max_points = 10),
                    ],
                    grading_start_time = edq.util.time.Timestamp(123), grading_end_time = edq.util.time.Timestamp(123),
                    proxy_start_time = edq.util.time.Timestamp(123), proxy_end_time = edq.util.time.Timestamp(123),
                ),
                [
                    'Autograder transcript for assignment: Test Assignment',
                    'Grading started at <PRETTY TIME> and ended at <PRETTY TIME>.',
                    'A: 1 / 10',
                    '',
                    'Total: 1 / 10',
                ],
            ),

            # Float - Simple
            (
                autograder.assignment.GradedAssignment(
                    name = 'Test Assignment',
                    questions = [
                        autograder.question.GradedQuestion(name = 'A', score = 5.5, max_points = 10),
                    ],
                    grading_start_time = edq.util.time.Timestamp(123), grading_end_time = edq.util.time.Timestamp(123),
                    proxy_start_time = edq.util.time.Timestamp(123), proxy_end_time = edq.util.time.Timestamp(123),
                ),
                [
                    'Autograder transcript for assignment: Test Assignment',
                    'Grading started at <PRETTY TIME> and ended at <PRETTY TIME>.',
                    'A: 5.5 / 10',
                    '',
                    'Total: 5.5 / 10',
                ],
            ),

            # Float - Zero
            (
                autograder.assignment.GradedAssignment(
                    name = 'Test Assignment',
                    questions = [
                        autograder.question.GradedQuestion(name = 'A', score = 5.0, max_points = 10),
                    ],
                    grading_start_time = edq.util.time.Timestamp(123), grading_end_time = edq.util.time.Timestamp(123),
                    proxy_start_time = edq.util.time.Timestamp(123), proxy_end_time = edq.util.time.Timestamp(123),
                ),
                [
                    'Autograder transcript for assignment: Test Assignment',
                    'Grading started at <PRETTY TIME> and ended at <PRETTY TIME>.',
                    'A: 5.0 / 10',
                    '',
                    'Total: 5.0 / 10',
                ],
            ),

            # Float - Double Zero
            (
                autograder.assignment.GradedAssignment(
                    name = 'Test Assignment',
                    questions = [
                        autograder.question.GradedQuestion(name = 'A', score = 5.00, max_points = 10),
                    ],
                    grading_start_time = edq.util.time.Timestamp(123), grading_end_time = edq.util.time.Timestamp(123),
                    proxy_start_time = edq.util.time.Timestamp(123), proxy_end_time = edq.util.time.Timestamp(123),
                ),
                [
                    'Autograder transcript for assignment: Test Assignment',
                    'Grading started at <PRETTY TIME> and ended at <PRETTY TIME>.',
                    'A: 5.0 / 10',
                    '',
                    'Total: 5.0 / 10',
                ],
            ),

            # Float - Irrational
            (
                autograder.assignment.GradedAssignment(
                    name = 'Test Assignment',
                    questions = [
                        autograder.question.GradedQuestion(name = 'A', score = 10 / 3, max_points = 10),
                    ],
                    grading_start_time = edq.util.time.Timestamp(123), grading_end_time = edq.util.time.Timestamp(123),
                    proxy_start_time = edq.util.time.Timestamp(123), proxy_end_time = edq.util.time.Timestamp(123),
                ),
                [
                    'Autograder transcript for assignment: Test Assignment',
                    'Grading started at <PRETTY TIME> and ended at <PRETTY TIME>.',
                    'A: 3.33 / 10',
                    '',
                    'Total: 3.33 / 10',
                ],
            ),

            # Float - Irrational - Max Points
            (
                autograder.assignment.GradedAssignment(
                    name = 'Test Assignment',
                    questions = [
                        autograder.question.GradedQuestion(name = 'A', score = 1, max_points = 10 / 3),
                    ],
                    grading_start_time = edq.util.time.Timestamp(123), grading_end_time = edq.util.time.Timestamp(123),
                    proxy_start_time = edq.util.time.Timestamp(123), proxy_end_time = edq.util.time.Timestamp(123),
                ),
                [
                    'Autograder transcript for assignment: Test Assignment',
                    'Grading started at <PRETTY TIME> and ended at <PRETTY TIME>.',
                    'A: 1 / 3.33',
                    '',
                    'Total: 1 / 3.33',
                ],
            ),
        ]

        for (i, test_case) in enumerate(test_cases):
            (graded_assignment, expected_lines) = test_case

            with self.subTest(msg = f"Case {i}"):
                expected = '\n'.join(expected_lines)
                actual = graded_assignment.report()
                autograder.testing.asserts.equals_clean_pretty_time(self, expected, actual)
