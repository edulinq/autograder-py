import typing

import edq.util.time

import autograder.assignment

def display_grading_result(
        api_response: typing.Dict[str, typing.Any],
        grading_result: typing.Union[autograder.assignment.GradedAssignment, None],
        include_found_user: bool = False,
        include_found_submission: bool = False,
        ) -> int:
    """
    Display the result of a grading endpoint, e.g., a grading report.
    Return the recommended exit status.
    """

    message = api_response.get('message', '')
    if ((message is not None) and (message != '')):
        # Replace any timestamps in the message.
        message = edq.util.time.Timestamp.convert_embedded(message, pretty = True)

        print("--- Message from Autograder ---")
        print(message)
        print("-------------------------------")

    if (include_found_user and (not api_response['found-user'])):
        print("Proxy user not found.")
        return 10

    if (include_found_submission and (not api_response['found-submission'])):
        print("Target submission not found.")
        return 11

    if (api_response['rejected']):
        print("Submission was rejected by the autograder.")
        return 12

    if (not api_response['grading-success']):
        print("Grading failed.")
        return 13

    if (grading_result is not None):
        print(grading_result.report())

    return 0
