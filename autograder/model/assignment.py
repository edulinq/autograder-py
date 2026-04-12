import typing

import edq.util.time
import lms.model.assignments
import lms.model.scores

def make_assignment(raw_data: typing.Dict[str, typing.Any]) -> lms.model.assignments.Assignment:
    """
    Create an LMS Toolkit assignment from raw data coming from the autograder.
    The raw data from the server should be a core.AssignmentInfo.
    """

    raw_due_date = raw_data.get('due-date', None)
    if (raw_due_date is not None):
        raw_due_date = edq.util.time.Timestamp(int(raw_due_date))

    data = {
        'id': raw_data['id'],
        'name': raw_data['name'],
        'points_possible': raw_data.get('max-points', None),
        'due_date': raw_due_date,
    }

    return lms.model.assignments.Assignment(**data)

def make_assignment_score(raw_data: typing.Dict[str, typing.Any]) -> lms.model.scores.AssignmentScore:
    """
    Create an LMS Toolkit assignment score from raw data coming from the autograder.
    The raw data from the server should be a model.SubmissionHistoryItem.
    """

    data = {
        'id': raw_data['id'],
        'score': raw_data['score'],
        'submission_date': edq.util.time.Timestamp(int(raw_data['grading_start_time'])),
        'graded_date': edq.util.time.Timestamp(int(raw_data['grading_start_time'])),
        'comment': raw_data['message'],
        'assignment': raw_data['assignment-id'],
        'user': raw_data['user'],
    }

    return lms.model.scores.AssignmentScore(**data)
