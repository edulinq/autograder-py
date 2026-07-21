"""
Fetch a gradebook for this course.
"""

import typing

import lms.model.assignments
import lms.model.scores
import lms.model.users

import autograder.api.common
import autograder.api.config
import autograder.model.assignment
import autograder.model.config

API_ENDPOINT: str = 'courses/gradebook/fetch'
API_WRITE: bool = False
API_PARAMS: typing.List[autograder.api.config.APIParam] = [
    autograder.api.config.PARAM_SERVER,
    autograder.api.config.PARAM_USER_EMAIL,
    autograder.api.config.PARAM_USER_PASS,

    autograder.api.config.PARAM_COURSE,

    autograder.api.config.PARAM_COURSE_USER_REFERENCES,
    autograder.api.config.PARAM_TARGET_ASSIGNMENTS,
]

def send(config: autograder.model.config.Config, **kwargs: typing.Any) -> lms.model.scores.Gradebook:
    """ Send a request to the autograder. """

    response = autograder.api.common.make_api_request(API_ENDPOINT, config, API_PARAMS, write = API_WRITE, **kwargs)

    assignment_queries: typing.List[lms.model.assignments.AssignmentQuery] = []
    user_queries: typing.List[lms.model.users.UserQuery] = []

    for assignment_id in response['gradebook']:
        assignment_queries.append(lms.model.assignments.AssignmentQuery(id = assignment_id))
        if (not user_queries):
            for user_email in response['gradebook'][assignment_id]:
                user_queries.append(lms.model.users.UserQuery(id = user_email))

    gradebook = lms.model.scores.Gradebook(assignment_queries, user_queries)

    for user_scores in response['gradebook'].values():
        for raw_score in user_scores.values():
            if (raw_score is not None):
                score = autograder.model.assignment.make_assignment_score(raw_score)
                score.user = lms.model.users.UserQuery(id = raw_score['user'])
                gradebook.add(score)

    return gradebook
