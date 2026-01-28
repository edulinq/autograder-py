"""
A single question (test case) for an assignment.
"""

import abc
import functools
import numbers
import traceback
import typing

import edq.util.json
import edq.util.time

import autograder.util.invoke

DEFAULT_TIMEOUT_SEC: float = 60
""" Default timeout for grading a question. """

class AutograderFailError(RuntimeError):
    """
    This error indicates that fail() has been called on a question
    and execution should be stopped.
    """

class AutograderHardFailError(RuntimeError):
    """
    This error indicates that hard_fail() has been called on a question
    and execution should be stopped for all questions in the assignment.
    """

class GradedQuestion(edq.util.json.DictConverter):
    """
    The result of a question being graded with a submission.
    """

    def __init__(self,
            name: str,
            max_points: float,
            score: float = 0,
            message: str = '',
            hard_fail: bool = False,
            skipped: bool = False,
            grading_start_time: typing.Union[edq.util.time.Timestamp, int, None] = None,
            grading_end_time: typing.Union[edq.util.time.Timestamp, int, None] = None,
            **kwargs: typing.Any) -> None:
        self.name: str = name
        """ The name of the question. """

        self.max_points: float = max_points
        """ The max points possible for this question. """

        self.score: float = score
        """ The score earned for this question. """

        self.message: str = message
        """ A message/feedback for the student. """

        self.hard_fail = hard_fail
        """ Whether this question triggered a hard fail during grading. """

        self.skipped = skipped
        """ Whether this question was skipped during grading. """

        # Default the grading time to deal with situations where the grader throws an exception.
        now = edq.util.time.Timestamp.now()

        if (grading_start_time is None):
            grading_start_time = now

        self.grading_start_time: typing.Any = edq.util.time.Timestamp(grading_start_time)
        """ When grading started. """

        if (grading_end_time is None):
            grading_end_time = now

        self.grading_end_time: typing.Any = edq.util.time.Timestamp(grading_end_time)
        """ When grading ended. """

    def to_dict(self) -> typing.Dict[str, typing.Any]:
        return {
            'name': self.name,
            'max_points': self.max_points,
            'score': self.score,
            'hard_fail': self.hard_fail,
            'skipped': self.skipped,
            'message': self.message,
            'grading_start_time': self.grading_start_time,
            'grading_end_time': self.grading_end_time,
        }

    @staticmethod
    def from_dict(data: typing.Dict[str, typing.Any]) -> 'GradedQuestion':
        return GradedQuestion(**data)

    def scoring_report(self, prefix: str = '') -> str:
        """
        Get a string that represents the scoring for this question.
        """

        if ((prefix != '') and (not prefix.endswith(' '))):
            prefix += ' '

        lines = [f"{prefix}{self.name}: {self.score} / {self.max_points}"]
        if (self.message != ''):
            for line in self.message.split("\n"):
                lines.append(prefix + '   ' + line)

        return "\n".join(lines)

    def __eq__(self, other: typing.Any) -> bool:
        return self.equals(other)

    def equals(self, other: typing.Any, ignore_messages: bool = False, **kwargs: typing.Any) -> bool:
        """ Check another graded question for equality. """

        if (not isinstance(other, GradedQuestion)):
            return False

        if (
                (self.name != other.name)
                or (self.max_points != other.max_points)
                or (self.score != other.score)
                or (self.hard_fail != other.hard_fail)
                or (self.skipped != other.skipped)):
            return False

        if (ignore_messages):
            return True

        return self.message == other.message

