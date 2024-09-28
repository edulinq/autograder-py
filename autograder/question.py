"""
A single question (test case) for an assignment.
"""

import abc
import functools
import json
import numbers
import traceback

import autograder.util.invoke
import autograder.util.timestamp

DEFAULT_TIMEOUT_SEC = 60

class Question(object):
    """
    Questions are grade-able portions of an assignment.
    They can also be thought of as "test cases".
    Note that all scoring is in ints.
    """

    def __init__(self, max_points = 0, name = None, timeout = DEFAULT_TIMEOUT_SEC):
        self.name = name
        if (self.name is None):
            self.name = type(self).__name__

        if ((not isinstance(max_points, numbers.Real)) or (max_points < 0)):
            raise ValueError("max_points must be a real number, got '%s' (type: %s)." % (
                max_points, type(max_points)))

        self.max_points = max_points
        self._timeout = timeout

        # Create the base scoring artifact.
        self.result = GradedQuestion(name = self.name, max_points = self.max_points)

    @abc.abstractmethod
    def score_question(self, submission, **kwargs):
        """
        Assign an actual score to this question.
        The implementer has full access to instance variables.
        However, users should generally just call the grading methods to manipulate the result.
        """

        pass

    def grade(self, submission, additional_data = {}, show_exceptions = False):
        """
        Invoke the scoring method using a timeout and cleanup.
        Return the graded question.
        """

        helper = functools.partial(self._score_helper, submission,
                additional_data = additional_data)

        self._internal_grade(helper, show_exceptions)

        return self.result

    def _internal_grade(self, helper, show_exceptions):
        try:
            success, value = autograder.util.invoke.with_timeout(self._timeout, helper)
        except Exception:
            if (show_exceptions):
                traceback.print_exc()

            self.set_result(0, "Raised an exception: " + traceback.format_exc())
            return

        if (not success):
            if (value is None):
                self.set_result(0, "Timeout (%d seconds)." % (self._timeout))
            else:
                self.set_result(0, "Error during execution: " + value)

            return

        # Because we use the helper method, we can only get None back if there was an error.
        if (value is None):
            self.set_result(0, "Error running scoring.")
            return

        self.result = value

    def _score_helper(self, submission, additional_data = {}):
        """
        Score the question, but make sure to return the result so
        multiprocessing can properly pass it back.
        """

        self.result = GradedQuestion(name = self.name, max_points = self.max_points)

        self.result.grading_start_time = autograder.util.timestamp.get()

        try:
            self.score_question(submission, **additional_data)
        except AutograderFailError:
            # The question has been failed, no additional output is required.
            pass

        self.result.grading_end_time = autograder.util.timestamp.get()

        return self.result

    def get_last_result(self):
        return self.result

    def get_score(self):
        return self.result.score

    # Grading functions.

    def check_not_implemented(self, value):
        if (value is None):
            self.fail("None returned.")

        if (isinstance(value, type(NotImplemented))):
            self.fail("NotImplemented returned.")

        return False

    def set_result(self, score, message):
        self.result.score = score
        self.result.message = message

    def set_score(self, score):
        self.result.score = score

    def set_message(self, message):
        self.result.message = message

    def fail(self, message):
        """
        Immediately fail this question, no partial credit.
        """

        self.set_result(0, message)
        raise AutograderFailError()

    def full_credit(self, message = ''):
        self.set_score(self.max_points)

        if (message != ''):
            self.set_message(message)

    def add_score(self, add_score):
        self.result.score += add_score

    def add_message(self, message, add_score = 0):
        if (self.result.message != ''):
            self.result.message += "\n"

        self.result.message += str(message)
        self.result.score += add_score

    def cap_score(self):
        """
        Cap the score so it is in [0, self.max_points].
        """

        self.result.score = max(0, min(self.max_points, self.result.score))

class AutograderFailError(RuntimeError):
    """
    This error indicates that fail() has been called on a question
    and execution should be stopped.
    """

    pass

class GradedQuestion(object):
    """
    The result of a question being graded with a submission.
    """

    def __init__(self, name = '', max_points = 0,
            score = 0, message = '',
            grading_start_time = None, grading_end_time = None,
            **kwargs):
        self.name = name
        self.max_points = max_points

        self.score = score
        self.message = message

        # Default the grading time to deal with situations where the grader throws an exception.
        now = autograder.util.timestamp.get()

        self.grading_start_time = now
        if (grading_start_time is not None):
            self.grading_start_time = autograder.util.timestamp.get(grading_start_time)

        self.grading_end_time = now
        if (grading_end_time is not None):
            self.grading_end_time = autograder.util.timestamp.get(grading_end_time)

    def to_dict(self):
        """
        Convert to all simple structures that can be later converted to JSON.
        """

        return {
            'name': self.name,
            'max_points': self.max_points,
            'score': self.score,
            'message': self.message,
            'grading_start_time': self.grading_start_time,
            'grading_end_time': self.grading_end_time,
        }

    @staticmethod
    def from_dict(data):
        """
        Partner to to_dict().
        """

        return GradedQuestion(**data)

    def scoring_report(self, prefix = ''):
        """
        Get a string that represents the scoring for this question.
        """

        if ((prefix != '') and (not prefix.endswith(' '))):
            prefix += ' '

        lines = ["%s%s: %d / %d" % (prefix, self.name, self.score, self.max_points)]
        if (self.message != ''):
            for line in self.message.split("\n"):
                lines.append(prefix + '   ' + line)

        return "\n".join(lines)

    def string(self, indent = None):
        return json.dumps(self.to_dict(), indent = indent)

    def __repr__(self):
        return self.string()

    def __eq__(self, other):
        return self.equals(other)

    def equals(self, other, ignore_messages = False, **kwargs):
        if (not isinstance(other, GradedQuestion)):
            return False

        if (
                (self.name != other.name)
                or (self.max_points != other.max_points)
                or (self.score != other.score)):
            return False

        if (ignore_messages):
            return True

        return self.message == other.message
