"""
What is necessary to grade a single assignment.
"""

import inspect
import json
import traceback
import typing

import autograder.code
import autograder.question
import autograder.util.submission
import autograder.util.timestamp

# TEST - Timestamps.
class GradedAssignment:
    """
    The result of an assignment being graded with a submission.
    """

    def __init__(self,
            name: str,
            questions: typing.List[autograder.question.GradedQuestion],
            prologue: typing.Union[str, None] = None,
            epilogue: typing.Union[str, None] = None,
            grading_start_time: typing.Union[typing.Any, None] = None,
            grading_end_time: typing.Union[typing.Any, None] = None,
            proxy_start_time: typing.Union[typing.Any, None] = None,
            proxy_end_time: typing.Union[typing.Any, None] = None,
            **kwargs: typing.Any) -> None:
        self.name: str = name
        """ The name of the graded assignment. """

        self.questions: typing.List[autograder.question.GradedQuestion] = questions
        """ The result of grading for each question. """

        self.prologue: typing.Union[str, None] = prologue
        """ Text to include before the grading result. """

        self.epilogue: typing.Union[str, None] = epilogue
        """ Text to include after the grading result. """

        if (grading_start_time is None):
            grading_start_time = autograder.util.timestamp.MISSING_TIMESTAMP

        self.grading_start_time: typing.Any = autograder.util.timestamp.get(grading_start_time)
        """ When grading started. """

        if (grading_end_time is None):
            grading_end_time = autograder.util.timestamp.MISSING_TIMESTAMP

        self.grading_end_time: typing.Any = autograder.util.timestamp.get(grading_end_time)
        """ When grading ended. """

        if (proxy_start_time is None):
            proxy_start_time = autograder.util.timestamp.MISSING_TIMESTAMP

        self.proxy_start_time: typing.Any = autograder.util.timestamp.get(proxy_start_time)
        """ When proxy grading started. """

        if (proxy_end_time is None):
            proxy_end_time = autograder.util.timestamp.MISSING_TIMESTAMP

        self.proxy_end_time: typing.Any = autograder.util.timestamp.get(proxy_end_time)
        """ When proxy grading ended. """

    def to_dict(self) -> typing.Dict[str, typing.Any]:
        """
        Convert to all simple structures that can be later converted to JSON.
        """

        return {
            'name': self.name,
            'questions': [question.to_dict() for question in self.questions],
            'grading_start_time': self.grading_start_time,
            'grading_end_time': self.grading_end_time,
            'proxy_start_time': self.proxy_start_time,
            'proxy_end_time': self.proxy_end_time,
        }

    def to_test_submission(self, options: typing.Union[typing.Dict[str, typing.Any], None] = None) -> typing.Dict[str, typing.Any]:
        """
        Output a dict that can be used as a test submission.
        """

        if (options is None):
            options = {}

        results = self.to_dict()

        del results['grading_start_time']
        del results['grading_end_time']
        del results['proxy_start_time']
        del results['proxy_end_time']

        for question in results['questions']:
            del question['grading_start_time']
            del question['grading_end_time']

        test_submission = {
            'result': results,
        }

        test_submission.update(options)

        return test_submission

    @staticmethod
    def from_dict(data: typing.Dict[str, typing.Any]) -> 'GradedAssignment':
        """
        Partner to to_dict().
        """

        data = dict(data)

        if ('questions' in data):
            data['questions'] = [
                autograder.question.GradedQuestion(**question)
                for question in data['questions']
            ]

        return GradedAssignment(**data)

    def get_score(self) -> typing.Tuple[float, float]:
        """
        Return (total score, max score).
        """

        total_score = 0
        max_score = 0

        for question in self.questions:
            total_score += question.score
            max_score += question.max_points

        return (total_score, max_score)

    def report(self, prefix: str = '') -> str:
        """
        Return a string representation of the grading for this assignment.
        """

        if ((prefix != '') and (not prefix.endswith(' '))):
            prefix += ' '

        output: typing.List[str] = []

        output += self._format_logue(self.prologue, prefix)

        output += [
            prefix + "Autograder transcript for assignment: %s." % (self.name),
            prefix + "Grading started at %s and ended at %s." % (
                autograder.util.timestamp.get(self.grading_start_time, pretty = True),
                autograder.util.timestamp.get(self.grading_end_time, pretty = True))
        ]

        total_score = 0
        max_score = 0

        for question in self.questions:
            total_score += question.score
            max_score += question.max_points

            output.append(question.scoring_report(prefix = prefix))

        output.append('')
        output.append(prefix + "Total: %d / %d" % (total_score, max_score))

        output += self._format_logue(self.epilogue, prefix)

        return "\n".join(output)

    def _format_logue(self, text: typing.Union[str, None], prefix: str) -> typing.List[str]:
        """ Format the output logue (prologe/epilogue). """

        if ((text is None) or (text == '')):
            return []

        lines = text.splitlines()
        return [prefix + line.rstrip() for line in lines]

    def __eq__(self, other: object) -> bool:
        return self.equals(other)

    def string(self, indent: typing.Any = None) -> str:
        return json.dumps(self.to_dict(), indent = indent)

    def __repr__(self) -> str:
        return self.string()

    def equals(self, other: object, **kwargs: typing.Any) -> bool:
        if (not isinstance(other, GradedAssignment)):
            return False

        if ((self.name != other.name) or (len(self.questions) != len(other.questions))):
            return False

        for i in range(len(self.questions)):
            if (not self.questions[i].equals(other.questions[i], **kwargs)):
                return False

        return True