class Question:
    """
    Questions are grade-able portions of an assignment.
    They can also be thought of as "test cases".
    Note that all scoring is in ints.
    """

    def __init__(self,
            max_points: float = 0,
            name: typing.Union[str, None] = None,
            timeout: float = DEFAULT_TIMEOUT_SEC,
            ) -> None:
        if (name is None):
            name = type(self).__name__

        self.name: str = name
        """
        The name of this question.
        Defaults to the name of the question class.
        """

        if ((not isinstance(max_points, numbers.Real)) or (max_points < 0)):
            raise ValueError("max_points must be a real number, got '{max_points}' (type: '{type(max_points)}).")

        self.max_points: float = max_points
        """ The maximum number of points possible for this question (does not include extra credit). """

        self._timeout: float = timeout
        """ The number of seconds allowed when grading this question. """

        # Create the base scoring artifact.
        self.result: GradedQuestion = GradedQuestion(name = self.name, max_points = self.max_points)
        """
        The result of grading this question.
        A default/empty one is created on construction and is added to during the grading process.
        """

    @abc.abstractmethod
    def score_question(self, submission: typing.Any, **kwargs: typing.Any) -> None:
        """
        Assign an actual score to this question.
        The implementer has full access to instance variables.
        However, users should generally just call the grading methods to manipulate the result.
        """

    def grade(self, submission: typing.Any,
            additional_data: typing.Union[typing.Dict[str, typing.Any], None] = None,
            show_exceptions: bool = False) -> GradedQuestion:
        """
        Invoke the scoring method using a timeout and cleanup.
        Return the graded question.
        """

        if (additional_data is None):
            additional_data = {}

        helper = functools.partial(self._score_helper, submission,
                additional_data = additional_data)

        self._internal_grade(helper, show_exceptions)

        return self.result

    def _internal_grade(self, helper: typing.Callable, show_exceptions: bool) -> None:
        """
        Handle the internal process for grading a question.
        """

        try:
            success, value = autograder.util.invoke.with_timeout(self._timeout, helper)
        except Exception:
            if (show_exceptions):
                traceback.print_exc()

            self.set_result(0, "Raised an exception: " + traceback.format_exc())
            return

        if (not success):
            if (value is None):
                self.set_result(0, f"Timeout ({self._timeout} seconds).")
            else:
                self.set_result(0, f"Error during execution: '{value}'.")

            return

        # Because we use the helper method, we can only get None back if there was an error.
        if (value is None):
            self.set_result(0, "Error running scoring.")
            return

        self.result = value

    def _score_helper(self, submission: typing.Any,
            additional_data: typing.Union[typing.Dict[str, typing.Any], None] = None,
            ) -> GradedQuestion:
        """
        Score the question, but make sure to return the result so
        multiprocessing can properly pass it back.
        """

        if (additional_data is None):
            additional_data = {}

        self.result = GradedQuestion(name = self.name, max_points = self.max_points)

        self.result.grading_start_time = edq.util.time.Timestamp.now()

        try:
            self.score_question(submission, **additional_data)
        except AutograderFailError:
            # The question has been failed, no additional output is required.
            pass
        except AutograderHardFailError:
            # The question has been failed hard, signal to stop grading.
            self.result.hard_fail = True

        self.result.grading_end_time = edq.util.time.Timestamp.now()

        return self.result

    def get_last_result(self) -> GradedQuestion:
        """ Get the current grading result. """

        return self.result

    def get_score(self) -> float:
        """ Get the current assigned score for this grading. """

        return self.result.score

    # Grading functions.

    def check_not_implemented(self, value: typing.Any) -> bool:
        """
        Check if the given value is a marker for not implemented.
        By default, this checked for a NotImplemented value.
        Children may override this to define their own not implemented values.
        """

        if (value is None):
            self.fail("None returned.")

        if (isinstance(value, type(NotImplemented))):
            self.fail("NotImplemented returned.")

        return False

    def set_result(self, score: float, message: str) -> None:
        """ Set the score and message for the current grading (overrides any other values). """

        self.result.score = score
        self.result.message = message

    def set_score(self, score: float) -> None:
        """ Set the score for the current grading (overrides any other values). """

        self.result.score = score

    def set_message(self, message: str) -> None:
        """ Set the message for the current grading (overrides any other values). """

        self.result.message = message

    def fail(self, message: str) -> None:
        """
        Immediately fail this question, no partial credit.
        """

        self.set_result(0, message)
        raise AutograderFailError()

    def hard_fail(self, message: str) -> None:
        """
        Immediately hard fail this question, no partial credit.
        Grading will be stopped for the rest of the assignment.
        """

        self.set_result(0, message)
        raise AutograderHardFailError()

    def full_credit(self, message: str = '') -> None:
        """ Assign full credit for this question. """

        self.set_score(self.max_points)

        if (message != ''):
            self.set_message(message)

    def add_score(self, add_score: float) -> None:
        """ Add the given score to the current score for this question. """

        self.result.score += add_score

    def add_message(self, message: str, add_score: float = 0) -> None:
        """ Add the given message (and optional score) to the current grading for this question. """

        if (self.result.message != ''):
            self.result.message += "\n"

        self.result.message += str(message)
        self.result.score += add_score

    def cap_score(self) -> None:
        """
        Cap the current score so it is in [0, self.max_points].
        """

        self.result.score = max(0, min(self.max_points, self.result.score))
