import typing

import lms.model.assignments
import lms.model.base

import autograder.model.assignment

class Course(lms.model.base.BaseType):
    """
    A course.
    """

    CORE_FIELDS = [
        'id',
        'name',
    ]

    def __init__(self,
            id: str,
            name: str,
            assignments: typing.Dict[str, lms.model.assignments.Assignment],
            **kwargs: typing.Any) -> None:
        super().__init__(**kwargs)

        self.id: str = id
        """ ID for this course. """

        self.name: str = name
        """ Name for this course. """

        self.assignments: typing.Dict[str, lms.model.assignments.Assignment] = assignments
        """ Assignments for this course, keyed by assignment id. """

    @classmethod
    def from_api(cls, data: typing.Dict[str, typing.Any]) -> 'Course':
        """ Convert a dict coming from autograder API JSON. """

        data = data.copy()

        data['assignments'] = {key: autograder.model.assignment.make_assignment(value) for (key, value) in data['assignments'].items()}

        return Course(**data)
