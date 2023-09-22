import autograder.api.common
import autograder.assignment
import autograder.util.hash

API_ENDPOINT = '/api/v01/submit'
API_KEYS = ['user', 'pass', 'course', 'assignment', 'message']

def send(server, config_data, files = []):
    """
    Take in a server address
    and config data (of the form produced by autograder.api.common.parse_config()),
    and make a subimt request.
    Returns:
        (success, <message or graded assignment>)
    """

    url = "%s%s" % (server, API_ENDPOINT)

    data = {}
    for key in API_KEYS:
        if (config_data.get(key) is None):
            return (False, "No request made, missing required config '%s'." % (key))

        data[key] = config_data[key]

    # Don't send cleartext passwords.
    data['pass'] = autograder.util.hash.sha256_hex(data['pass'])

    body, message = autograder.api.common.send_api_request(url, data = data, files = files)

    if (body is None):
        response = "The autograder failed to grade your assignment."
        response += "\nMessage from the autograder: " + message
        return (False, response)

    result = autograder.assignment.GradedAssignment.from_dict(body['result'])

    return (True, result)
