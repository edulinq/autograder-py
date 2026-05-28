import typing

import edq.testing.unittest
import edq.util.time

import autograder.question

TEST_TIMESTAMP: edq.util.time.Timestamp = edq.util.time.Timestamp(123)

class TestQuestion(edq.testing.unittest.BaseTest):
    """ Test questions. """

    def test_grade_base(self):
        """ Test that grading can run successfully. """

        # [(action, expected result, message substring), ...]
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
                None,
            ),

            # Full Credit
            (
                lambda question: question.full_credit(),
                autograder.question.GradedQuestion(
                    name = '_TestQustion', max_points = 10,
                    grading_start_time = TEST_TIMESTAMP, grading_end_time = TEST_TIMESTAMP,
                    score = 10,
                ),
                None,
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
                None,
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
                None,
            ),

            # Set Score
            (
                lambda question: question.set_score(5),
                autograder.question.GradedQuestion(
                    name = '_TestQustion', max_points = 10,
                    grading_start_time = TEST_TIMESTAMP, grading_end_time = TEST_TIMESTAMP,
                    score = 5,
                ),
                None,
            ),

            # Set Message
            (
                lambda question: question.set_message('Test Message'),
                autograder.question.GradedQuestion(
                    name = '_TestQustion', max_points = 10,
                    grading_start_time = TEST_TIMESTAMP, grading_end_time = TEST_TIMESTAMP,
                    message = 'Test Message',
                ),
                None,
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
                None,
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
                None,
            ),

            # Add Score
            (
                lambda question: question.add_score(-1),
                autograder.question.GradedQuestion(
                    name = '_TestQustion', max_points = 10,
                    grading_start_time = TEST_TIMESTAMP, grading_end_time = TEST_TIMESTAMP,
                    score = -1,
                ),
                None,
            ),

            # Add Message
            (
                lambda question: question.add_message('Test Message'),
                autograder.question.GradedQuestion(
                    name = '_TestQustion', max_points = 10,
                    grading_start_time = TEST_TIMESTAMP, grading_end_time = TEST_TIMESTAMP,
                    message = 'Test Message',
                ),
                None,
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
                None,
            ),

            # Cap Score - Max
            (
                lambda question: (question.set_score(-100), question.cap_score())[0],
                autograder.question.GradedQuestion(
                    name = '_TestQustion', max_points = 10,
                    grading_start_time = TEST_TIMESTAMP, grading_end_time = TEST_TIMESTAMP,
                    score = 0,
                ),
                None,
            ),

            # Cap Score - Min
            (
                lambda question: (question.set_score(100), question.cap_score())[0],
                autograder.question.GradedQuestion(
                    name = '_TestQustion', max_points = 10,
                    grading_start_time = TEST_TIMESTAMP, grading_end_time = TEST_TIMESTAMP,
                    score = 10,
                ),
                None,
            ),

            # Code does not run.
            (
                lambda question: (question.full_credit(), exec('import ZZZ'))[0],  # pylint: disable=exec-used
                autograder.question.GradedQuestion(
                    name = '_TestQustion', max_points = 10,
                    grading_start_time = TEST_TIMESTAMP, grading_end_time = TEST_TIMESTAMP,
                    score = 0,
                    message = '',
                ),
                "No module named 'ZZZ'",
            ),
        ]

        class _TestQustion(autograder.question.Question):
            def __init__(self, action: typing.Callable):
                super().__init__(10)

                self.action = action

            def score_question(self, submission: typing.Any, **kwargs: typing.Any) -> None:
                self.action(self)

        for (i, test_case) in enumerate(test_cases):
            (action, expected, message_substring) = test_case

            with self.subTest(msg = f"Case {i}"):
                question = _TestQustion(action)
                actual = question.grade(None)

                # Normalize timestamps.
                actual.grading_start_time = TEST_TIMESTAMP
                actual.grading_end_time = TEST_TIMESTAMP

                # If we are checking the message as a substring, normalize the result message.
                actual_message = actual.message
                if (message_substring is not None):
                    actual.message = ''

                self.assertJSONEqual(expected, actual)

                if (message_substring is not None):
                    self.assertIn(message_substring, actual_message, 'Message is not as expected.')

    def test_scoring_report_base(self):
        """ Test that output looks correct. """

        # [(graded question, expected), ...]
        test_cases = [
            # Zero
            (
                autograder.question.GradedQuestion(name = 'Test Question', max_points = 10),
                'Test Question: 0 / 10',
            ),

            # Int
            (
                autograder.question.GradedQuestion(name = 'Test Question', score = 5, max_points = 10),
                'Test Question: 5 / 10',
            ),

            # Float - Simple
            (
                autograder.question.GradedQuestion(name = 'Test Question', score = 5.5, max_points = 10),
                'Test Question: 5.5 / 10',
            ),

            # Float - Zero
            (
                autograder.question.GradedQuestion(name = 'Test Question', score = 5.0, max_points = 10),
                'Test Question: 5.0 / 10',
            ),

            # Float - Double Zero
            (
                autograder.question.GradedQuestion(name = 'Test Question', score = 5.00, max_points = 10),
                'Test Question: 5.0 / 10',
            ),

            # Float - Irrational
            (
                autograder.question.GradedQuestion(name = 'Test Question', score = 10 / 3, max_points = 10),
                'Test Question: 3.33 / 10',
            ),

            # Float - Irrational - Max Points
            (
                autograder.question.GradedQuestion(name = 'Test Question', score = 10 / 3, max_points = 20 / 3),
                'Test Question: 3.33 / 6.67',
            ),
        ]

        for (i, test_case) in enumerate(test_cases):
            (graded_question, expected) = test_case

            with self.subTest(msg = f"Case {i}"):
                actual = graded_question.scoring_report()
                self.assertEqual(expected, actual)
