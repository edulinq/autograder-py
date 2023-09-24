import autograder.api.common
import autograder.assignment

API_ENDPOINT = '/api/v01/peek'
API_KEYS = ['user', 'pass', 'course', 'assignment']

def send(server, config_data):
    """
    Take in a server address
    and config data (of the form produced by autograder.api.common.parse_config()),
    and make a peek request.
    Returns:
        (success, <message or graded assignment>)
    """

    url = "%s%s" % (server, API_ENDPOINT)

    data = {}
    for key in API_KEYS:
        if (config_data.get(key) is None):
            return (False, "No request made, missing required config '%s'." % (key))

        data[key] = config_data[key]

    body, message = autograder.api.common.send_api_request(url, data = data)

    if (body is None):
        response = "The autograder failed to peek your last submission."
        response += "\nMessage from the autograder: " + message
        return (False, response)

    if (body['result'] is None):
        return (True, None)

    result = autograder.assignment.GradedAssignment.from_dict(body['result'])

    return (True, result)
