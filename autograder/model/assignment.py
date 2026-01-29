import typing

import lms.model.scores

def make_assignment_score(raw_score: typing.Dict[str, typing.Any]) -> lms.model.scores.AssignmentScore:
    """
    Create an LMS Toolkit assignment score from raw data coming from the autograder.
    The raw data from the server should be a model.SubmissionHistoryItem.
    """

    data = {
        'id': raw_score['id'],
        'score': raw_score['score'],
        'submission_date': raw_score['grading_start_time'],
        'graded_date': raw_score['grading_start_time'],
        'comment': raw_score['message'],
        'assignment_query': raw_score['assignment-id'],
        'user_query': raw_score['user'],
    }

    return lms.model.scores.AssignmentScore(**data)
