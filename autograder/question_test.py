import typing

import edq.testing.unittest
import edq.util.time

import autograder.question

TEST_TIMESTAMP: edq.util.time.Timestamp = edq.util.time.Timestamp(123)

class TestQuestion(edq.testing.unittest.BaseTest):
    """ Test questions. """

    def test_grade_base(self):
        """ Test that grading can run successfully. """

        # [(action, expected result, expected message), ...]
        test_cases = [
            # Nothing
            (
                lambda question: None,
                autograder.question.GradedQuestion(
                    name = '_TestQustion', max_points = 10,
                    grading_start_time = TEST_TIMESTAMP, grading_end_time = TEST_TIMESTAMP,
                    score = 0,
                    message = '',
                ),
            ),

            # Full Credit
            (
                lambda question: question.full_credit(),
                autograder.question.GradedQuestion(
                    name = '_TestQustion', max_points = 10,
                    grading_start_time = TEST_TIMESTAMP, grading_end_time = TEST_TIMESTAMP,
                    score = 10,
                ),
            ),

            # Full Credit with Message
            (
                lambda question: question.full_credit('Test Message'),
                autograder.question.GradedQuestion(
                    name = '_TestQustion', max_points = 10,
                    grading_start_time = TEST_TIMESTAMP, grading_end_time = TEST_TIMESTAMP,
                    score = 10,
                    message = 'Test Message',
                ),
            ),

            # Set Result
            (
                lambda question: question.set_result(5, 'Test Message'),
                autograder.question.GradedQuestion(
                    name = '_TestQustion', max_points = 10,
                    grading_start_time = TEST_TIMESTAMP, grading_end_time = TEST_TIMESTAMP,
                    score = 5,
                    message = 'Test Message',
                ),
            ),

            # Set Score
            (
                lambda question: question.set_score(5),
                autograder.question.GradedQuestion(
                    name = '_TestQustion', max_points = 10,
                    grading_start_time = TEST_TIMESTAMP, grading_end_time = TEST_TIMESTAMP,
                    score = 5,
                ),
            ),

            # Set Message
            (
                lambda question: question.set_message('Test Message'),
                autograder.question.GradedQuestion(
                    name = '_TestQustion', max_points = 10,
                    grading_start_time = TEST_TIMESTAMP, grading_end_time = TEST_TIMESTAMP,
                    message = 'Test Message',
                ),
            ),

            # Fail
            (
                lambda question: (question.full_credit(), question.fail('Test Message'))[0],
                autograder.question.GradedQuestion(
                    name = '_TestQustion', max_points = 10,
                    grading_start_time = TEST_TIMESTAMP, grading_end_time = TEST_TIMESTAMP,
                    score = 0,
                    message = 'Test Message',
                ),
            ),

            # Hard Fail
            (
                lambda question: question.hard_fail('Test Message'),
                autograder.question.GradedQuestion(
                    name = '_TestQustion', max_points = 10,
                    grading_start_time = TEST_TIMESTAMP, grading_end_time = TEST_TIMESTAMP,
                    hard_fail = True,
                    score = 0,
                    message = 'Test Message',
                ),
            ),

            # Add Score
            (
                lambda question: question.add_score(-1),
                autograder.question.GradedQuestion(
                    name = '_TestQustion', max_points = 10,
                    grading_start_time = TEST_TIMESTAMP, grading_end_time = TEST_TIMESTAMP,
                    score = -1,
                ),
            ),

            # Add Message
            (
                lambda question: question.add_message('Test Message'),
                autograder.question.GradedQuestion(
                    name = '_TestQustion', max_points = 10,
                    grading_start_time = TEST_TIMESTAMP, grading_end_time = TEST_TIMESTAMP,
                    message = 'Test Message',
                ),
            ),

            # Add Message with Score
            (
                lambda question: question.add_message('Test Message', add_score = 2),
                autograder.question.GradedQuestion(
                    name = '_TestQustion', max_points = 10,
                    grading_start_time = TEST_TIMESTAMP, grading_end_time = TEST_TIMESTAMP,
                    score = 2,
                    message = 'Test Message',
                ),
            ),

            # Cap Score - Max
            (
                lambda question: (question.set_score(-100), question.cap_score())[0],
                autograder.question.GradedQuestion(
                    name = '_TestQustion', max_points = 10,
                    grading_start_time = TEST_TIMESTAMP, grading_end_time = TEST_TIMESTAMP,
                    score = 0,
                ),
            ),

            # Cap Score - Min
            (
                lambda question: (question.set_score(100), question.cap_score())[0],
                autograder.question.GradedQuestion(
                    name = '_TestQustion', max_points = 10,
                    grading_start_time = TEST_TIMESTAMP, grading_end_time = TEST_TIMESTAMP,
                    score = 10,
                ),
            ),
        ]

        class _TestQustion(autograder.question.Question):
            def __init__(self, action: typing.Callable):
                super().__init__(10)

                self.action = action

            def score_question(self, submission: typing.Any, **kwargs: typing.Any) -> None:
                self.action(self)

        for (i, test_case) in enumerate(test_cases):
            (action, expected) = test_case

            with self.subTest(msg = f"Case {i}"):
                question = _TestQustion(action)
                actual = question.grade(None)

                # Normalize timestamps.
                actual.grading_start_time = TEST_TIMESTAMP
                actual.grading_end_time = TEST_TIMESTAMP

                self.assertJSONEqual(expected, actual)