class Assignment:
    """
    A collection of questions to be scored.
    """

    def __init__(self,
            name: typing.Union[str, None] = None,
            questions: typing.Union[typing.List[autograder.question.Question], None] = None,
            input_dir: str = '.',
            output_dir: str = '.',
            work_dir: str = '.',
            prep_submission: bool = True,
            additional_data: typing.Union[typing.Dict[str, typing.Any], None] = None,
            **kwargs: typing.Any) -> None:
        if (name is None):
            name = type(self).__name__

        self.name: str = name
        """
        The display name for this assignment.
        Defaults to the (unqualified) name of this class.
        """

        if (questions is None):
            questions = []

        self.questions = questions
        """ The questions for this assignment. """

        self.input_dir: str = input_dir
        """ The base directory that houses student inputs for this assignment. """

        self.output_dir: str = output_dir
        """
        The base directory where output will be written for this assignment.
        A successful grading should result in a `result.json` created in this directory.
        """

        self.work_dir: str = work_dir
        """ The base directory that the grader is run in. """

        self.prep_submission: bool = prep_submission
        """ Whether or not to call self.prepare_submission() to prepare the input directory before grading. """

        if (additional_data is None):
            additional_data = {}

        self.additional_data: typing.Dict[str, typing.Any] = additional_data
        """ Additional data that can be passed to the grader. """

        self.result: typing.Union[GradedAssignment, None] = None
        """ The result of grading. """

    def grade(self, **kwargs: typing.Any) -> GradedAssignment:
        """ Grade this assignment. """

        try:
            return self._grade_submission(self._prepare_submission(), **kwargs)
        except Exception:
            now = autograder.util.timestamp.get()

            questions = []
            for question in self.questions:
                questions.append(autograder.question.GradedQuestion(
                    name = question.name,
                    max_points = question.max_points, score = 0,
                    message = "Submission could not be graded.",
                    grading_start_time = now, grading_end_time = now))

            epilogue = ("\nSubmission could not be graded because of the following error:"
                    + "\n---\n%s---" % (traceback.format_exc()))

            return GradedAssignment(
                name = self.name,
                questions = questions,
                grading_start_time = now, grading_end_time = now,
                epilogue = epilogue)

    def _grade_submission(self,
            submission: typing.Union[object, None],
            show_exceptions: bool = False,
            **kwargs: typing.Any) -> GradedAssignment:
        """
        Grade an assignment by grading all the questions.

        The submission argument is the result of _prepare_submission().
        """

        self.result = GradedAssignment(name = self.name, questions = [])
        self.result.grading_start_time = autograder.util.timestamp.get()

        stop_grading = False
        for question in self.questions:
            if (stop_grading):
                now = autograder.util.timestamp.get()

                self.result.questions.append(autograder.question.GradedQuestion(
                    name = question.name,
                    max_points = question.max_points, score = 0,
                    message = "Grading stopped because of a hard error, skipping question...",
                    grading_start_time = now, grading_end_time = now,
                    skipped = True))
            else:
                result = question.grade(submission,
                    additional_data = self.additional_data,
                    show_exceptions = show_exceptions)

                self.result.questions.append(result)

                stop_grading = result.hard_fail

        self.result.grading_end_time = autograder.util.timestamp.get()

        return self.result

    def _prepare_submission(self) -> typing.Union[object, None]:
        """
        Prepare the submission in the input directory for grading.
        The result of this is what will be passed to grade().
        Child classes may leave this default behavior or override.

        This implementation will check the prep_submission argument passed in the constructor.
        If true the input directory will be prepared, otherwise None will be returned.
        """

        if (self.prep_submission):
            return autograder.util.submission.prepare(self.input_dir)

        return None

def load_assignment_classes(path: str) -> typing.List[typing.Type[Assignment]]:
    """
    Recursively load all the assignment classes in a path (file or dir).
    """

    module = autograder.code.sanitize_and_import_path(path)
    assignments = []

    for name in dir(module):
        obj = getattr(module, name)

        if (not inspect.isclass(obj)):
            continue

        if (obj == autograder.assignment.Assignment):
            continue

        if (issubclass(obj, autograder.assignment.Assignment)):
            assignments.append(obj)

    return assignments

def fetch_assignment_class(path: str) -> typing.Type[Assignment]:
    """
    Recursively fetch a single assignment class from a path.
    If exactly one assignment is not found, then raise an error.
    """

    assignments = load_assignment_classes(path)

    if (len(assignments) == 0):
        raise ValueError(("Assignment file (%s) does not contain any instances of"
            + " autograder.assignment.Assignment.") % (path))
    elif (len(assignments) > 1):
        raise ValueError(("Assignment file (%s) contains more than one (%d) instances of"
            + " autograder.assignment.Assignment.") % (path, len(assignments)))

    return assignments[0]
